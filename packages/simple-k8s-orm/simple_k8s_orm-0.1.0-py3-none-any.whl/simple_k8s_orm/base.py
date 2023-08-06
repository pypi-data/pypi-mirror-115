
from pprint import pprint

def map_circular_reference(reference_class_obj, class_obj, attribute_name):
    for c in class_obj.mapped_attributes:
        if c['name'] == attribute_name:
            c['mapped_type'] = reference_class_obj


class ORMBase:

    mapped_attributes = {}
    api_group = ""
    kind = ""
    version = ""
    plural = ""

    @staticmethod
    def deserialize(class_obj, name=None, client=None, depth=0, raw_data_inc=None):
        depth += 1
        version = class_obj.version
        namespace = client.namespace
        group = class_obj.api_group
        plural = class_obj.plural
        if raw_data_inc is None:
            try:
                raw_data = client.get_live_object(group, version, namespace, plural, name)
            except Exception as ex:
                raise Exception(str(ex))
        else:
            raw_data = raw_data_inc
        class_to_create = class_obj
        attributes_to_map = class_to_create.mapped_attributes
        parameter_list = [raw_data['metadata']['name']]
        for attribute in attributes_to_map:
            attribute_name = attribute['name']
            if attribute['type'] == "ref":
                if depth <= attribute['deserialize_depth']:
                    if attribute['mapped_field_name'] in raw_data['spec']:
                        mapped_class = attribute['mapped_type']
                        parameter_list.append(mapped_class.deserialize(mapped_class, raw_data['spec'][attribute_name], client, depth=depth))
                    else:
                        parameter_list.append(None)
                else:
                    parameter_list.append(None)
            elif attribute['type'] == "list":
                if depth <= attribute['deserialize_depth']:
                    if attribute['mapped_field_name'] in raw_data['spec']:
                        mapped_class = attribute['mapped_type']
                        mapped_list = list()
                        for item in raw_data['spec'][attribute_name]:
                            mapped_list.append(mapped_class.deserialize(mapped_class, item, client))
                        parameter_list.append(mapped_list)
                    else:
                        parameter_list.append(list())
                else:
                    parameter_list.append(None)

            elif attribute['type'] == "str":
                if attribute_name in raw_data['spec']:
                    parameter_list.append(raw_data['spec'][attribute_name])
                else:
                    parameter_list.append(None)
            elif attribute['type'] == "array":
                if attribute_name in raw_data['spec']:
                    append_list = list()
                    for item in raw_data['spec'][attribute_name]:
                        append_list.append(item)
                    parameter_list.append(append_list)
                else:
                    parameter_list.append(list())
        object = class_to_create(*parameter_list)
        print(object)
        return object


    def serialize(self, client, create=False, patch=False, depth=0):
        depth += 1
        class_to_create = self.__class__
        attributes_to_map = class_to_create.mapped_attributes
        attributes_map = dict()
        attributes_map['body'] = dict()
        attributes_map['api_group'] = class_to_create.api_group
        attributes_map['version'] = class_to_create.version
        attributes_map['kind'] = class_to_create.kind
        attributes_map['plural'] = class_to_create.plural
        for at in attributes_to_map:
            name = at['name']
            type = at['type']
            if type == "str":
                value = getattr(self, name)
                attributes_map['body'][name] = str(value)
            elif type == "ref":
                if depth <= at['deserialize_depth']:
                    item = getattr(self, name)
                    mapped_field_name = at['mapped_field_name']
                    mapped_class = at['mapped_type']
                    mapped_api_group = mapped_class.api_group
                    mapped_version = mapped_class.version
                    mapped_plural = mapped_class.plural
                    try:
                        client.get_live_object(mapped_api_group, mapped_version, client.namespace, mapped_plural, item.name)
                        attributes_map['body'][mapped_field_name] = item.name
                        if patch:
                            print("Referenced object exists, patching %s/%s" % (class_to_create.kind, item.name))
                            client.patch_object(item, depth=depth)
                    except Exception as ex:
                        if create:
                            print("Referenced object does not exist, creating %s/%s. Exception %s" % (class_to_create.kind, item.name, str(ex)))
                            try:
                                client.add_object(item, depth=depth)
                            except Exception as ex2:
                                if str(ex2).find("409") != -1:
                                    pass
                                else:
                                    raise Exception("Exception while adding object: %s" % str(ex2))
                            attributes_map['body'][mapped_field_name] = item.name
                        else:
                            raise Exception("Referenced object %s/%s does not exist" % (class_to_create.kind, item.name))
            elif type == "list":
                if depth <= at['deserialize_depth']:
                    items = getattr(self, name)
                    mapped_field_name = at['mapped_field_name']
                    mapped_class = at['mapped_type']
                    mapped_api_group = mapped_class.api_group
                    mapped_version = mapped_class.version
                    mapped_kind = mapped_class.kind
                    mapped_plural = mapped_class.plural
                    if items.__len__() > 0:
                        attributes_map['body'][mapped_field_name] = list()
                        for i in items:
                            try:
                                client.get_live_object(mapped_api_group, mapped_version, client.namespace, mapped_plural, i.name)
                                if patch:
                                    print("Referenced object exists, patching %s/%s" % (class_to_create.kind, i.name))
                                    client.patch_object(i, depth=depth)
                            except Exception as ex:
                                if create:
                                    print("Referenced object does not exist, creating %s/%s" % (class_to_create.kind, i.name))
                                    client.add_object(i, depth=depth)
                                else:
                                    raise Exception("Referenced object %s/%s does not exist" % (class_to_create.kind, i.name))
                            i.serialize(client)
                            attributes_map['body'][mapped_field_name].append(i.name)
            elif type == "array":
                items = getattr(self, name)
                if items.__len__() > 0:
                    attributes_map['body'][name] = list()
                    for i in items:
                        attributes_map['body'][name].append(i)
        return attributes_map
