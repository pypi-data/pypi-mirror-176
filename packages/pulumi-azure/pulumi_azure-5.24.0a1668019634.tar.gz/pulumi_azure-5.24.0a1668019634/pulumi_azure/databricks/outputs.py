# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'AccessConnectorIdentity',
    'WorkspaceCustomParameters',
    'WorkspaceStorageAccountIdentity',
    'GetWorkspacePrivateEndpointConnectionConnectionResult',
]

@pulumi.output_type
class AccessConnectorIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessConnectorIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessConnectorIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessConnectorIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        pulumi.set(__self__, "type", type)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class WorkspaceCustomParameters(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "machineLearningWorkspaceId":
            suggest = "machine_learning_workspace_id"
        elif key == "natGatewayName":
            suggest = "nat_gateway_name"
        elif key == "noPublicIp":
            suggest = "no_public_ip"
        elif key == "privateSubnetName":
            suggest = "private_subnet_name"
        elif key == "privateSubnetNetworkSecurityGroupAssociationId":
            suggest = "private_subnet_network_security_group_association_id"
        elif key == "publicIpName":
            suggest = "public_ip_name"
        elif key == "publicSubnetName":
            suggest = "public_subnet_name"
        elif key == "publicSubnetNetworkSecurityGroupAssociationId":
            suggest = "public_subnet_network_security_group_association_id"
        elif key == "storageAccountName":
            suggest = "storage_account_name"
        elif key == "storageAccountSkuName":
            suggest = "storage_account_sku_name"
        elif key == "virtualNetworkId":
            suggest = "virtual_network_id"
        elif key == "vnetAddressPrefix":
            suggest = "vnet_address_prefix"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceCustomParameters. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceCustomParameters.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceCustomParameters.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 machine_learning_workspace_id: Optional[str] = None,
                 nat_gateway_name: Optional[str] = None,
                 no_public_ip: Optional[bool] = None,
                 private_subnet_name: Optional[str] = None,
                 private_subnet_network_security_group_association_id: Optional[str] = None,
                 public_ip_name: Optional[str] = None,
                 public_subnet_name: Optional[str] = None,
                 public_subnet_network_security_group_association_id: Optional[str] = None,
                 storage_account_name: Optional[str] = None,
                 storage_account_sku_name: Optional[str] = None,
                 virtual_network_id: Optional[str] = None,
                 vnet_address_prefix: Optional[str] = None):
        """
        :param str machine_learning_workspace_id: The ID of a Azure Machine Learning workspace to link with Databricks workspace. Changing this forces a new resource to be created.
        :param str nat_gateway_name: Name of the NAT gateway for Secure Cluster Connectivity (No Public IP) workspace subnets. Defaults to `nat-gateway`. Changing this forces a new resource to be created.
        :param bool no_public_ip: Are public IP Addresses not allowed? Possible values are `true` or `false`. Defaults to `false`. Changing this forces a new resource to be created.
        :param str private_subnet_name: The name of the Private Subnet within the Virtual Network. Required if `virtual_network_id` is set. Changing this forces a new resource to be created.
        :param str private_subnet_network_security_group_association_id: The resource ID of the `network.SubnetNetworkSecurityGroupAssociation` resource which is referred to by the `private_subnet_name` field. This is the same as the ID of the subnet referred to by the `private_subnet_name` field. Required if `virtual_network_id` is set.
        :param str public_ip_name: Name of the Public IP for No Public IP workspace with managed vNet. Defaults to `nat-gw-public-ip`. Changing this forces a new resource to be created.
        :param str public_subnet_name: The name of the Public Subnet within the Virtual Network. Required if `virtual_network_id` is set. Changing this forces a new resource to be created.
        :param str public_subnet_network_security_group_association_id: The resource ID of the `network.SubnetNetworkSecurityGroupAssociation` resource which is referred to by the `public_subnet_name` field. This is the same as the ID of the subnet referred to by the `public_subnet_name` field. Required if `virtual_network_id` is set.
        :param str storage_account_name: Default Databricks File Storage account name. Defaults to a randomized name(e.g. `dbstoragel6mfeghoe5kxu`). Changing this forces a new resource to be created.
        :param str storage_account_sku_name: Storage account SKU name. Possible values include `Standard_LRS`, `Standard_GRS`, `Standard_RAGRS`, `Standard_GZRS`, `Standard_RAGZRS`, `Standard_ZRS`, `Premium_LRS` or `Premium_ZRS`. Defaults to `Standard_GRS`. Changing this forces a new resource to be created.
        :param str virtual_network_id: The ID of a Virtual Network where this Databricks Cluster should be created. Changing this forces a new resource to be created.
        :param str vnet_address_prefix: Address prefix for Managed virtual network. Defaults to `10.139`. Changing this forces a new resource to be created.
        """
        if machine_learning_workspace_id is not None:
            pulumi.set(__self__, "machine_learning_workspace_id", machine_learning_workspace_id)
        if nat_gateway_name is not None:
            pulumi.set(__self__, "nat_gateway_name", nat_gateway_name)
        if no_public_ip is not None:
            pulumi.set(__self__, "no_public_ip", no_public_ip)
        if private_subnet_name is not None:
            pulumi.set(__self__, "private_subnet_name", private_subnet_name)
        if private_subnet_network_security_group_association_id is not None:
            pulumi.set(__self__, "private_subnet_network_security_group_association_id", private_subnet_network_security_group_association_id)
        if public_ip_name is not None:
            pulumi.set(__self__, "public_ip_name", public_ip_name)
        if public_subnet_name is not None:
            pulumi.set(__self__, "public_subnet_name", public_subnet_name)
        if public_subnet_network_security_group_association_id is not None:
            pulumi.set(__self__, "public_subnet_network_security_group_association_id", public_subnet_network_security_group_association_id)
        if storage_account_name is not None:
            pulumi.set(__self__, "storage_account_name", storage_account_name)
        if storage_account_sku_name is not None:
            pulumi.set(__self__, "storage_account_sku_name", storage_account_sku_name)
        if virtual_network_id is not None:
            pulumi.set(__self__, "virtual_network_id", virtual_network_id)
        if vnet_address_prefix is not None:
            pulumi.set(__self__, "vnet_address_prefix", vnet_address_prefix)

    @property
    @pulumi.getter(name="machineLearningWorkspaceId")
    def machine_learning_workspace_id(self) -> Optional[str]:
        """
        The ID of a Azure Machine Learning workspace to link with Databricks workspace. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "machine_learning_workspace_id")

    @property
    @pulumi.getter(name="natGatewayName")
    def nat_gateway_name(self) -> Optional[str]:
        """
        Name of the NAT gateway for Secure Cluster Connectivity (No Public IP) workspace subnets. Defaults to `nat-gateway`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "nat_gateway_name")

    @property
    @pulumi.getter(name="noPublicIp")
    def no_public_ip(self) -> Optional[bool]:
        """
        Are public IP Addresses not allowed? Possible values are `true` or `false`. Defaults to `false`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "no_public_ip")

    @property
    @pulumi.getter(name="privateSubnetName")
    def private_subnet_name(self) -> Optional[str]:
        """
        The name of the Private Subnet within the Virtual Network. Required if `virtual_network_id` is set. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "private_subnet_name")

    @property
    @pulumi.getter(name="privateSubnetNetworkSecurityGroupAssociationId")
    def private_subnet_network_security_group_association_id(self) -> Optional[str]:
        """
        The resource ID of the `network.SubnetNetworkSecurityGroupAssociation` resource which is referred to by the `private_subnet_name` field. This is the same as the ID of the subnet referred to by the `private_subnet_name` field. Required if `virtual_network_id` is set.
        """
        return pulumi.get(self, "private_subnet_network_security_group_association_id")

    @property
    @pulumi.getter(name="publicIpName")
    def public_ip_name(self) -> Optional[str]:
        """
        Name of the Public IP for No Public IP workspace with managed vNet. Defaults to `nat-gw-public-ip`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "public_ip_name")

    @property
    @pulumi.getter(name="publicSubnetName")
    def public_subnet_name(self) -> Optional[str]:
        """
        The name of the Public Subnet within the Virtual Network. Required if `virtual_network_id` is set. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "public_subnet_name")

    @property
    @pulumi.getter(name="publicSubnetNetworkSecurityGroupAssociationId")
    def public_subnet_network_security_group_association_id(self) -> Optional[str]:
        """
        The resource ID of the `network.SubnetNetworkSecurityGroupAssociation` resource which is referred to by the `public_subnet_name` field. This is the same as the ID of the subnet referred to by the `public_subnet_name` field. Required if `virtual_network_id` is set.
        """
        return pulumi.get(self, "public_subnet_network_security_group_association_id")

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> Optional[str]:
        """
        Default Databricks File Storage account name. Defaults to a randomized name(e.g. `dbstoragel6mfeghoe5kxu`). Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "storage_account_name")

    @property
    @pulumi.getter(name="storageAccountSkuName")
    def storage_account_sku_name(self) -> Optional[str]:
        """
        Storage account SKU name. Possible values include `Standard_LRS`, `Standard_GRS`, `Standard_RAGRS`, `Standard_GZRS`, `Standard_RAGZRS`, `Standard_ZRS`, `Premium_LRS` or `Premium_ZRS`. Defaults to `Standard_GRS`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "storage_account_sku_name")

    @property
    @pulumi.getter(name="virtualNetworkId")
    def virtual_network_id(self) -> Optional[str]:
        """
        The ID of a Virtual Network where this Databricks Cluster should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_network_id")

    @property
    @pulumi.getter(name="vnetAddressPrefix")
    def vnet_address_prefix(self) -> Optional[str]:
        """
        Address prefix for Managed virtual network. Defaults to `10.139`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "vnet_address_prefix")


