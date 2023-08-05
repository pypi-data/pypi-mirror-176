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
    'GetFrontdoorEndpointResult',
    'AwaitableGetFrontdoorEndpointResult',
    'get_frontdoor_endpoint',
    'get_frontdoor_endpoint_output',
]

@pulumi.output_type
class GetFrontdoorEndpointResult:
    """
    A collection of values returned by getFrontdoorEndpoint.
    """
    def __init__(__self__, enabled=None, host_name=None, id=None, name=None, profile_name=None, resource_group_name=None, tags=None):
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if host_name and not isinstance(host_name, str):
            raise TypeError("Expected argument 'host_name' to be a str")
        pulumi.set(__self__, "host_name", host_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if profile_name and not isinstance(profile_name, str):
            raise TypeError("Expected argument 'profile_name' to be a str")
        pulumi.set(__self__, "profile_name", profile_name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Specifies whether this Front Door Endpoint is enabled or not.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> str:
        """
        Specifies the host name of the Front Door Endpoint, in the format `{endpointName}.{dnsZone}` (for example, `contoso.azureedge.net`).
        """
        return pulumi.get(self, "host_name")

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
    @pulumi.getter(name="profileName")
    def profile_name(self) -> str:
        return pulumi.get(self, "profile_name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Specifies a mapping of Tags assigned to this Front Door Endpoint.
        """
        return pulumi.get(self, "tags")


class AwaitableGetFrontdoorEndpointResult(GetFrontdoorEndpointResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFrontdoorEndpointResult(
            enabled=self.enabled,
            host_name=self.host_name,
            id=self.id,
            name=self.name,
            profile_name=self.profile_name,
            resource_group_name=self.resource_group_name,
            tags=self.tags)


def get_frontdoor_endpoint(name: Optional[str] = None,
                           profile_name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFrontdoorEndpointResult:
    """
    Use this data source to access information about an existing Front Door (standard/premium) Endpoint.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.cdn.get_frontdoor_endpoint(name="existing-endpoint",
        profile_name="existing-cdn-profile",
        resource_group_name="existing-resources")
    ```


    :param str name: Specifies the name of the Front Door Endpoint.
    :param str profile_name: The name of the Front Door Profile within which Front Door Endpoint exists.
    :param str resource_group_name: The name of the Resource Group where the Front Door Profile exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['profileName'] = profile_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:cdn/getFrontdoorEndpoint:getFrontdoorEndpoint', __args__, opts=opts, typ=GetFrontdoorEndpointResult).value

    return AwaitableGetFrontdoorEndpointResult(
        enabled=__ret__.enabled,
        host_name=__ret__.host_name,
        id=__ret__.id,
        name=__ret__.name,
        profile_name=__ret__.profile_name,
        resource_group_name=__ret__.resource_group_name,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_frontdoor_endpoint)
def get_frontdoor_endpoint_output(name: Optional[pulumi.Input[str]] = None,
                                  profile_name: Optional[pulumi.Input[str]] = None,
                                  resource_group_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFrontdoorEndpointResult]:
    """
    Use this data source to access information about an existing Front Door (standard/premium) Endpoint.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.cdn.get_frontdoor_endpoint(name="existing-endpoint",
        profile_name="existing-cdn-profile",
        resource_group_name="existing-resources")
    ```


    :param str name: Specifies the name of the Front Door Endpoint.
    :param str profile_name: The name of the Front Door Profile within which Front Door Endpoint exists.
    :param str resource_group_name: The name of the Resource Group where the Front Door Profile exists.
    """
    ...
