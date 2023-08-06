import kubernetes
from kubernetes.client.rest import ApiException
from pprint import pprint


def get_instance(namespace):
    return ORM(namespace)

class ORM:

    def __init__(self, namespace):
        self.lock = False
        self.namespace = namespace

        self.configuration = kubernetes.config.load_incluster_config()

        self.api_client = kubernetes.client.ApiClient(self.configuration)
        self.custom_object_api = kubernetes.client.CustomObjectsApi(self.api_client)

    def get_live_object(self, group, version, namespace, plural, name):
        return self.custom_object_api.get_namespaced_custom_object(group, version, namespace, plural, name)

    def add_object(self, object, depth=0):
        mapped_attributes = object.serialize(self, create=True, depth=depth)
        version = mapped_attributes['version']
        namespace = self.namespace
        group = mapped_attributes['api_group']
        plural = mapped_attributes['plural']
        kind = mapped_attributes['kind']
        body = {
            "apiVersion": "%s/%s" % (group, version),
            "kind": kind,
            "metadata": {
                "name": object.name
            },
            "spec": mapped_attributes['body']
        }
        try:
            api_response = self.custom_object_api.create_namespaced_custom_object(group, version, namespace, plural, body)
        except ApiException as e:
            raise Exception("Exception while creating object: %s" % str(e))

    def delete_object(self, object):
        mapped_attributes = object.serialize(self)
        version = mapped_attributes['version']
        namespace = self.namespace
        group = mapped_attributes['api_group']
        plural = mapped_attributes['plural']
        kind = mapped_attributes['kind']
        try:
            api_response = self.custom_object_api.delete_namespaced_custom_object(group, version, namespace, plural, object.name)
        except ApiException as e:
            raise Exception("Exception when deleting object: %s" % str(e))


    def patch_object(self, object, depth=0):
        mapped_attributes = object.serialize(self, patch=True, depth=depth)
        version = mapped_attributes['version']
        namespace = self.namespace
        group = mapped_attributes['api_group']
        plural = mapped_attributes['plural']
        kind = mapped_attributes['kind']
        body = {
            "apiVersion": "%s/%s" % (group, version),
            "kind": kind,
            "metadata": {
                "name": object.name
            },
            "spec": mapped_attributes['body']
        }
        try:
            api_response = self.custom_object_api.patch_namespaced_custom_object(group, version, namespace, plural, object.name, body)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->patch_namespaced_custom_object: %s\n" % e)

    def get_object(self, class_obj, name):
        version = class_obj.version
        namespace = self.namespace
        group = class_obj.api_group
        plural = class_obj.plural
        try:
            return class_obj.deserialize(class_obj, name, self)
        except Exception as ex:
            print(str(ex))
            return None

    def get_all_objects(self, class_obj):
        version = class_obj.version
        namespace = self.namespace
        group = class_obj.api_group
        plural = class_obj.plural
        ret_list = list()
        data = self.custom_object_api.list_namespaced_custom_object(group, version, namespace, plural)
        for item in data['items']:
            if item is not None:
                print(item)
                ret_list.append(class_obj.deserialize(class_obj, raw_data_inc=item, client=self))
        return ret_list