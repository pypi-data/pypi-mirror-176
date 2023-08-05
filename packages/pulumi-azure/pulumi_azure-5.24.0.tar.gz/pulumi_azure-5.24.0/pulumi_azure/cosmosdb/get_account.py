# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetAccountResult',
    'AwaitableGetAccountResult',
    'get_account',
    'get_account_output',
]

@pulumi.output_type
class GetAccountResult:
    """
    A collection of values returned by getAccount.
    """
    def __init__(__self__, capabilities=None, consistency_policies=None, enable_automatic_failover=None, enable_free_tier=None, enable_multiple_write_locations=None, endpoint=None, geo_locations=None, id=None, ip_range_filter=None, is_virtual_network_filter_enabled=None, key_vault_key_id=None, kind=None, location=None, name=None, offer_type=None, primary_key=None, primary_readonly_key=None, read_endpoints=None, resource_group_name=None, secondary_key=None, secondary_readonly_key=None, tags=None, virtual_network_rules=None, write_endpoints=None):
        if capabilities and not isinstance(capabilities, list):
            raise TypeError("Expected argument 'capabilities' to be a list")
        pulumi.set(__self__, "capabilities", capabilities)
        if consistency_policies and not isinstance(consistency_policies, list):
            raise TypeError("Expected argument 'consistency_policies' to be a list")
        pulumi.set(__self__, "consistency_policies", consistency_policies)
        if enable_automatic_failover and not isinstance(enable_automatic_failover, bool):
            raise TypeError("Expected argument 'enable_automatic_failover' to be a bool")
        pulumi.set(__self__, "enable_automatic_failover", enable_automatic_failover)
        if enable_free_tier and not isinstance(enable_free_tier, bool):
            raise TypeError("Expected argument 'enable_free_tier' to be a bool")
        pulumi.set(__self__, "enable_free_tier", enable_free_tier)
        if enable_multiple_write_locations and not isinstance(enable_multiple_write_locations, bool):
            raise TypeError("Expected argument 'enable_multiple_write_locations' to be a bool")
        pulumi.set(__self__, "enable_multiple_write_locations", enable_multiple_write_locations)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if geo_locations and not isinstance(geo_locations, list):
            raise TypeError("Expected argument 'geo_locations' to be a list")
        pulumi.set(__self__, "geo_locations", geo_locations)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_range_filter and not isinstance(ip_range_filter, str):
            raise TypeError("Expected argument 'ip_range_filter' to be a str")
        pulumi.set(__self__, "ip_range_filter", ip_range_filter)
        if is_virtual_network_filter_enabled and not isinstance(is_virtual_network_filter_enabled, bool):
            raise TypeError("Expected argument 'is_virtual_network_filter_enabled' to be a bool")
        pulumi.set(__self__, "is_virtual_network_filter_enabled", is_virtual_network_filter_enabled)
        if key_vault_key_id and not isinstance(key_vault_key_id, str):
            raise TypeError("Expected argument 'key_vault_key_id' to be a str")
        pulumi.set(__self__, "key_vault_key_id", key_vault_key_id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if offer_type and not isinstance(offer_type, str):
            raise TypeError("Expected argument 'offer_type' to be a str")
        pulumi.set(__self__, "offer_type", offer_type)
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, "primary_key", primary_key)
        if primary_readonly_key and not isinstance(primary_readonly_key, str):
            raise TypeError("Expected argument 'primary_readonly_key' to be a str")
        pulumi.set(__self__, "primary_readonly_key", primary_readonly_key)
        if read_endpoints and not isinstance(read_endpoints, list):
            raise TypeError("Expected argument 'read_endpoints' to be a list")
        pulumi.set(__self__, "read_endpoints", read_endpoints)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, "secondary_key", secondary_key)
        if secondary_readonly_key and not isinstance(secondary_readonly_key, str):
            raise TypeError("Expected argument 'secondary_readonly_key' to be a str")
        pulumi.set(__self__, "secondary_readonly_key", secondary_readonly_key)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if virtual_network_rules and not isinstance(virtual_network_rules, list):
            raise TypeError("Expected argument 'virtual_network_rules' to be a list")
        pulumi.set(__self__, "virtual_network_rules", virtual_network_rules)
        if write_endpoints and not isinstance(write_endpoints, list):
            raise TypeError("Expected argument 'write_endpoints' to be a list")
        pulumi.set(__self__, "write_endpoints", write_endpoints)

    @property
    @pulumi.getter
    def capabilities(self) -> Sequence['outputs.GetAccountCapabilityResult']:
        """
        Capabilities enabled on this Cosmos DB account.
        """
        return pulumi.get(self, "capabilities")

    @property
    @pulumi.getter(name="consistencyPolicies")
    def consistency_policies(self) -> Sequence['outputs.GetAccountConsistencyPolicyResult']:
        return pulumi.get(self, "consistency_policies")

    @property
    @pulumi.getter(name="enableAutomaticFailover")
    def enable_automatic_failover(self) -> bool:
        """
        If automatic failover is enabled for this CosmosDB Account.
        """
        return pulumi.get(self, "enable_automatic_failover")

    @property
    @pulumi.getter(name="enableFreeTier")
    def enable_free_tier(self) -> bool:
        """
        If Free Tier pricing option is enabled for this CosmosDB Account. You can have up to one free tier Azure Cosmos DB account per Azure subscription.
        """
        return pulumi.get(self, "enable_free_tier")

    @property
    @pulumi.getter(name="enableMultipleWriteLocations")
    def enable_multiple_write_locations(self) -> bool:
        """
        If multiple write locations are enabled for this Cosmos DB account.
        """
        return pulumi.get(self, "enable_multiple_write_locations")

    @property
    @pulumi.getter
    def endpoint(self) -> str:
        """
        The endpoint used to connect to the CosmosDB account.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="geoLocations")
    def geo_locations(self) -> Sequence['outputs.GetAccountGeoLocationResult']:
        return pulumi.get(self, "geo_locations")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipRangeFilter")
    def ip_range_filter(self) -> str:
        """
        The current IP Filter for this CosmosDB account
        """
        return pulumi.get(self, "ip_range_filter")

    @property
    @pulumi.getter(name="isVirtualNetworkFilterEnabled")
    def is_virtual_network_filter_enabled(self) -> bool:
        """
        If virtual network filtering is enabled for this Cosmos DB account.
        """
        return pulumi.get(self, "is_virtual_network_filter_enabled")

    @property
    @pulumi.getter(name="keyVaultKeyId")
    def key_vault_key_id(self) -> str:
        """
        The Key Vault key URI for CMK encryption.
        """
        return pulumi.get(self, "key_vault_key_id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The Kind of the CosmosDB account.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The name of the Azure region hosting replicated data.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="offerType")
    def offer_type(self) -> str:
        """
        The Offer Type to used by this CosmosDB Account.
        """
        return pulumi.get(self, "offer_type")

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> str:
        """
        The primary key for the CosmosDB account.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="primaryReadonlyKey")
    def primary_readonly_key(self) -> str:
        """
        The primary read-only Key for the CosmosDB account.
        """
        return pulumi.get(self, "primary_readonly_key")

    @property
    @pulumi.getter(name="readEndpoints")
    def read_endpoints(self) -> Sequence[str]:
        """
        A list of read endpoints available for this CosmosDB account.
        """
        return pulumi.get(self, "read_endpoints")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> str:
        """
        The secondary key for the CosmosDB account.
        """
        return pulumi.get(self, "secondary_key")

    @property
    @pulumi.getter(name="secondaryReadonlyKey")
    def secondary_readonly_key(self) -> str:
        """
        The secondary read-only key for the CosmosDB account.
        """
        return pulumi.get(self, "secondary_readonly_key")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="virtualNetworkRules")
    def virtual_network_rules(self) -> Sequence['outputs.GetAccountVirtualNetworkRuleResult']:
        """
        Subnets that are allowed to access this CosmosDB account.
        """
        return pulumi.get(self, "virtual_network_rules")

    @property
    @pulumi.getter(name="writeEndpoints")
    def write_endpoints(self) -> Sequence[str]:
        """
        A list of write endpoints available for this CosmosDB account.
        """
        return pulumi.get(self, "write_endpoints")


