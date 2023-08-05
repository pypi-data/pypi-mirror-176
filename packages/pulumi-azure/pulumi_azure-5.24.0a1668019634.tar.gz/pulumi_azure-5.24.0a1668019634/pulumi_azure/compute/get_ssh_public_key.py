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
    'GetSshPublicKeyResult',
    'AwaitableGetSshPublicKeyResult',
    'get_ssh_public_key',
    'get_ssh_public_key_output',
]

@pulumi.output_type
class GetSshPublicKeyResult:
    """
    A collection of values returned by getSshPublicKey.
    """
    def __init__(__self__, id=None, name=None, public_key=None, resource_group_name=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if public_key and not isinstance(public_key, str):
            raise TypeError("Expected argument 'public_key' to be a str")
        pulumi.set(__self__, "public_key", public_key)
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
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> str:
        """
        The SSH public key used to authenticate to a virtual machine through ssh.
        """
        return pulumi.get(self, "public_key")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "tags")


class AwaitableGetSshPublicKeyResult(GetSshPublicKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSshPublicKeyResult(
            id=self.id,
            name=self.name,
            public_key=self.public_key,
            resource_group_name=self.resource_group_name,
            tags=self.tags)


def get_ssh_public_key(name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       tags: Optional[Mapping[str, str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSshPublicKeyResult:
    """
    Use this data source to access information about an existing SSH Public Key.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_ssh_public_key(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this SSH Public Key.
    :param str resource_group_name: The name of the Resource Group where the SSH Public Key exists.
    :param Mapping[str, str] tags: A mapping of tags which should be assigned to the SSH Public Key.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:compute/getSshPublicKey:getSshPublicKey', __args__, opts=opts, typ=GetSshPublicKeyResult).value

    return AwaitableGetSshPublicKeyResult(
        id=__ret__.id,
        name=__ret__.name,
        public_key=__ret__.public_key,
        resource_group_name=__ret__.resource_group_name,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_ssh_public_key)
def get_ssh_public_key_output(name: Optional[pulumi.Input[str]] = None,
                              resource_group_name: Optional[pulumi.Input[str]] = None,
                              tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSshPublicKeyResult]:
    """
    Use this data source to access information about an existing SSH Public Key.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_ssh_public_key(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this SSH Public Key.
    :param str resource_group_name: The name of the Resource Group where the SSH Public Key exists.
    :param Mapping[str, str] tags: A mapping of tags which should be assigned to the SSH Public Key.
    """
    ...
