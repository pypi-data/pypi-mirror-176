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

__all__ = ['ServiceArgs', 'Service']

@pulumi.input_type
class ServiceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 access_policy_object_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 authentication_configuration: Optional[pulumi.Input['ServiceAuthenticationConfigurationArgs']] = None,
                 cors_configuration: Optional[pulumi.Input['ServiceCorsConfigurationArgs']] = None,
                 cosmosdb_key_vault_key_versionless_id: Optional[pulumi.Input[str]] = None,
                 cosmosdb_throughput: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_network_access_enabled: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Service resource.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which to create the Service.
        :param pulumi.Input['ServiceAuthenticationConfigurationArgs'] authentication_configuration: An `authentication_configuration` block as defined below.
        :param pulumi.Input['ServiceCorsConfigurationArgs'] cors_configuration: A `cors_configuration` block as defined below.
        :param pulumi.Input[str] cosmosdb_key_vault_key_versionless_id: A versionless Key Vault Key ID for CMK encryption of the backing database. Changing this forces a new resource to be created.
        :param pulumi.Input[int] cosmosdb_throughput: The provisioned throughput for the backing database. Range of `400`-`10000`. Defaults to `400`.
        :param pulumi.Input[str] kind: The type of the service. Values at time of publication are: `fhir`, `fhir-Stu3` and `fhir-R4`. Default value is `fhir`.
        :param pulumi.Input[str] location: Specifies the supported Azure Region where the Service should be created.
        :param pulumi.Input[str] name: The name of the service instance. Used for service endpoint, must be unique within the audience.
        :param pulumi.Input[bool] public_network_access_enabled: Whether public network access is enabled or disabled for this service instance.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if access_policy_object_ids is not None:
            pulumi.set(__self__, "access_policy_object_ids", access_policy_object_ids)
        if authentication_configuration is not None:
            pulumi.set(__self__, "authentication_configuration", authentication_configuration)
        if cors_configuration is not None:
            pulumi.set(__self__, "cors_configuration", cors_configuration)
        if cosmosdb_key_vault_key_versionless_id is not None:
            pulumi.set(__self__, "cosmosdb_key_vault_key_versionless_id", cosmosdb_key_vault_key_versionless_id)
        if cosmosdb_throughput is not None:
            pulumi.set(__self__, "cosmosdb_throughput", cosmosdb_throughput)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if public_network_access_enabled is not None:
            pulumi.set(__self__, "public_network_access_enabled", public_network_access_enabled)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group in which to create the Service.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="accessPolicyObjectIds")
    def access_policy_object_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "access_policy_object_ids")

    @access_policy_object_ids.setter
    def access_policy_object_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "access_policy_object_ids", value)

    @property
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> Optional[pulumi.Input['ServiceAuthenticationConfigurationArgs']]:
        """
        An `authentication_configuration` block as defined below.
        """
        return pulumi.get(self, "authentication_configuration")

    @authentication_configuration.setter
    def authentication_configuration(self, value: Optional[pulumi.Input['ServiceAuthenticationConfigurationArgs']]):
        pulumi.set(self, "authentication_configuration", value)

    @property
    @pulumi.getter(name="corsConfiguration")
    def cors_configuration(self) -> Optional[pulumi.Input['ServiceCorsConfigurationArgs']]:
        """
        A `cors_configuration` block as defined below.
        """
        return pulumi.get(self, "cors_configuration")

    @cors_configuration.setter
    def cors_configuration(self, value: Optional[pulumi.Input['ServiceCorsConfigurationArgs']]):
        pulumi.set(self, "cors_configuration", value)

    @property
    @pulumi.getter(name="cosmosdbKeyVaultKeyVersionlessId")
    def cosmosdb_key_vault_key_versionless_id(self) -> Optional[pulumi.Input[str]]:
        """
        A versionless Key Vault Key ID for CMK encryption of the backing database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "cosmosdb_key_vault_key_versionless_id")

    @cosmosdb_key_vault_key_versionless_id.setter
    def cosmosdb_key_vault_key_versionless_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cosmosdb_key_vault_key_versionless_id", value)

    @property
    @pulumi.getter(name="cosmosdbThroughput")
    def cosmosdb_throughput(self) -> Optional[pulumi.Input[int]]:
        """
        The provisioned throughput for the backing database. Range of `400`-`10000`. Defaults to `400`.
        """
        return pulumi.get(self, "cosmosdb_throughput")

    @cosmosdb_throughput.setter
    def cosmosdb_throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cosmosdb_throughput", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the service. Values at time of publication are: `fhir`, `fhir-Stu3` and `fhir-R4`. Default value is `fhir`.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure Region where the Service should be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the service instance. Used for service endpoint, must be unique within the audience.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="publicNetworkAccessEnabled")
    def public_network_access_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether public network access is enabled or disabled for this service instance.
        """
        return pulumi.get(self, "public_network_access_enabled")

    @public_network_access_enabled.setter
    def public_network_access_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "public_network_access_enabled", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ServiceState:
    def __init__(__self__, *,
                 access_policy_object_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 authentication_configuration: Optional[pulumi.Input['ServiceAuthenticationConfigurationArgs']] = None,
                 cors_configuration: Optional[pulumi.Input['ServiceCorsConfigurationArgs']] = None,
                 cosmosdb_key_vault_key_versionless_id: Optional[pulumi.Input[str]] = None,
                 cosmosdb_throughput: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_network_access_enabled: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Service resources.
        :param pulumi.Input['ServiceAuthenticationConfigurationArgs'] authentication_configuration: An `authentication_configuration` block as defined below.
        :param pulumi.Input['ServiceCorsConfigurationArgs'] cors_configuration: A `cors_configuration` block as defined below.
        :param pulumi.Input[str] cosmosdb_key_vault_key_versionless_id: A versionless Key Vault Key ID for CMK encryption of the backing database. Changing this forces a new resource to be created.
        :param pulumi.Input[int] cosmosdb_throughput: The provisioned throughput for the backing database. Range of `400`-`10000`. Defaults to `400`.
        :param pulumi.Input[str] kind: The type of the service. Values at time of publication are: `fhir`, `fhir-Stu3` and `fhir-R4`. Default value is `fhir`.
        :param pulumi.Input[str] location: Specifies the supported Azure Region where the Service should be created.
        :param pulumi.Input[str] name: The name of the service instance. Used for service endpoint, must be unique within the audience.
        :param pulumi.Input[bool] public_network_access_enabled: Whether public network access is enabled or disabled for this service instance.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which to create the Service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        if access_policy_object_ids is not None:
            pulumi.set(__self__, "access_policy_object_ids", access_policy_object_ids)
        if authentication_configuration is not None:
            pulumi.set(__self__, "authentication_configuration", authentication_configuration)
        if cors_configuration is not None:
            pulumi.set(__self__, "cors_configuration", cors_configuration)
        if cosmosdb_key_vault_key_versionless_id is not None:
            pulumi.set(__self__, "cosmosdb_key_vault_key_versionless_id", cosmosdb_key_vault_key_versionless_id)
        if cosmosdb_throughput is not None:
            pulumi.set(__self__, "cosmosdb_throughput", cosmosdb_throughput)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if public_network_access_enabled is not None:
            pulumi.set(__self__, "public_network_access_enabled", public_network_access_enabled)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="accessPolicyObjectIds")
    def access_policy_object_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "access_policy_object_ids")

    @access_policy_object_ids.setter
    def access_policy_object_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "access_policy_object_ids", value)

    @property
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> Optional[pulumi.Input['ServiceAuthenticationConfigurationArgs']]:
        """
        An `authentication_configuration` block as defined below.
        """
        return pulumi.get(self, "authentication_configuration")

    @authentication_configuration.setter
    def authentication_configuration(self, value: Optional[pulumi.Input['ServiceAuthenticationConfigurationArgs']]):
        pulumi.set(self, "authentication_configuration", value)

    @property
    @pulumi.getter(name="corsConfiguration")
    def cors_configuration(self) -> Optional[pulumi.Input['ServiceCorsConfigurationArgs']]:
        """
        A `cors_configuration` block as defined below.
        """
        return pulumi.get(self, "cors_configuration")

    @cors_configuration.setter
    def cors_configuration(self, value: Optional[pulumi.Input['ServiceCorsConfigurationArgs']]):
        pulumi.set(self, "cors_configuration", value)

    @property
    @pulumi.getter(name="cosmosdbKeyVaultKeyVersionlessId")
    def cosmosdb_key_vault_key_versionless_id(self) -> Optional[pulumi.Input[str]]:
        """
        A versionless Key Vault Key ID for CMK encryption of the backing database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "cosmosdb_key_vault_key_versionless_id")

    @cosmosdb_key_vault_key_versionless_id.setter
    def cosmosdb_key_vault_key_versionless_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cosmosdb_key_vault_key_versionless_id", value)

    @property
    @pulumi.getter(name="cosmosdbThroughput")
    def cosmosdb_throughput(self) -> Optional[pulumi.Input[int]]:
        """
        The provisioned throughput for the backing database. Range of `400`-`10000`. Defaults to `400`.
        """
        return pulumi.get(self, "cosmosdb_throughput")

    @cosmosdb_throughput.setter
    def cosmosdb_throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cosmosdb_throughput", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the service. Values at time of publication are: `fhir`, `fhir-Stu3` and `fhir-R4`. Default value is `fhir`.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure Region where the Service should be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the service instance. Used for service endpoint, must be unique within the audience.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="publicNetworkAccessEnabled")
    def public_network_access_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether public network access is enabled or disabled for this service instance.
        """
        return pulumi.get(self, "public_network_access_enabled")

    @public_network_access_enabled.setter
    def public_network_access_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "public_network_access_enabled", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group in which to create the Service.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Service(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_policy_object_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 authentication_configuration: Optional[pulumi.Input[pulumi.InputType['ServiceAuthenticationConfigurationArgs']]] = None,
                 cors_configuration: Optional[pulumi.Input[pulumi.InputType['ServiceCorsConfigurationArgs']]] = None,
                 cosmosdb_key_vault_key_versionless_id: Optional[pulumi.Input[str]] = None,
                 cosmosdb_throughput: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_network_access_enabled: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Healthcare Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example = azure.healthcare.Service("example",
            resource_group_name="sample-resource-group",
            location="westus2",
            kind="fhir-R4",
            cosmosdb_throughput=2000,
            access_policy_object_ids=current.object_id,
            tags={
                "environment": "testenv",
                "purpose": "AcceptanceTests",
            },
            authentication_configuration=azure.healthcare.ServiceAuthenticationConfigurationArgs(
                authority="https://login.microsoftonline.com/$%7Bdata.azurerm_client_config.current.tenant_id%7D",
                audience="https://azurehealthcareapis.com/",
                smart_proxy_enabled=True,
            ),
            cors_configuration=azure.healthcare.ServiceCorsConfigurationArgs(
                allowed_origins=[
                    "http://www.example.com",
                    "http://www.example2.com",
                ],
                allowed_headers=[
                    "x-tempo-*",
                    "x-tempo2-*",
                ],
                allowed_methods=[
                    "GET",
                    "PUT",
                ],
                max_age_in_seconds=500,
                allow_credentials=True,
            ))
        ```

        ## Import

        Healthcare Service can be imported using the resource`id`, e.g.

        ```sh
         $ pulumi import azure:healthcare/service:Service example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource_group/providers/Microsoft.HealthcareApis/services/service_name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ServiceAuthenticationConfigurationArgs']] authentication_configuration: An `authentication_configuration` block as defined below.
        :param pulumi.Input[pulumi.InputType['ServiceCorsConfigurationArgs']] cors_configuration: A `cors_configuration` block as defined below.
        :param pulumi.Input[str] cosmosdb_key_vault_key_versionless_id: A versionless Key Vault Key ID for CMK encryption of the backing database. Changing this forces a new resource to be created.
        :param pulumi.Input[int] cosmosdb_throughput: The provisioned throughput for the backing database. Range of `400`-`10000`. Defaults to `400`.
        :param pulumi.Input[str] kind: The type of the service. Values at time of publication are: `fhir`, `fhir-Stu3` and `fhir-R4`. Default value is `fhir`.
        :param pulumi.Input[str] location: Specifies the supported Azure Region where the Service should be created.
        :param pulumi.Input[str] name: The name of the service instance. Used for service endpoint, must be unique within the audience.
        :param pulumi.Input[bool] public_network_access_enabled: Whether public network access is enabled or disabled for this service instance.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which to create the Service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Healthcare Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example = azure.healthcare.Service("example",
            resource_group_name="sample-resource-group",
            location="westus2",
            kind="fhir-R4",
            cosmosdb_throughput=2000,
            access_policy_object_ids=current.object_id,
            tags={
                "environment": "testenv",
                "purpose": "AcceptanceTests",
            },
            authentication_configuration=azure.healthcare.ServiceAuthenticationConfigurationArgs(
                authority="https://login.microsoftonline.com/$%7Bdata.azurerm_client_config.current.tenant_id%7D",
                audience="https://azurehealthcareapis.com/",
                smart_proxy_enabled=True,
            ),
            cors_configuration=azure.healthcare.ServiceCorsConfigurationArgs(
                allowed_origins=[
                    "http://www.example.com",
                    "http://www.example2.com",
                ],
                allowed_headers=[
                    "x-tempo-*",
                    "x-tempo2-*",
                ],
                allowed_methods=[
                    "GET",
                    "PUT",
                ],
                max_age_in_seconds=500,
                allow_credentials=True,
            ))
        ```

        ## Import

        Healthcare Service can be imported using the resource`id`, e.g.

        ```sh
         $ pulumi import azure:healthcare/service:Service example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource_group/providers/Microsoft.HealthcareApis/services/service_name
        ```

        :param str resource_name: The name of the resource.
        :param ServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_policy_object_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 authentication_configuration: Optional[pulumi.Input[pulumi.InputType['ServiceAuthenticationConfigurationArgs']]] = None,
                 cors_configuration: Optional[pulumi.Input[pulumi.InputType['ServiceCorsConfigurationArgs']]] = None,
                 cosmosdb_key_vault_key_versionless_id: Optional[pulumi.Input[str]] = None,
                 cosmosdb_throughput: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_network_access_enabled: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceArgs.__new__(ServiceArgs)

            __props__.__dict__["access_policy_object_ids"] = access_policy_object_ids
            __props__.__dict__["authentication_configuration"] = authentication_configuration
            __props__.__dict__["cors_configuration"] = cors_configuration
            __props__.__dict__["cosmosdb_key_vault_key_versionless_id"] = cosmosdb_key_vault_key_versionless_id
            __props__.__dict__["cosmosdb_throughput"] = cosmosdb_throughput
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["public_network_access_enabled"] = public_network_access_enabled
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
        super(Service, __self__).__init__(
            'azure:healthcare/service:Service',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_policy_object_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            authentication_configuration: Optional[pulumi.Input[pulumi.InputType['ServiceAuthenticationConfigurationArgs']]] = None,
            cors_configuration: Optional[pulumi.Input[pulumi.InputType['ServiceCorsConfigurationArgs']]] = None,
            cosmosdb_key_vault_key_versionless_id: Optional[pulumi.Input[str]] = None,
            cosmosdb_throughput: Optional[pulumi.Input[int]] = None,
            kind: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            public_network_access_enabled: Optional[pulumi.Input[bool]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Service':
        """
        Get an existing Service resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ServiceAuthenticationConfigurationArgs']] authentication_configuration: An `authentication_configuration` block as defined below.
        :param pulumi.Input[pulumi.InputType['ServiceCorsConfigurationArgs']] cors_configuration: A `cors_configuration` block as defined below.
        :param pulumi.Input[str] cosmosdb_key_vault_key_versionless_id: A versionless Key Vault Key ID for CMK encryption of the backing database. Changing this forces a new resource to be created.
        :param pulumi.Input[int] cosmosdb_throughput: The provisioned throughput for the backing database. Range of `400`-`10000`. Defaults to `400`.
        :param pulumi.Input[str] kind: The type of the service. Values at time of publication are: `fhir`, `fhir-Stu3` and `fhir-R4`. Default value is `fhir`.
        :param pulumi.Input[str] location: Specifies the supported Azure Region where the Service should be created.
        :param pulumi.Input[str] name: The name of the service instance. Used for service endpoint, must be unique within the audience.
        :param pulumi.Input[bool] public_network_access_enabled: Whether public network access is enabled or disabled for this service instance.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which to create the Service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceState.__new__(_ServiceState)

        __props__.__dict__["access_policy_object_ids"] = access_policy_object_ids
        __props__.__dict__["authentication_configuration"] = authentication_configuration
        __props__.__dict__["cors_configuration"] = cors_configuration
        __props__.__dict__["cosmosdb_key_vault_key_versionless_id"] = cosmosdb_key_vault_key_versionless_id
        __props__.__dict__["cosmosdb_throughput"] = cosmosdb_throughput
        __props__.__dict__["kind"] = kind
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["public_network_access_enabled"] = public_network_access_enabled
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        return Service(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessPolicyObjectIds")
    def access_policy_object_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "access_policy_object_ids")

    @property
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> pulumi.Output['outputs.ServiceAuthenticationConfiguration']:
        """
        An `authentication_configuration` block as defined below.
        """
        return pulumi.get(self, "authentication_configuration")

    @property
    @pulumi.getter(name="corsConfiguration")
    def cors_configuration(self) -> pulumi.Output['outputs.ServiceCorsConfiguration']:
        """
        A `cors_configuration` block as defined below.
        """
        return pulumi.get(self, "cors_configuration")

    @property
    @pulumi.getter(name="cosmosdbKeyVaultKeyVersionlessId")
    def cosmosdb_key_vault_key_versionless_id(self) -> pulumi.Output[Optional[str]]:
        """
        A versionless Key Vault Key ID for CMK encryption of the backing database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "cosmosdb_key_vault_key_versionless_id")

    @property
    @pulumi.getter(name="cosmosdbThroughput")
    def cosmosdb_throughput(self) -> pulumi.Output[Optional[int]]:
        """
        The provisioned throughput for the backing database. Range of `400`-`10000`. Defaults to `400`.
        """
        return pulumi.get(self, "cosmosdb_throughput")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        The type of the service. Values at time of publication are: `fhir`, `fhir-Stu3` and `fhir-R4`. Default value is `fhir`.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure Region where the Service should be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the service instance. Used for service endpoint, must be unique within the audience.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicNetworkAccessEnabled")
    def public_network_access_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether public network access is enabled or disabled for this service instance.
        """
        return pulumi.get(self, "public_network_access_enabled")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group in which to create the Service.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

