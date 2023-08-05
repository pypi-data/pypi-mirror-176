# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BoolVariableArgs', 'BoolVariable']

@pulumi.input_type
class BoolVariableArgs:
    def __init__(__self__, *,
                 automation_account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a BoolVariable resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account in which the Variable is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Automation Variable. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of the Automation Variable.
        :param pulumi.Input[bool] encrypted: Specifies if the Automation Variable is encrypted. Defaults to `false`.
        :param pulumi.Input[str] name: The name of the Automation Variable. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] value: The value of the Automation Variable as a `boolean`.
        """
        pulumi.set(__self__, "automation_account_name", automation_account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encrypted is not None:
            pulumi.set(__self__, "encrypted", encrypted)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="automationAccountName")
    def automation_account_name(self) -> pulumi.Input[str]:
        """
        The name of the automation account in which the Variable is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "automation_account_name")

    @automation_account_name.setter
    def automation_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "automation_account_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the Automation Variable. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Automation Variable.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def encrypted(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if the Automation Variable is encrypted. Defaults to `false`.
        """
        return pulumi.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encrypted", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Automation Variable. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[bool]]:
        """
        The value of the Automation Variable as a `boolean`.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class _BoolVariableState:
    def __init__(__self__, *,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering BoolVariable resources.
        :param pulumi.Input[str] automation_account_name: The name of the automation account in which the Variable is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of the Automation Variable.
        :param pulumi.Input[bool] encrypted: Specifies if the Automation Variable is encrypted. Defaults to `false`.
        :param pulumi.Input[str] name: The name of the Automation Variable. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Automation Variable. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] value: The value of the Automation Variable as a `boolean`.
        """
        if automation_account_name is not None:
            pulumi.set(__self__, "automation_account_name", automation_account_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encrypted is not None:
            pulumi.set(__self__, "encrypted", encrypted)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="automationAccountName")
    def automation_account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the automation account in which the Variable is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "automation_account_name")

    @automation_account_name.setter
    def automation_account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "automation_account_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Automation Variable.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def encrypted(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if the Automation Variable is encrypted. Defaults to `false`.
        """
        return pulumi.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encrypted", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Automation Variable. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the Automation Variable. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[bool]]:
        """
        The value of the Automation Variable as a `boolean`.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "value", value)


class BoolVariable(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Manages a boolean variable in Azure Automation

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.automation.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Basic")
        example_bool_variable = azure.automation.BoolVariable("exampleBoolVariable",
            resource_group_name=example_resource_group.name,
            automation_account_name=example_account.name,
            value=False)
        ```

        ## Import

        Automation Bool Variable can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:automation/boolVariable:BoolVariable example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/tfex-example-rg/providers/Microsoft.Automation/automationAccounts/tfex-example-account/variables/tfex-example-var
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account in which the Variable is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of the Automation Variable.
        :param pulumi.Input[bool] encrypted: Specifies if the Automation Variable is encrypted. Defaults to `false`.
        :param pulumi.Input[str] name: The name of the Automation Variable. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Automation Variable. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] value: The value of the Automation Variable as a `boolean`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BoolVariableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a boolean variable in Azure Automation

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.automation.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Basic")
        example_bool_variable = azure.automation.BoolVariable("exampleBoolVariable",
            resource_group_name=example_resource_group.name,
            automation_account_name=example_account.name,
            value=False)
        ```

        ## Import

        Automation Bool Variable can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:automation/boolVariable:BoolVariable example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/tfex-example-rg/providers/Microsoft.Automation/automationAccounts/tfex-example-account/variables/tfex-example-var
        ```

        :param str resource_name: The name of the resource.
        :param BoolVariableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BoolVariableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BoolVariableArgs.__new__(BoolVariableArgs)

            if automation_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'automation_account_name'")
            __props__.__dict__["automation_account_name"] = automation_account_name
            __props__.__dict__["description"] = description
            __props__.__dict__["encrypted"] = encrypted
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["value"] = value
        super(BoolVariable, __self__).__init__(
            'azure:automation/boolVariable:BoolVariable',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            automation_account_name: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            encrypted: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            value: Optional[pulumi.Input[bool]] = None) -> 'BoolVariable':
        """
        Get an existing BoolVariable resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account in which the Variable is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of the Automation Variable.
        :param pulumi.Input[bool] encrypted: Specifies if the Automation Variable is encrypted. Defaults to `false`.
        :param pulumi.Input[str] name: The name of the Automation Variable. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Automation Variable. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] value: The value of the Automation Variable as a `boolean`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BoolVariableState.__new__(_BoolVariableState)

        __props__.__dict__["automation_account_name"] = automation_account_name
        __props__.__dict__["description"] = description
        __props__.__dict__["encrypted"] = encrypted
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["value"] = value
        return BoolVariable(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="automationAccountName")
    def automation_account_name(self) -> pulumi.Output[str]:
        """
        The name of the automation account in which the Variable is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "automation_account_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the Automation Variable.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def encrypted(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if the Automation Variable is encrypted. Defaults to `false`.
        """
        return pulumi.get(self, "encrypted")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Automation Variable. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the Automation Variable. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[Optional[bool]]:
        """
        The value of the Automation Variable as a `boolean`.
        """
        return pulumi.get(self, "value")

