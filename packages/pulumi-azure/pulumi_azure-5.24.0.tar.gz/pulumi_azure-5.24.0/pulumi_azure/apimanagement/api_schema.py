# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ApiSchemaArgs', 'ApiSchema']

@pulumi.input_type
class ApiSchemaArgs:
    def __init__(__self__, *,
                 api_management_name: pulumi.Input[str],
                 api_name: pulumi.Input[str],
                 content_type: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 schema_id: pulumi.Input[str],
                 components: Optional[pulumi.Input[str]] = None,
                 definitions: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ApiSchema resource.
        :param pulumi.Input[str] api_management_name: The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] api_name: The name of the API within the API Management Service where this API Schema should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] content_type: The content type of the API Schema.
        :param pulumi.Input[str] resource_group_name: The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] schema_id: A unique identifier for this API Schema. Changing this forces a new resource to be created.
        :param pulumi.Input[str] components: Types definitions. Used for Swagger/OpenAPI v2/v3 schemas only.
        :param pulumi.Input[str] definitions: Types definitions. Used for Swagger/OpenAPI v1 schemas only.
        :param pulumi.Input[str] value: The JSON escaped string defining the document representing the Schema.
        """
        pulumi.set(__self__, "api_management_name", api_management_name)
        pulumi.set(__self__, "api_name", api_name)
        pulumi.set(__self__, "content_type", content_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "schema_id", schema_id)
        if components is not None:
            pulumi.set(__self__, "components", components)
        if definitions is not None:
            pulumi.set(__self__, "definitions", definitions)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> pulumi.Input[str]:
        """
        The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_name")

    @api_management_name.setter
    def api_management_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_management_name", value)

    @property
    @pulumi.getter(name="apiName")
    def api_name(self) -> pulumi.Input[str]:
        """
        The name of the API within the API Management Service where this API Schema should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_name")

    @api_name.setter
    def api_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_name", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> pulumi.Input[str]:
        """
        The content type of the API Schema.
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="schemaId")
    def schema_id(self) -> pulumi.Input[str]:
        """
        A unique identifier for this API Schema. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "schema_id")

    @schema_id.setter
    def schema_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "schema_id", value)

    @property
    @pulumi.getter
    def components(self) -> Optional[pulumi.Input[str]]:
        """
        Types definitions. Used for Swagger/OpenAPI v2/v3 schemas only.
        """
        return pulumi.get(self, "components")

    @components.setter
    def components(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "components", value)

    @property
    @pulumi.getter
    def definitions(self) -> Optional[pulumi.Input[str]]:
        """
        Types definitions. Used for Swagger/OpenAPI v1 schemas only.
        """
        return pulumi.get(self, "definitions")

    @definitions.setter
    def definitions(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "definitions", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The JSON escaped string defining the document representing the Schema.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class _ApiSchemaState:
    def __init__(__self__, *,
                 api_management_name: Optional[pulumi.Input[str]] = None,
                 api_name: Optional[pulumi.Input[str]] = None,
                 components: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 definitions: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schema_id: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ApiSchema resources.
        :param pulumi.Input[str] api_management_name: The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] api_name: The name of the API within the API Management Service where this API Schema should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] components: Types definitions. Used for Swagger/OpenAPI v2/v3 schemas only.
        :param pulumi.Input[str] content_type: The content type of the API Schema.
        :param pulumi.Input[str] definitions: Types definitions. Used for Swagger/OpenAPI v1 schemas only.
        :param pulumi.Input[str] resource_group_name: The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] schema_id: A unique identifier for this API Schema. Changing this forces a new resource to be created.
        :param pulumi.Input[str] value: The JSON escaped string defining the document representing the Schema.
        """
        if api_management_name is not None:
            pulumi.set(__self__, "api_management_name", api_management_name)
        if api_name is not None:
            pulumi.set(__self__, "api_name", api_name)
        if components is not None:
            pulumi.set(__self__, "components", components)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if definitions is not None:
            pulumi.set(__self__, "definitions", definitions)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if schema_id is not None:
            pulumi.set(__self__, "schema_id", schema_id)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_name")

    @api_management_name.setter
    def api_management_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_management_name", value)

    @property
    @pulumi.getter(name="apiName")
    def api_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API within the API Management Service where this API Schema should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_name")

    @api_name.setter
    def api_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_name", value)

    @property
    @pulumi.getter
    def components(self) -> Optional[pulumi.Input[str]]:
        """
        Types definitions. Used for Swagger/OpenAPI v2/v3 schemas only.
        """
        return pulumi.get(self, "components")

    @components.setter
    def components(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "components", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        """
        The content type of the API Schema.
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter
    def definitions(self) -> Optional[pulumi.Input[str]]:
        """
        Types definitions. Used for Swagger/OpenAPI v1 schemas only.
        """
        return pulumi.get(self, "definitions")

    @definitions.setter
    def definitions(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "definitions", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="schemaId")
    def schema_id(self) -> Optional[pulumi.Input[str]]:
        """
        A unique identifier for this API Schema. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "schema_id")

    @schema_id.setter
    def schema_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schema_id", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The JSON escaped string defining the document representing the Schema.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


