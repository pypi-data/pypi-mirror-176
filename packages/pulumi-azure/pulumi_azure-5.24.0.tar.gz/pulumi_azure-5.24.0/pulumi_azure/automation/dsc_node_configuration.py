# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DscNodeConfigurationArgs', 'DscNodeConfiguration']

@pulumi.input_type
class DscNodeConfigurationArgs:
    def __init__(__self__, *,
                 automation_account_name: pulumi.Input[str],
                 content_embedded: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DscNodeConfiguration resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] content_embedded: The PowerShell DSC Node Configuration (mof content).
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the DSC Node Configuration. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "automation_account_name", automation_account_name)
        pulumi.set(__self__, "content_embedded", content_embedded)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="automationAccountName")
    def automation_account_name(self) -> pulumi.Input[str]:
        """
        The name of the automation account in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "automation_account_name")

    @automation_account_name.setter
    def automation_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "automation_account_name", value)

    @property
    @pulumi.getter(name="contentEmbedded")
    def content_embedded(self) -> pulumi.Input[str]:
        """
        The PowerShell DSC Node Configuration (mof content).
        """
        return pulumi.get(self, "content_embedded")

    @content_embedded.setter
    def content_embedded(self, value: pulumi.Input[str]):
        pulumi.set(self, "content_embedded", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the DSC Node Configuration. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _DscNodeConfigurationState:
    def __init__(__self__, *,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 configuration_name: Optional[pulumi.Input[str]] = None,
                 content_embedded: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DscNodeConfiguration resources.
        :param pulumi.Input[str] automation_account_name: The name of the automation account in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] content_embedded: The PowerShell DSC Node Configuration (mof content).
        :param pulumi.Input[str] name: Specifies the name of the DSC Node Configuration. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        if automation_account_name is not None:
            pulumi.set(__self__, "automation_account_name", automation_account_name)
        if configuration_name is not None:
            pulumi.set(__self__, "configuration_name", configuration_name)
        if content_embedded is not None:
            pulumi.set(__self__, "content_embedded", content_embedded)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter(name="automationAccountName")
    def automation_account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the automation account in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "automation_account_name")

    @automation_account_name.setter
    def automation_account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "automation_account_name", value)

    @property
    @pulumi.getter(name="configurationName")
    def configuration_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "configuration_name")

    @configuration_name.setter
    def configuration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration_name", value)

    @property
    @pulumi.getter(name="contentEmbedded")
    def content_embedded(self) -> Optional[pulumi.Input[str]]:
        """
        The PowerShell DSC Node Configuration (mof content).
        """
        return pulumi.get(self, "content_embedded")

    @content_embedded.setter
    def content_embedded(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_embedded", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the DSC Node Configuration. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)


class DscNodeConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 content_embedded: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Automation DSC Node Configuration.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.automation.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Basic")
        example_dsc_configuration = azure.automation.DscConfiguration("exampleDscConfiguration",
            resource_group_name=example_resource_group.name,
            automation_account_name=example_account.name,
            location=example_resource_group.location,
            content_embedded="configuration test {}")
        example_dsc_node_configuration = azure.automation.DscNodeConfiguration("exampleDscNodeConfiguration",
            resource_group_name=example_resource_group.name,
            automation_account_name=example_account.name,
            content_embedded=\"\"\"instance of MSFT_FileDirectoryConfiguration as $MSFT_FileDirectoryConfiguration1ref
        {
          ResourceID = "[File]bla";
          Ensure = "Present";
          Contents = "bogus Content";
          DestinationPath = "c:\\\\bogus.txt";
          ModuleName = "PSDesiredStateConfiguration";
          SourceInfo = "::3::9::file";
          ModuleVersion = "1.0";
          ConfigurationName = "bla";
        };
        instance of OMI_ConfigurationDocument
        {
          Version="2.0.0";
          MinimumCompatibleVersion = "1.0.0";
          CompatibleVersionAdditionalProperties= {"Omi_BaseResource:ConfigurationName"};
          Author="bogusAuthor";
          GenerationDate="06/15/2018 14:06:24";
          GenerationHost="bogusComputer";
          Name="test";
        };
        \"\"\",
            opts=pulumi.ResourceOptions(depends_on=[example_dsc_configuration]))
        ```

        ## Import

        Automation DSC Node Configuration's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:automation/dscNodeConfiguration:DscNodeConfiguration configuration1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Automation/automationAccounts/account1/nodeConfigurations/configuration1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] content_embedded: The PowerShell DSC Node Configuration (mof content).
        :param pulumi.Input[str] name: Specifies the name of the DSC Node Configuration. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DscNodeConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Automation DSC Node Configuration.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.automation.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Basic")
        example_dsc_configuration = azure.automation.DscConfiguration("exampleDscConfiguration",
            resource_group_name=example_resource_group.name,
            automation_account_name=example_account.name,
            location=example_resource_group.location,
            content_embedded="configuration test {}")
        example_dsc_node_configuration = azure.automation.DscNodeConfiguration("exampleDscNodeConfiguration",
            resource_group_name=example_resource_group.name,
            automation_account_name=example_account.name,
            content_embedded=\"\"\"instance of MSFT_FileDirectoryConfiguration as $MSFT_FileDirectoryConfiguration1ref
        {
          ResourceID = "[File]bla";
          Ensure = "Present";
          Contents = "bogus Content";
          DestinationPath = "c:\\\\bogus.txt";
          ModuleName = "PSDesiredStateConfiguration";
          SourceInfo = "::3::9::file";
          ModuleVersion = "1.0";
          ConfigurationName = "bla";
        };
        instance of OMI_ConfigurationDocument
        {
          Version="2.0.0";
          MinimumCompatibleVersion = "1.0.0";
          CompatibleVersionAdditionalProperties= {"Omi_BaseResource:ConfigurationName"};
          Author="bogusAuthor";
          GenerationDate="06/15/2018 14:06:24";
          GenerationHost="bogusComputer";
          Name="test";
        };
        \"\"\",
            opts=pulumi.ResourceOptions(depends_on=[example_dsc_configuration]))
        ```

        ## Import

        Automation DSC Node Configuration's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:automation/dscNodeConfiguration:DscNodeConfiguration configuration1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Automation/automationAccounts/account1/nodeConfigurations/configuration1
        ```

        :param str resource_name: The name of the resource.
        :param DscNodeConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DscNodeConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 content_embedded: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DscNodeConfigurationArgs.__new__(DscNodeConfigurationArgs)

            if automation_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'automation_account_name'")
            __props__.__dict__["automation_account_name"] = automation_account_name
            if content_embedded is None and not opts.urn:
                raise TypeError("Missing required property 'content_embedded'")
            __props__.__dict__["content_embedded"] = content_embedded
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["configuration_name"] = None
        super(DscNodeConfiguration, __self__).__init__(
            'azure:automation/dscNodeConfiguration:DscNodeConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            automation_account_name: Optional[pulumi.Input[str]] = None,
            configuration_name: Optional[pulumi.Input[str]] = None,
            content_embedded: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None) -> 'DscNodeConfiguration':
        """
        Get an existing DscNodeConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] content_embedded: The PowerShell DSC Node Configuration (mof content).
        :param pulumi.Input[str] name: Specifies the name of the DSC Node Configuration. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DscNodeConfigurationState.__new__(_DscNodeConfigurationState)

        __props__.__dict__["automation_account_name"] = automation_account_name
        __props__.__dict__["configuration_name"] = configuration_name
        __props__.__dict__["content_embedded"] = content_embedded
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        return DscNodeConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="automationAccountName")
    def automation_account_name(self) -> pulumi.Output[str]:
        """
        The name of the automation account in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "automation_account_name")

    @property
    @pulumi.getter(name="configurationName")
    def configuration_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "configuration_name")

    @property
    @pulumi.getter(name="contentEmbedded")
    def content_embedded(self) -> pulumi.Output[str]:
        """
        The PowerShell DSC Node Configuration (mof content).
        """
        return pulumi.get(self, "content_embedded")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the DSC Node Configuration. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which the DSC Node Configuration is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