class AwaitableGetAccountResult(GetAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountResult(
            capabilities=self.capabilities,
            consistency_policies=self.consistency_policies,
            enable_automatic_failover=self.enable_automatic_failover,
            enable_free_tier=self.enable_free_tier,
            enable_multiple_write_locations=self.enable_multiple_write_locations,
            endpoint=self.endpoint,
            geo_locations=self.geo_locations,
            id=self.id,
            ip_range_filter=self.ip_range_filter,
            is_virtual_network_filter_enabled=self.is_virtual_network_filter_enabled,
            key_vault_key_id=self.key_vault_key_id,
            kind=self.kind,
            location=self.location,
            name=self.name,
            offer_type=self.offer_type,
            primary_key=self.primary_key,
            primary_readonly_key=self.primary_readonly_key,
            read_endpoints=self.read_endpoints,
            resource_group_name=self.resource_group_name,
            secondary_key=self.secondary_key,
            secondary_readonly_key=self.secondary_readonly_key,
            tags=self.tags,
            virtual_network_rules=self.virtual_network_rules,
            write_endpoints=self.write_endpoints)


def get_account(name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccountResult:
    """
    Use this data source to access information about an existing CosmosDB (formally DocumentDB) Account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.cosmosdb.get_account(name="tfex-cosmosdb-account",
        resource_group_name="tfex-cosmosdb-account-rg")
    pulumi.export("cosmosdbAccountEndpoint", example.endpoint)
    ```


    :param str name: Specifies the name of the CosmosDB Account.
    :param str resource_group_name: Specifies the name of the resource group in which the CosmosDB Account resides.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:cosmosdb/getAccount:getAccount', __args__, opts=opts, typ=GetAccountResult).value

    return AwaitableGetAccountResult(
        capabilities=__ret__.capabilities,
        consistency_policies=__ret__.consistency_policies,
        enable_automatic_failover=__ret__.enable_automatic_failover,
        enable_free_tier=__ret__.enable_free_tier,
        enable_multiple_write_locations=__ret__.enable_multiple_write_locations,
        endpoint=__ret__.endpoint,
        geo_locations=__ret__.geo_locations,
        id=__ret__.id,
        ip_range_filter=__ret__.ip_range_filter,
        is_virtual_network_filter_enabled=__ret__.is_virtual_network_filter_enabled,
        key_vault_key_id=__ret__.key_vault_key_id,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        offer_type=__ret__.offer_type,
        primary_key=__ret__.primary_key,
        primary_readonly_key=__ret__.primary_readonly_key,
        read_endpoints=__ret__.read_endpoints,
        resource_group_name=__ret__.resource_group_name,
        secondary_key=__ret__.secondary_key,
        secondary_readonly_key=__ret__.secondary_readonly_key,
        tags=__ret__.tags,
        virtual_network_rules=__ret__.virtual_network_rules,
        write_endpoints=__ret__.write_endpoints)


@_utilities.lift_output_func(get_account)
def get_account_output(name: Optional[pulumi.Input[str]] = None,
                       resource_group_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccountResult]:
    """
    Use this data source to access information about an existing CosmosDB (formally DocumentDB) Account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.cosmosdb.get_account(name="tfex-cosmosdb-account",
        resource_group_name="tfex-cosmosdb-account-rg")
    pulumi.export("cosmosdbAccountEndpoint", example.endpoint)
    ```


    :param str name: Specifies the name of the CosmosDB Account.
    :param str resource_group_name: Specifies the name of the resource group in which the CosmosDB Account resides.
    """
    ...
