from pulumi_azure_native.storage import NetworkRuleSetArgs as StorageNetworkRuleSetArgs
from pulumi_azure_native.keyvault import (
    NetworkRuleSetArgs as KeyVaultNetworkRuleSetArgs,
)
import os
from hashlib import md5
from ipaddress import ip_network
from pulumi_azure_native import authorization


def ensure_type(value, types):
    if isinstance(value, types):
        return value
    else:
        raise TypeError(
            f"Value {value} is {type(value),}, but should be {types}!")


def get_os_root_path() -> str:
    return os.path.abspath(os.sep)


def cidrsubnet(cidr_subnet: str, new_prefix: int, network_number: int):
    return list(ip_network(cidr_subnet).subnets(new_prefix=new_prefix))[
        network_number
    ].exploded


def user_group_role_assignment(principal_id: str, role_definition_id: str, scope: str):
    unique_assignment_name = (
        "-".join([principal_id, role_definition_id, scope])
        .lower()
        .replace(" ", "")
        .encode("utf-8")
    )
    return authorization.RoleAssignment(
        resource_name=md5(unique_assignment_name).hexdigest(),
        principal_id=principal_id,
        principal_type="Group",
        role_definition_id=role_definition_id,
        scope=scope,
    )


key_vault_default_network_acl = KeyVaultNetworkRuleSetArgs(
    default_action="Allow",
    bypass="AzureServices",
    ip_rules=None,
    virtual_network_rules=None,
)

storage_default_network_acl = StorageNetworkRuleSetArgs(
    default_action="Allow",
    bypass="AzureServices",
    ip_rules=None,
    virtual_network_rules=None,
)