@pulumi.output_type
class WorkspaceStorageAccountIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceStorageAccountIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceStorageAccountIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceStorageAccountIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None,
                 type: Optional[str] = None):
        """
        :param str principal_id: The principal UUID for the internal databricks storage account needed to provide access to the workspace for enabling Customer Managed Keys.
        :param str tenant_id: The UUID of the tenant where the internal databricks storage account was created.
        :param str type: The type of the internal databricks storage account.
        """
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        """
        The principal UUID for the internal databricks storage account needed to provide access to the workspace for enabling Customer Managed Keys.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The UUID of the tenant where the internal databricks storage account was created.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the internal databricks storage account.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class GetWorkspacePrivateEndpointConnectionConnectionResult(dict):
    def __init__(__self__, *,
                 action_required: str,
                 description: str,
                 name: str,
                 status: str,
                 workspace_private_endpoint_id: str):
        """
        :param str action_required: Actions required for a private endpoint connection.
        :param str description: The description for the current state of a private endpoint connection.
        :param str name: The name of the Databricks Workspace.
        :param str status: The status of a private endpoint connection. Possible values are `Pending`, `Approved`, `Rejected` or `Disconnected`.
        :param str workspace_private_endpoint_id: The Databricks Workspace resource ID for the private link endpoint.
        """
        pulumi.set(__self__, "action_required", action_required)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "workspace_private_endpoint_id", workspace_private_endpoint_id)

    @property
    @pulumi.getter(name="actionRequired")
    def action_required(self) -> str:
        """
        Actions required for a private endpoint connection.
        """
        return pulumi.get(self, "action_required")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description for the current state of a private endpoint connection.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Databricks Workspace.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of a private endpoint connection. Possible values are `Pending`, `Approved`, `Rejected` or `Disconnected`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="workspacePrivateEndpointId")
    def workspace_private_endpoint_id(self) -> str:
        """
        The Databricks Workspace resource ID for the private link endpoint.
        """
        return pulumi.get(self, "workspace_private_endpoint_id")


