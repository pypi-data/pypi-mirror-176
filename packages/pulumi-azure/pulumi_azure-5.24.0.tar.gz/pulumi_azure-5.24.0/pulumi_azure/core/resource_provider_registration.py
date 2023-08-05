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
from ._inputs import *

__all__ = ['ResourceProviderRegistrationArgs', 'ResourceProviderRegistration']

@pulumi.input_type
class ResourceProviderRegistrationArgs:
    def __init__(__self__, *,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceProviderRegistrationFeatureArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ResourceProviderRegistration resource.
        :param pulumi.Input[Sequence[pulumi.Input['ResourceProviderRegistrationFeatureArgs']]] features: A list of `feature` blocks as defined below.
        :param pulumi.Input[str] name: The namespace of the Resource Provider which should be registered. Changing this forces a new resource to be created.
        """
        if features is not None:
            pulumi.set(__self__, "features", features)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ResourceProviderRegistrationFeatureArgs']]]]:
        """
        A list of `feature` blocks as defined below.
        """
        return pulumi.get(self, "features")

    @features.setter
    def features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceProviderRegistrationFeatureArgs']]]]):
        pulumi.set(self, "features", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace of the Resource Provider which should be registered. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ResourceProviderRegistrationState:
    def __init__(__self__, *,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceProviderRegistrationFeatureArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ResourceProviderRegistration resources.
        :param pulumi.Input[Sequence[pulumi.Input['ResourceProviderRegistrationFeatureArgs']]] features: A list of `feature` blocks as defined below.
        :param pulumi.Input[str] name: The namespace of the Resource Provider which should be registered. Changing this forces a new resource to be created.
        """
        if features is not None:
            pulumi.set(__self__, "features", features)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ResourceProviderRegistrationFeatureArgs']]]]:
        """
        A list of `feature` blocks as defined below.
        """
        return pulumi.get(self, "features")

    @features.setter
    def features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceProviderRegistrationFeatureArgs']]]]):
        pulumi.set(self, "features", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace of the Resource Provider which should be registered. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class ResourceProviderRegistration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceProviderRegistrationFeatureArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages the registration of a Resource Provider - which allows access to the API's supported by this Resource Provider.

        > The Azure Provider will automatically register all of the Resource Providers which it supports on launch (unless opted-out using the `skip_provider_registration` field within the provider block).

        !> **Note:** The errors returned from the Azure API when a Resource Provider is unregistered are unclear (example `API version '2019-01-01' was not found for 'Microsoft.Foo'`) - please ensure that all of the necessary Resource Providers you're using are registered - if in doubt **we strongly recommend letting the provider register these for you**.

        > **Note:** Adding or Removing a Preview Feature will re-register the Resource Provider.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceProviderRegistration("example")
        ```
        ### Registering A Preview Feature)

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceProviderRegistration("example", features=[azure.core.ResourceProviderRegistrationFeatureArgs(
            name="AKS-DataPlaneAutoApprove",
            registered=True,
        )])
        ```

        ## Import

        Resource Provider Registrations can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:core/resourceProviderRegistration:ResourceProviderRegistration example /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.PolicyInsights
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceProviderRegistrationFeatureArgs']]]] features: A list of `feature` blocks as defined below.
        :param pulumi.Input[str] name: The namespace of the Resource Provider which should be registered. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ResourceProviderRegistrationArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the registration of a Resource Provider - which allows access to the API's supported by this Resource Provider.

        > The Azure Provider will automatically register all of the Resource Providers which it supports on launch (unless opted-out using the `skip_provider_registration` field within the provider block).

        !> **Note:** The errors returned from the Azure API when a Resource Provider is unregistered are unclear (example `API version '2019-01-01' was not found for 'Microsoft.Foo'`) - please ensure that all of the necessary Resource Providers you're using are registered - if in doubt **we strongly recommend letting the provider register these for you**.

        > **Note:** Adding or Removing a Preview Feature will re-register the Resource Provider.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceProviderRegistration("example")
        ```
        ### Registering A Preview Feature)

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceProviderRegistration("example", features=[azure.core.ResourceProviderRegistrationFeatureArgs(
            name="AKS-DataPlaneAutoApprove",
            registered=True,
        )])
        ```

        ## Import

        Resource Provider Registrations can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:core/resourceProviderRegistration:ResourceProviderRegistration example /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.PolicyInsights
        ```

        :param str resource_name: The name of the resource.
        :param ResourceProviderRegistrationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceProviderRegistrationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceProviderRegistrationFeatureArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceProviderRegistrationArgs.__new__(ResourceProviderRegistrationArgs)

            __props__.__dict__["features"] = features
            __props__.__dict__["name"] = name
        super(ResourceProviderRegistration, __self__).__init__(
            'azure:core/resourceProviderRegistration:ResourceProviderRegistration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceProviderRegistrationFeatureArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'ResourceProviderRegistration':
        """
        Get an existing ResourceProviderRegistration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceProviderRegistrationFeatureArgs']]]] features: A list of `feature` blocks as defined below.
        :param pulumi.Input[str] name: The namespace of the Resource Provider which should be registered. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceProviderRegistrationState.__new__(_ResourceProviderRegistrationState)

        __props__.__dict__["features"] = features
        __props__.__dict__["name"] = name
        return ResourceProviderRegistration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def features(self) -> pulumi.Output[Optional[Sequence['outputs.ResourceProviderRegistrationFeature']]]:
        """
        A list of `feature` blocks as defined below.
        """
        return pulumi.get(self, "features")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The namespace of the Resource Provider which should be registered. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

