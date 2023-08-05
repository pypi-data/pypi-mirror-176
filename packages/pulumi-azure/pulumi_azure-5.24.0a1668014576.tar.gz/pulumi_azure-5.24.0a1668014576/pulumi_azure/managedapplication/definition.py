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

__all__ = ['DefinitionArgs', 'Definition']

@pulumi.input_type
class DefinitionArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 lock_level: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 authorizations: Optional[pulumi.Input[Sequence[pulumi.Input['DefinitionAuthorizationArgs']]]] = None,
                 create_ui_definition: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 main_template: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 package_enabled: Optional[pulumi.Input[bool]] = None,
                 package_file_uri: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Definition resource.
        :param pulumi.Input[str] display_name: Specifies the managed application definition display name.
        :param pulumi.Input[str] lock_level: Specifies the managed application lock level. Valid values include `CanNotDelete`, `None`, `ReadOnly`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Managed Application Definition should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['DefinitionAuthorizationArgs']]] authorizations: One or more `authorization` block defined below.
        :param pulumi.Input[str] create_ui_definition: Specifies the `createUiDefinition` JSON for the backing template with `Microsoft.Solutions/applications` resource.
        :param pulumi.Input[str] description: Specifies the managed application definition description.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] main_template: Specifies the inline main template JSON which has resources to be provisioned.
        :param pulumi.Input[str] name: Specifies the name of the Managed Application Definition. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] package_enabled: Is the package enabled? Defaults to `true`.
        :param pulumi.Input[str] package_file_uri: Specifies the managed application definition package file Uri.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "lock_level", lock_level)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if authorizations is not None:
            pulumi.set(__self__, "authorizations", authorizations)
        if create_ui_definition is not None:
            pulumi.set(__self__, "create_ui_definition", create_ui_definition)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if main_template is not None:
            pulumi.set(__self__, "main_template", main_template)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if package_enabled is not None:
            pulumi.set(__self__, "package_enabled", package_enabled)
        if package_file_uri is not None:
            pulumi.set(__self__, "package_file_uri", package_file_uri)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        Specifies the managed application definition display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="lockLevel")
    def lock_level(self) -> pulumi.Input[str]:
        """
        Specifies the managed application lock level. Valid values include `CanNotDelete`, `None`, `ReadOnly`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "lock_level")

    @lock_level.setter
    def lock_level(self, value: pulumi.Input[str]):
        pulumi.set(self, "lock_level", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Managed Application Definition should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def authorizations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DefinitionAuthorizationArgs']]]]:
        """
        One or more `authorization` block defined below.
        """
        return pulumi.get(self, "authorizations")

    @authorizations.setter
    def authorizations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DefinitionAuthorizationArgs']]]]):
        pulumi.set(self, "authorizations", value)

    @property
    @pulumi.getter(name="createUiDefinition")
    def create_ui_definition(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the `createUiDefinition` JSON for the backing template with `Microsoft.Solutions/applications` resource.
        """
        return pulumi.get(self, "create_ui_definition")

    @create_ui_definition.setter
    def create_ui_definition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_ui_definition", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the managed application definition description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="mainTemplate")
    def main_template(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the inline main template JSON which has resources to be provisioned.
        """
        return pulumi.get(self, "main_template")

    @main_template.setter
    def main_template(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "main_template", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Managed Application Definition. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="packageEnabled")
    def package_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the package enabled? Defaults to `true`.
        """
        return pulumi.get(self, "package_enabled")

    @package_enabled.setter
    def package_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "package_enabled", value)

    @property
    @pulumi.getter(name="packageFileUri")
    def package_file_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the managed application definition package file Uri.
        """
        return pulumi.get(self, "package_file_uri")

    @package_file_uri.setter
    def package_file_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_file_uri", value)

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
class _DefinitionState:
    def __init__(__self__, *,
                 authorizations: Optional[pulumi.Input[Sequence[pulumi.Input['DefinitionAuthorizationArgs']]]] = None,
                 create_ui_definition: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 lock_level: Optional[pulumi.Input[str]] = None,
                 main_template: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 package_enabled: Optional[pulumi.Input[bool]] = None,
                 package_file_uri: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Definition resources.
        :param pulumi.Input[Sequence[pulumi.Input['DefinitionAuthorizationArgs']]] authorizations: One or more `authorization` block defined below.
        :param pulumi.Input[str] create_ui_definition: Specifies the `createUiDefinition` JSON for the backing template with `Microsoft.Solutions/applications` resource.
        :param pulumi.Input[str] description: Specifies the managed application definition description.
        :param pulumi.Input[str] display_name: Specifies the managed application definition display name.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] lock_level: Specifies the managed application lock level. Valid values include `CanNotDelete`, `None`, `ReadOnly`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] main_template: Specifies the inline main template JSON which has resources to be provisioned.
        :param pulumi.Input[str] name: Specifies the name of the Managed Application Definition. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] package_enabled: Is the package enabled? Defaults to `true`.
        :param pulumi.Input[str] package_file_uri: Specifies the managed application definition package file Uri.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Managed Application Definition should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        if authorizations is not None:
            pulumi.set(__self__, "authorizations", authorizations)
        if create_ui_definition is not None:
            pulumi.set(__self__, "create_ui_definition", create_ui_definition)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if lock_level is not None:
            pulumi.set(__self__, "lock_level", lock_level)
        if main_template is not None:
            pulumi.set(__self__, "main_template", main_template)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if package_enabled is not None:
            pulumi.set(__self__, "package_enabled", package_enabled)
        if package_file_uri is not None:
            pulumi.set(__self__, "package_file_uri", package_file_uri)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def authorizations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DefinitionAuthorizationArgs']]]]:
        """
        One or more `authorization` block defined below.
        """
        return pulumi.get(self, "authorizations")

    @authorizations.setter
    def authorizations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DefinitionAuthorizationArgs']]]]):
        pulumi.set(self, "authorizations", value)

    @property
    @pulumi.getter(name="createUiDefinition")
    def create_ui_definition(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the `createUiDefinition` JSON for the backing template with `Microsoft.Solutions/applications` resource.
        """
        return pulumi.get(self, "create_ui_definition")

    @create_ui_definition.setter
    def create_ui_definition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_ui_definition", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the managed application definition description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the managed application definition display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="lockLevel")
    def lock_level(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the managed application lock level. Valid values include `CanNotDelete`, `None`, `ReadOnly`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "lock_level")

    @lock_level.setter
    def lock_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lock_level", value)

    @property
    @pulumi.getter(name="mainTemplate")
    def main_template(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the inline main template JSON which has resources to be provisioned.
        """
        return pulumi.get(self, "main_template")

    @main_template.setter
    def main_template(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "main_template", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Managed Application Definition. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="packageEnabled")
    def package_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the package enabled? Defaults to `true`.
        """
        return pulumi.get(self, "package_enabled")

    @package_enabled.setter
    def package_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "package_enabled", value)

    @property
    @pulumi.getter(name="packageFileUri")
    def package_file_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the managed application definition package file Uri.
        """
        return pulumi.get(self, "package_file_uri")

    @package_file_uri.setter
    def package_file_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_file_uri", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Managed Application Definition should exist. Changing this forces a new resource to be created.
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


class Definition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorizations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DefinitionAuthorizationArgs']]]]] = None,
                 create_ui_definition: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 lock_level: Optional[pulumi.Input[str]] = None,
                 main_template: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 package_enabled: Optional[pulumi.Input[bool]] = None,
                 package_file_uri: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Managed Application Definition.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_definition = azure.managedapplication.Definition("exampleDefinition",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            lock_level="ReadOnly",
            package_file_uri="https://github.com/Azure/azure-managedapp-samples/raw/master/Managed Application Sample Packages/201-managed-storage-account/managedstorage.zip",
            display_name="TestManagedApplicationDefinition",
            description="Test Managed Application Definition",
            authorizations=[azure.managedapplication.DefinitionAuthorizationArgs(
                service_principal_id=current.object_id,
                role_definition_id="a094b430-dad3-424d-ae58-13f72fd72591",
            )])
        ```

        ## Import

        Managed Application Definition can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:managedapplication/definition:Definition example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Solutions/applicationDefinitions/appDefinition1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DefinitionAuthorizationArgs']]]] authorizations: One or more `authorization` block defined below.
        :param pulumi.Input[str] create_ui_definition: Specifies the `createUiDefinition` JSON for the backing template with `Microsoft.Solutions/applications` resource.
        :param pulumi.Input[str] description: Specifies the managed application definition description.
        :param pulumi.Input[str] display_name: Specifies the managed application definition display name.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] lock_level: Specifies the managed application lock level. Valid values include `CanNotDelete`, `None`, `ReadOnly`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] main_template: Specifies the inline main template JSON which has resources to be provisioned.
        :param pulumi.Input[str] name: Specifies the name of the Managed Application Definition. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] package_enabled: Is the package enabled? Defaults to `true`.
        :param pulumi.Input[str] package_file_uri: Specifies the managed application definition package file Uri.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Managed Application Definition should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Managed Application Definition.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_definition = azure.managedapplication.Definition("exampleDefinition",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            lock_level="ReadOnly",
            package_file_uri="https://github.com/Azure/azure-managedapp-samples/raw/master/Managed Application Sample Packages/201-managed-storage-account/managedstorage.zip",
            display_name="TestManagedApplicationDefinition",
            description="Test Managed Application Definition",
            authorizations=[azure.managedapplication.DefinitionAuthorizationArgs(
                service_principal_id=current.object_id,
                role_definition_id="a094b430-dad3-424d-ae58-13f72fd72591",
            )])
        ```

        ## Import

        Managed Application Definition can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:managedapplication/definition:Definition example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Solutions/applicationDefinitions/appDefinition1
        ```

        :param str resource_name: The name of the resource.
        :param DefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorizations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DefinitionAuthorizationArgs']]]]] = None,
                 create_ui_definition: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 lock_level: Optional[pulumi.Input[str]] = None,
                 main_template: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 package_enabled: Optional[pulumi.Input[bool]] = None,
                 package_file_uri: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DefinitionArgs.__new__(DefinitionArgs)

            __props__.__dict__["authorizations"] = authorizations
            __props__.__dict__["create_ui_definition"] = create_ui_definition
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["location"] = location
            if lock_level is None and not opts.urn:
                raise TypeError("Missing required property 'lock_level'")
            __props__.__dict__["lock_level"] = lock_level
            __props__.__dict__["main_template"] = main_template
            __props__.__dict__["name"] = name
            __props__.__dict__["package_enabled"] = package_enabled
            __props__.__dict__["package_file_uri"] = package_file_uri
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
        super(Definition, __self__).__init__(
            'azure:managedapplication/definition:Definition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            authorizations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DefinitionAuthorizationArgs']]]]] = None,
            create_ui_definition: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            lock_level: Optional[pulumi.Input[str]] = None,
            main_template: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            package_enabled: Optional[pulumi.Input[bool]] = None,
            package_file_uri: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Definition':
        """
        Get an existing Definition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DefinitionAuthorizationArgs']]]] authorizations: One or more `authorization` block defined below.
        :param pulumi.Input[str] create_ui_definition: Specifies the `createUiDefinition` JSON for the backing template with `Microsoft.Solutions/applications` resource.
        :param pulumi.Input[str] description: Specifies the managed application definition description.
        :param pulumi.Input[str] display_name: Specifies the managed application definition display name.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] lock_level: Specifies the managed application lock level. Valid values include `CanNotDelete`, `None`, `ReadOnly`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] main_template: Specifies the inline main template JSON which has resources to be provisioned.
        :param pulumi.Input[str] name: Specifies the name of the Managed Application Definition. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] package_enabled: Is the package enabled? Defaults to `true`.
        :param pulumi.Input[str] package_file_uri: Specifies the managed application definition package file Uri.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Managed Application Definition should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DefinitionState.__new__(_DefinitionState)

        __props__.__dict__["authorizations"] = authorizations
        __props__.__dict__["create_ui_definition"] = create_ui_definition
        __props__.__dict__["description"] = description
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["location"] = location
        __props__.__dict__["lock_level"] = lock_level
        __props__.__dict__["main_template"] = main_template
        __props__.__dict__["name"] = name
        __props__.__dict__["package_enabled"] = package_enabled
        __props__.__dict__["package_file_uri"] = package_file_uri
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        return Definition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def authorizations(self) -> pulumi.Output[Optional[Sequence['outputs.DefinitionAuthorization']]]:
        """
        One or more `authorization` block defined below.
        """
        return pulumi.get(self, "authorizations")

    @property
    @pulumi.getter(name="createUiDefinition")
    def create_ui_definition(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the `createUiDefinition` JSON for the backing template with `Microsoft.Solutions/applications` resource.
        """
        return pulumi.get(self, "create_ui_definition")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the managed application definition description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Specifies the managed application definition display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="lockLevel")
    def lock_level(self) -> pulumi.Output[str]:
        """
        Specifies the managed application lock level. Valid values include `CanNotDelete`, `None`, `ReadOnly`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "lock_level")

    @property
    @pulumi.getter(name="mainTemplate")
    def main_template(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the inline main template JSON which has resources to be provisioned.
        """
        return pulumi.get(self, "main_template")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Managed Application Definition. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="packageEnabled")
    def package_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Is the package enabled? Defaults to `true`.
        """
        return pulumi.get(self, "package_enabled")

    @property
    @pulumi.getter(name="packageFileUri")
    def package_file_uri(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the managed application definition package file Uri.
        """
        return pulumi.get(self, "package_file_uri")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Managed Application Definition should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

