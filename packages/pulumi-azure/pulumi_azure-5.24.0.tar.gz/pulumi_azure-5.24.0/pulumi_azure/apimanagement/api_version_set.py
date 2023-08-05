# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ApiVersionSetArgs', 'ApiVersionSet']

@pulumi.input_type
class ApiVersionSetArgs:
    def __init__(__self__, *,
                 api_management_name: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 versioning_scheme: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 version_header_name: Optional[pulumi.Input[str]] = None,
                 version_query_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ApiVersionSet resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service in which the API Version Set should exist. May only contain alphanumeric characters and dashes up to 50 characters in length. Changing this forces a new resource to be created.
        :param pulumi.Input[str] display_name: The display name of this API Version Set.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] versioning_scheme: Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        :param pulumi.Input[str] description: The description of API Version Set.
        :param pulumi.Input[str] name: The name of the API Version Set. May only contain alphanumeric characters and dashes up to 80 characters in length. Changing this forces a new resource to be created.
        :param pulumi.Input[str] version_header_name: The name of the Header which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] version_query_name: The name of the Query String which should be read from Inbound Requests which defines the API Version.
        """
        pulumi.set(__self__, "api_management_name", api_management_name)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "versioning_scheme", versioning_scheme)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if version_header_name is not None:
            pulumi.set(__self__, "version_header_name", version_header_name)
        if version_query_name is not None:
            pulumi.set(__self__, "version_query_name", version_query_name)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management Service in which the API Version Set should exist. May only contain alphanumeric characters and dashes up to 50 characters in length. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_name")

    @api_management_name.setter
    def api_management_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_management_name", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The display name of this API Version Set.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="versioningScheme")
    def versioning_scheme(self) -> pulumi.Input[str]:
        """
        Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        """
        return pulumi.get(self, "versioning_scheme")

    @versioning_scheme.setter
    def versioning_scheme(self, value: pulumi.Input[str]):
        pulumi.set(self, "versioning_scheme", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of API Version Set.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API Version Set. May only contain alphanumeric characters and dashes up to 80 characters in length. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="versionHeaderName")
    def version_header_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Header which should be read from Inbound Requests which defines the API Version.
        """
        return pulumi.get(self, "version_header_name")

    @version_header_name.setter
    def version_header_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_header_name", value)

    @property
    @pulumi.getter(name="versionQueryName")
    def version_query_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Query String which should be read from Inbound Requests which defines the API Version.
        """
        return pulumi.get(self, "version_query_name")

    @version_query_name.setter
    def version_query_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_query_name", value)


@pulumi.input_type
class _ApiVersionSetState:
    def __init__(__self__, *,
                 api_management_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version_header_name: Optional[pulumi.Input[str]] = None,
                 version_query_name: Optional[pulumi.Input[str]] = None,
                 versioning_scheme: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ApiVersionSet resources.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service in which the API Version Set should exist. May only contain alphanumeric characters and dashes up to 50 characters in length. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of API Version Set.
        :param pulumi.Input[str] display_name: The display name of this API Version Set.
        :param pulumi.Input[str] name: The name of the API Version Set. May only contain alphanumeric characters and dashes up to 80 characters in length. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] version_header_name: The name of the Header which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] version_query_name: The name of the Query String which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] versioning_scheme: Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        """
        if api_management_name is not None:
            pulumi.set(__self__, "api_management_name", api_management_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if version_header_name is not None:
            pulumi.set(__self__, "version_header_name", version_header_name)
        if version_query_name is not None:
            pulumi.set(__self__, "version_query_name", version_query_name)
        if versioning_scheme is not None:
            pulumi.set(__self__, "versioning_scheme", versioning_scheme)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API Management Service in which the API Version Set should exist. May only contain alphanumeric characters and dashes up to 50 characters in length. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_name")

    @api_management_name.setter
    def api_management_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_management_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of API Version Set.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name of this API Version Set.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API Version Set. May only contain alphanumeric characters and dashes up to 80 characters in length. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="versionHeaderName")
    def version_header_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Header which should be read from Inbound Requests which defines the API Version.
        """
        return pulumi.get(self, "version_header_name")

    @version_header_name.setter
    def version_header_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_header_name", value)

    @property
    @pulumi.getter(name="versionQueryName")
    def version_query_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Query String which should be read from Inbound Requests which defines the API Version.
        """
        return pulumi.get(self, "version_query_name")

    @version_query_name.setter
    def version_query_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_query_name", value)

    @property
    @pulumi.getter(name="versioningScheme")
    def versioning_scheme(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        """
        return pulumi.get(self, "versioning_scheme")

    @versioning_scheme.setter
    def versioning_scheme(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "versioning_scheme", value)


class ApiVersionSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version_header_name: Optional[pulumi.Input[str]] = None,
                 version_query_name: Optional[pulumi.Input[str]] = None,
                 versioning_scheme: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an API Version Set within an API Management Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="pub1",
            publisher_email="pub1@email.com",
            sku_name="Developer_1")
        example_api_version_set = azure.apimanagement.ApiVersionSet("exampleApiVersionSet",
            resource_group_name=example_resource_group.name,
            api_management_name=example_service.name,
            display_name="ExampleAPIVersionSet",
            versioning_scheme="Segment")
        ```

        ## Import

        API Version Set can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/apiVersionSet:ApiVersionSet example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ApiManagement/service/service1/apiVersionSets/set1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service in which the API Version Set should exist. May only contain alphanumeric characters and dashes up to 50 characters in length. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of API Version Set.
        :param pulumi.Input[str] display_name: The display name of this API Version Set.
        :param pulumi.Input[str] name: The name of the API Version Set. May only contain alphanumeric characters and dashes up to 80 characters in length. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] version_header_name: The name of the Header which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] version_query_name: The name of the Query String which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] versioning_scheme: Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApiVersionSetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an API Version Set within an API Management Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="pub1",
            publisher_email="pub1@email.com",
            sku_name="Developer_1")
        example_api_version_set = azure.apimanagement.ApiVersionSet("exampleApiVersionSet",
            resource_group_name=example_resource_group.name,
            api_management_name=example_service.name,
            display_name="ExampleAPIVersionSet",
            versioning_scheme="Segment")
        ```

        ## Import

        API Version Set can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/apiVersionSet:ApiVersionSet example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ApiManagement/service/service1/apiVersionSets/set1
        ```

        :param str resource_name: The name of the resource.
        :param ApiVersionSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApiVersionSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version_header_name: Optional[pulumi.Input[str]] = None,
                 version_query_name: Optional[pulumi.Input[str]] = None,
                 versioning_scheme: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApiVersionSetArgs.__new__(ApiVersionSetArgs)

            if api_management_name is None and not opts.urn:
                raise TypeError("Missing required property 'api_management_name'")
            __props__.__dict__["api_management_name"] = api_management_name
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["version_header_name"] = version_header_name
            __props__.__dict__["version_query_name"] = version_query_name
            if versioning_scheme is None and not opts.urn:
                raise TypeError("Missing required property 'versioning_scheme'")
            __props__.__dict__["versioning_scheme"] = versioning_scheme
        super(ApiVersionSet, __self__).__init__(
            'azure:apimanagement/apiVersionSet:ApiVersionSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_management_name: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            version_header_name: Optional[pulumi.Input[str]] = None,
            version_query_name: Optional[pulumi.Input[str]] = None,
            versioning_scheme: Optional[pulumi.Input[str]] = None) -> 'ApiVersionSet':
        """
        Get an existing ApiVersionSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service in which the API Version Set should exist. May only contain alphanumeric characters and dashes up to 50 characters in length. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of API Version Set.
        :param pulumi.Input[str] display_name: The display name of this API Version Set.
        :param pulumi.Input[str] name: The name of the API Version Set. May only contain alphanumeric characters and dashes up to 80 characters in length. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] version_header_name: The name of the Header which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] version_query_name: The name of the Query String which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] versioning_scheme: Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ApiVersionSetState.__new__(_ApiVersionSetState)

        __props__.__dict__["api_management_name"] = api_management_name
        __props__.__dict__["description"] = description
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["version_header_name"] = version_header_name
        __props__.__dict__["version_query_name"] = version_query_name
        __props__.__dict__["versioning_scheme"] = versioning_scheme
        return ApiVersionSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> pulumi.Output[str]:
        """
        The name of the API Management Service in which the API Version Set should exist. May only contain alphanumeric characters and dashes up to 50 characters in length. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of API Version Set.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name of this API Version Set.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the API Version Set. May only contain alphanumeric characters and dashes up to 80 characters in length. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="versionHeaderName")
    def version_header_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Header which should be read from Inbound Requests which defines the API Version.
        """
        return pulumi.get(self, "version_header_name")

    @property
    @pulumi.getter(name="versionQueryName")
    def version_query_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Query String which should be read from Inbound Requests which defines the API Version.
        """
        return pulumi.get(self, "version_query_name")

    @property
    @pulumi.getter(name="versioningScheme")
    def versioning_scheme(self) -> pulumi.Output[str]:
        """
        Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        """
        return pulumi.get(self, "versioning_scheme")

