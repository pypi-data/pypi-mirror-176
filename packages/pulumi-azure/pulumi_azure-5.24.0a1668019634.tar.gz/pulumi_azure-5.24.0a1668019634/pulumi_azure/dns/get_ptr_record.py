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
    'GetPtrRecordResult',
    'AwaitableGetPtrRecordResult',
    'get_ptr_record',
    'get_ptr_record_output',
]

@pulumi.output_type
class GetPtrRecordResult:
    """
    A collection of values returned by getPtrRecord.
    """
    def __init__(__self__, fqdn=None, id=None, name=None, records=None, resource_group_name=None, tags=None, ttl=None, zone_name=None):
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if records and not isinstance(records, list):
            raise TypeError("Expected argument 'records' to be a list")
        pulumi.set(__self__, "records", records)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if ttl and not isinstance(ttl, int):
            raise TypeError("Expected argument 'ttl' to be a int")
        pulumi.set(__self__, "ttl", ttl)
        if zone_name and not isinstance(zone_name, str):
            raise TypeError("Expected argument 'zone_name' to be a str")
        pulumi.set(__self__, "zone_name", zone_name)

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        The FQDN of the DNS PTR Record.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def records(self) -> Sequence[str]:
        """
        List of Fully Qualified Domain Names.
        """
        return pulumi.get(self, "records")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def ttl(self) -> int:
        """
        The Time To Live (TTL) of the DNS record in seconds.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter(name="zoneName")
    def zone_name(self) -> str:
        return pulumi.get(self, "zone_name")


class AwaitableGetPtrRecordResult(GetPtrRecordResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPtrRecordResult(
            fqdn=self.fqdn,
            id=self.id,
            name=self.name,
            records=self.records,
            resource_group_name=self.resource_group_name,
            tags=self.tags,
            ttl=self.ttl,
            zone_name=self.zone_name)


def get_ptr_record(name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   zone_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPtrRecordResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.dns.PtrRecord("example",
        zone_name="test-zone",
        resource_group_name="test-rg")
    pulumi.export("dnsPtrRecordId", example.id)
    ```


    :param str name: The name of the DNS PTR Record.
    :param str resource_group_name: Specifies the resource group where the DNS Zone (parent resource) exists.
    :param str zone_name: Specifies the DNS Zone where the resource exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['zoneName'] = zone_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:dns/getPtrRecord:getPtrRecord', __args__, opts=opts, typ=GetPtrRecordResult).value

    return AwaitableGetPtrRecordResult(
        fqdn=__ret__.fqdn,
        id=__ret__.id,
        name=__ret__.name,
        records=__ret__.records,
        resource_group_name=__ret__.resource_group_name,
        tags=__ret__.tags,
        ttl=__ret__.ttl,
        zone_name=__ret__.zone_name)


@_utilities.lift_output_func(get_ptr_record)
def get_ptr_record_output(name: Optional[pulumi.Input[str]] = None,
                          resource_group_name: Optional[pulumi.Input[str]] = None,
                          zone_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPtrRecordResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.dns.PtrRecord("example",
        zone_name="test-zone",
        resource_group_name="test-rg")
    pulumi.export("dnsPtrRecordId", example.id)
    ```


    :param str name: The name of the DNS PTR Record.
    :param str resource_group_name: Specifies the resource group where the DNS Zone (parent resource) exists.
    :param str zone_name: Specifies the DNS Zone where the resource exists.
    """
    ...
