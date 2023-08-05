import os
import yamale
import hiyapyco as hco
from glob import glob
from hashlib import md5
from dynaconf import Dynaconf
from dynaconf.base import LazySettings
from typing import OrderedDict


class ConfigParser:
    merge_methods = {
        "merge": hco.METHOD_MERGE,
        "simple": hco.METHOD_SIMPLE,
        "substitute": hco.METHOD_SUBSTITUTE,
    }

    def __init__(self, schema_path: str, default_config_path: str, customer_config_path: str, search_depth: int = 5) -> None:
        if not schema_path or not default_config_path or not customer_config_path:
            raise ValueError(
                "schema_path, default_config_path and customer_config_path attributes are required.")

        self.schema_path = self._find_file_path(
            schema_path, depth=search_depth)
        self.default_config_path = self._find_file_path(
            default_config_path, depth=search_depth)
        self.customer_config_path = self._find_file_path(
            query=customer_config_path, default_file_path=self.default_config_path, depth=search_depth)

    def _find_file_path(self, query: str, depth: int = 5, default_file_path=None) -> str:
        i = 0
        while i <= depth:
            i += 1
            findings = glob(query, recursive=True)
            for result in findings:
                return os.path.abspath(result)
            if (os.getcwd() == os.path.abspath(os.sep)) or (i == depth):
                return default_file_path
            os.chdir("../")

    def validate_schema(self):
        yaml_config = hco.load(
            [self.default_config_path, self.customer_config_path], method=hco.METHOD_MERGE)
        schema = yamale.make_schema(self.schema_path)
        data = yamale.make_data(content=hco.dump(yaml_config))
        try:
            yamale.validate(schema, data)
            print("The configuration schema is valid. ✅")
        except ValueError as e:
            print(f"The configuration schema is NOT valid! ❌\n{e}")
            exit(1)
        return self

    def load_as_ordered_dict(self, merge_method: str = "merge") -> OrderedDict:
        # Return an OrderedDict of the YAML configs.
        return hco.load([self.default_config_path, self.customer_config_path], method=self.merge_methods[merge_method])

    def load_as_dynaconf(self, envvar_prefix="ADP") -> LazySettings:
        return Dynaconf(
            settings_files=[
                self.default_config_path,
                self.customer_config_path
            ],
            envvar_prefix=envvar_prefix,
        )


class PlatformConfigurationException(Exception):
    ...


class PlatformConfiguration:
    def __init__(self, stack: str, config_object: LazySettings) -> None:
        region = config_object["general"]["region"].lower()
        if region not in self.azure_region_name_map:
            raise PlatformConfigurationException(
                f'Region name {region} not recognised.'
            )
        self.stack = stack
        self.config_object = config_object
        self.prefix = config_object["general"]["prefix"]
        self.region_long_name = config_object["general"]["region"]
        self.region_short_name = self.azure_region_name_map[region]
        self.tags = config_object["general"]["tags"]
        self.unique_id = config_object["general"]["unique_id"]

    azure_region_name_map = {
        "eastus": "eus",
        "eastus2": "eus2",
        "centralus": "cus",
        "northcentralus": "ncus",
        "southcentralus": "scus",
        "westcentralus": "wcus",
        "westus": "wus",
        "westus2": "wus2",
        "westus3": "wus3",
        "australiaeast": "aue",
        "australiacentral": "auc",
        "australiacentral2": "auc2",
        "australiasoutheast": "ause",
        "southafricanorth": "san",
        "southafricawest": "saw",
        "centralindia": "cin",
        "southindia": "sin",
        "westindia": "win",
        "eastasia": "eas",
        "southeastasia": "seas",
        "japaneast": "jpe",
        "japanwest": "jpw",
        "jioindiawest": "jinw",
        "jioindiacentral": "jinc",
        "koreacentral": "koc",
        "koreasouth": "kos",
        "canadacentral": "cac",
        "canadaeast": "cae",
        "francecentral": "frc",
        "francesouth": "frs",
        "germanywestcentral": "gewc",
        "germanynorth": "gen",
        "norwayeast": "nwye",
        "norwaywest": "nwyw",
        "switzerlandnorth": "swn",
        "switzerlandwest": "sww",
        "uaenorth": "uaen",
        "uaecentral": "uaec",
        "brazilsouth": "brs",
        "brazilsoutheast": "brse",
        "northeurope": "neu",
        "westeurope": "weu",
        "swedencentral": "swec",
        "swedensouth": "swes",
        "uksouth": "uks",
        "ukwest": "ukw",
    }

    azure_iam_role_definitions = {
        # General
        "Owner": "/providers/Microsoft.Authorization/roleDefinitions/8e3af657-a8ff-443c-a75c-2fe8c4bcb635",
        "Contributor": "/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c",
        "Reader": "/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
        # Key Vault
        "Key Vault Administrator": "/providers/Microsoft.Authorization/roleDefinitions/00482a5a-887f-4fb3-b363-3b7fe8e74483",
        "Key Vault Secrets Reader": "/providers/Microsoft.Authorization/roleDefinitions/4633458b-17de-408a-b874-0445c86b69e6",
        # Storage
        "Storage Blob Data Owner": "/providers/Microsoft.Authorization/roleDefinitions/b7e6dc6d-f1e8-4753-8033-0f276bb0955b",
        "Storage Blob Data Contributor": "/providers/Microsoft.Authorization/roleDefinitions/ba92f5b4-2d11-453d-a403-e96b0029c9fe",
        "Storage Blob Data Reader": "/providers/Microsoft.Authorization/roleDefinitions/2a2b9908-6ea1-4ae2-8e65-a410df84e7d1",
        "Storage Blob Delegator": "/providers/Microsoft.Authorization/roleDefinitions/db58b8e5-c6ad-4a2a-8342-4190687cbf4a"
    }

    azure_resource_name_map = {
        "resource_group": "rg",
        "virtual_network": "vnet",
        "subnet": "snet",
        "route_table": "rt",
        "network_security_group": "nsg",
        "nat_gateway": "ngw",
        "public_ip": "pip",
        "private_endpoint": "pe",
        "databricks_workspace": "dbw",
        "databricks_cluster": "dbwc",
        "service_principal": "sp",
        "storage_blob_container": "sbc",
        "dns_zone": "dz",
        "private_dns_zone": "prdz",
        "datafactory": "adf"
    }

    def generate_name(self, resource_type: str, resource_name: str) -> str:
        resource_type = resource_type.lower()
        if resource_type == "user_group":
            return f"{self.prefix.upper()}-{self.stack.title()}-{resource_name.title()}"
        elif resource_type == "gateway_subnet":
            return "Gateway"
        elif resource_type == "key_vault":
            return f"{self.prefix}-{self.stack}-{self.region_short_name}-kv-{resource_name}-{self.unique_id}"
        elif resource_type == "storage_account":
            return f"{self.prefix}{self.stack}{resource_name}{self.unique_id}"
        elif resource_type in self.azure_resource_name_map:
            return f"{self.prefix}-{self.stack}-{self.region_short_name}-{self.azure_resource_name_map[resource_type]}-{resource_name.lower()}"
        else:
            raise Exception(f"Resource type {resource_type} not recognised.")

    # This function arbitrary number of string arguments and returns an MD5 hash based on them.
    def generate_hash(self, *args: str):
        concat = "".join(args).encode("utf-8")
        return md5(concat).hexdigest()