class ApiSchema(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_name: Optional[pulumi.Input[str]] = None,
                 api_name: Optional[pulumi.Input[str]] = None,
                 components: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 definitions: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schema_id: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an API Schema within an API Management Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_api = azure.apimanagement.get_api(name="search-api",
            api_management_name="search-api-management",
            resource_group_name="search-service",
            revision="2")
        example_api_schema = azure.apimanagement.ApiSchema("exampleApiSchema",
            api_name=example_api.name,
            api_management_name=example_api.api_management_name,
            resource_group_name=example_api.resource_group_name,
            schema_id="example-schema",
            content_type="application/vnd.ms-azure-apim.xsd+xml",
            value=(lambda path: open(path).read())("api_management_api_schema.xml"))
        ```

        ## Import

        API Management API Schema's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/apiSchema:ApiSchema example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.ApiManagement/service/instance1/apis/api1/schemas/schema1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] api_name: The name of the API within the API Management Service where this API Schema should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] components: Types definitions. Used for Swagger/OpenAPI v2/v3 schemas only.
        :param pulumi.Input[str] content_type: The content type of the API Schema.
        :param pulumi.Input[str] definitions: Types definitions. Used for Swagger/OpenAPI v1 schemas only.
        :param pulumi.Input[str] resource_group_name: The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] schema_id: A unique identifier for this API Schema. Changing this forces a new resource to be created.
        :param pulumi.Input[str] value: The JSON escaped string defining the document representing the Schema.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApiSchemaArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an API Schema within an API Management Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_api = azure.apimanagement.get_api(name="search-api",
            api_management_name="search-api-management",
            resource_group_name="search-service",
            revision="2")
        example_api_schema = azure.apimanagement.ApiSchema("exampleApiSchema",
            api_name=example_api.name,
            api_management_name=example_api.api_management_name,
            resource_group_name=example_api.resource_group_name,
            schema_id="example-schema",
            content_type="application/vnd.ms-azure-apim.xsd+xml",
            value=(lambda path: open(path).read())("api_management_api_schema.xml"))
        ```

        ## Import

        API Management API Schema's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/apiSchema:ApiSchema example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.ApiManagement/service/instance1/apis/api1/schemas/schema1
        ```

        :param str resource_name: The name of the resource.
        :param ApiSchemaArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApiSchemaArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_name: Optional[pulumi.Input[str]] = None,
                 api_name: Optional[pulumi.Input[str]] = None,
                 components: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 definitions: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schema_id: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApiSchemaArgs.__new__(ApiSchemaArgs)

            if api_management_name is None and not opts.urn:
                raise TypeError("Missing required property 'api_management_name'")
            __props__.__dict__["api_management_name"] = api_management_name
            if api_name is None and not opts.urn:
                raise TypeError("Missing required property 'api_name'")
            __props__.__dict__["api_name"] = api_name
            __props__.__dict__["components"] = components
            if content_type is None and not opts.urn:
                raise TypeError("Missing required property 'content_type'")
            __props__.__dict__["content_type"] = content_type
            __props__.__dict__["definitions"] = definitions
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if schema_id is None and not opts.urn:
                raise TypeError("Missing required property 'schema_id'")
            __props__.__dict__["schema_id"] = schema_id
            __props__.__dict__["value"] = value
        super(ApiSchema, __self__).__init__(
            'azure:apimanagement/apiSchema:ApiSchema',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_management_name: Optional[pulumi.Input[str]] = None,
            api_name: Optional[pulumi.Input[str]] = None,
            components: Optional[pulumi.Input[str]] = None,
            content_type: Optional[pulumi.Input[str]] = None,
            definitions: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            schema_id: Optional[pulumi.Input[str]] = None,
            value: Optional[pulumi.Input[str]] = None) -> 'ApiSchema':
        """
        Get an existing ApiSchema resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] api_name: The name of the API within the API Management Service where this API Schema should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] components: Types definitions. Used for Swagger/OpenAPI v2/v3 schemas only.
        :param pulumi.Input[str] content_type: The content type of the API Schema.
        :param pulumi.Input[str] definitions: Types definitions. Used for Swagger/OpenAPI v1 schemas only.
        :param pulumi.Input[str] resource_group_name: The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] schema_id: A unique identifier for this API Schema. Changing this forces a new resource to be created.
        :param pulumi.Input[str] value: The JSON escaped string defining the document representing the Schema.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ApiSchemaState.__new__(_ApiSchemaState)

        __props__.__dict__["api_management_name"] = api_management_name
        __props__.__dict__["api_name"] = api_name
        __props__.__dict__["components"] = components
        __props__.__dict__["content_type"] = content_type
        __props__.__dict__["definitions"] = definitions
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["schema_id"] = schema_id
        __props__.__dict__["value"] = value
        return ApiSchema(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> pulumi.Output[str]:
        """
        The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_name")

    @property
    @pulumi.getter(name="apiName")
    def api_name(self) -> pulumi.Output[str]:
        """
        The name of the API within the API Management Service where this API Schema should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_name")

    @property
    @pulumi.getter
    def components(self) -> pulumi.Output[Optional[str]]:
        """
        Types definitions. Used for Swagger/OpenAPI v2/v3 schemas only.
        """
        return pulumi.get(self, "components")

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> pulumi.Output[str]:
        """
        The content type of the API Schema.
        """
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter
    def definitions(self) -> pulumi.Output[Optional[str]]:
        """
        Types definitions. Used for Swagger/OpenAPI v1 schemas only.
        """
        return pulumi.get(self, "definitions")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="schemaId")
    def schema_id(self) -> pulumi.Output[str]:
        """
        A unique identifier for this API Schema. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "schema_id")

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[Optional[str]]:
        """
        The JSON escaped string defining the document representing the Schema.
        """
        return pulumi.get(self, "value")

