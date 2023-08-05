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
    'GetNetworkWatcherResult',
    'AwaitableGetNetworkWatcherResult',
    'get_network_watcher',
    'get_network_watcher_output',
]

@pulumi.output_type
class GetNetworkWatcherResult:
    """
    A collection of values returned by getNetworkWatcher.
    """
    def __init__(__self__, id=None, location=None, name=None, resource_group_name=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The supported Azure location where the resource exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

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


class AwaitableGetNetworkWatcherResult(GetNetworkWatcherResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkWatcherResult(
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            tags=self.tags)


def get_network_watcher(name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkWatcherResult:
    """
    Use this data source to access information about an existing Network Watcher.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_network_watcher(name=azurerm_network_watcher["example"]["name"],
        resource_group_name=azurerm_resource_group["example"]["name"])
    pulumi.export("networkWatcherId", example.id)
    ```


    :param str name: Specifies the Name of the Network Watcher.
    :param str resource_group_name: Specifies the Name of the Resource Group within which the Network Watcher exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:network/getNetworkWatcher:getNetworkWatcher', __args__, opts=opts, typ=GetNetworkWatcherResult).value

    return AwaitableGetNetworkWatcherResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_network_watcher)
def get_network_watcher_output(name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworkWatcherResult]:
    """
    Use this data source to access information about an existing Network Watcher.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_network_watcher(name=azurerm_network_watcher["example"]["name"],
        resource_group_name=azurerm_resource_group["example"]["name"])
    pulumi.export("networkWatcherId", example.id)
    ```


    :param str name: Specifies the Name of the Network Watcher.
    :param str resource_group_name: Specifies the Name of the Resource Group within which the Network Watcher exists.
    """
    ...
