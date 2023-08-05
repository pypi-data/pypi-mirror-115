from setuptools import setup, find_packages

setup(
    name='ingenii-azure-data-platform',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        "pulumi==3.9.0",
        "pulumi-azure-native==1.19.0",
        "pulumi-azuread == 4.3.0",
        "pulumi-databricks==0.0.2",
        "HiYaPyCo==0.4.16",
        "dynaconf==3.1.4",
        "yamale==3.0.7",
        "autopep8"
    ]
)
