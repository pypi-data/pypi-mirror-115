from setuptools import setup, find_packages

setup(name="simple_k8s_orm",
      version="0.1.0",
      description="Simple (probably) kubeapi ORM",
      author="Florian Baier",
      author_email="f.baier1@gmail.com",
      packages=find_packages(),
      install_requires=['requests', 'kubernetes'])