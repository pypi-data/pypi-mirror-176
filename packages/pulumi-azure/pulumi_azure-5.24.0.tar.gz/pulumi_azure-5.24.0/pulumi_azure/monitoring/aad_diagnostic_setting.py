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

__all__ = ['AadDiagnosticSettingArgs', 'AadDiagnosticSetting']

@pulumi.input_type
class AadDiagnosticSettingArgs:
    def __init__(__self__, *,
                 logs: pulumi.Input[Sequence[pulumi.Input['AadDiagnosticSettingLogArgs']]],
                 eventhub_authorization_rule_id: Optional[pulumi.Input[str]] = None,
                 eventhub_name: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AadDiagnosticSetting resource.
        :param pulumi.Input[Sequence[pulumi.Input['AadDiagnosticSettingLogArgs']]] logs: One or more `log` blocks as defined below.
        :param pulumi.Input[str] eventhub_authorization_rule_id: Specifies the ID of an Event Hub Namespace Authorization Rule used to send Diagnostics Data. Changing this forces a new resource to be created.
        :param pulumi.Input[str] eventhub_name: Specifies the name of the Event Hub where Diagnostics Data should be sent. If not specified, the default Event Hub will be used. Changing this forces a new resource to be created.
        :param pulumi.Input[str] log_analytics_workspace_id: Specifies the ID of a Log Analytics Workspace where Diagnostics Data should be sent.
        :param pulumi.Input[str] name: The name which should be used for this Monitor Azure Active Directory Diagnostic Setting. Changing this forces a new Monitor Azure Active Directory Diagnostic Setting to be created.
        :param pulumi.Input[str] storage_account_id: The ID of the Storage Account where logs should be sent. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "logs", logs)
        if eventhub_authorization_rule_id is not None:
            pulumi.set(__self__, "eventhub_authorization_rule_id", eventhub_authorization_rule_id)
        if eventhub_name is not None:
            pulumi.set(__self__, "eventhub_name", eventhub_name)
        if log_analytics_workspace_id is not None:
            pulumi.set(__self__, "log_analytics_workspace_id", log_analytics_workspace_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if storage_account_id is not None:
            pulumi.set(__self__, "storage_account_id", storage_account_id)

    @property
    @pulumi.getter
    def logs(self) -> pulumi.Input[Sequence[pulumi.Input['AadDiagnosticSettingLogArgs']]]:
        """
        One or more `log` blocks as defined below.
        """
        return pulumi.get(self, "logs")

    @logs.setter
    def logs(self, value: pulumi.Input[Sequence[pulumi.Input['AadDiagnosticSettingLogArgs']]]):
        pulumi.set(self, "logs", value)

    @property
    @pulumi.getter(name="eventhubAuthorizationRuleId")
    def eventhub_authorization_rule_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of an Event Hub Namespace Authorization Rule used to send Diagnostics Data. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "eventhub_authorization_rule_id")

    @eventhub_authorization_rule_id.setter
    def eventhub_authorization_rule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eventhub_authorization_rule_id", value)

    @property
    @pulumi.getter(name="eventhubName")
    def eventhub_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Event Hub where Diagnostics Data should be sent. If not specified, the default Event Hub will be used. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "eventhub_name")

    @eventhub_name.setter
    def eventhub_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eventhub_name", value)

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of a Log Analytics Workspace where Diagnostics Data should be sent.
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_analytics_workspace_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Monitor Azure Active Directory Diagnostic Setting. Changing this forces a new Monitor Azure Active Directory Diagnostic Setting to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Storage Account where logs should be sent. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "storage_account_id")

    @storage_account_id.setter
    def storage_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_id", value)


@pulumi.input_type
class _AadDiagnosticSettingState:
    def __init__(__self__, *,
                 eventhub_authorization_rule_id: Optional[pulumi.Input[str]] = None,
                 eventhub_name: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 logs: Optional[pulumi.Input[Sequence[pulumi.Input['AadDiagnosticSettingLogArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AadDiagnosticSetting resources.
        :param pulumi.Input[str] eventhub_authorization_rule_id: Specifies the ID of an Event Hub Namespace Authorization Rule used to send Diagnostics Data. Changing this forces a new resource to be created.
        :param pulumi.Input[str] eventhub_name: Specifies the name of the Event Hub where Diagnostics Data should be sent. If not specified, the default Event Hub will be used. Changing this forces a new resource to be created.
        :param pulumi.Input[str] log_analytics_workspace_id: Specifies the ID of a Log Analytics Workspace where Diagnostics Data should be sent.
        :param pulumi.Input[Sequence[pulumi.Input['AadDiagnosticSettingLogArgs']]] logs: One or more `log` blocks as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Monitor Azure Active Directory Diagnostic Setting. Changing this forces a new Monitor Azure Active Directory Diagnostic Setting to be created.
        :param pulumi.Input[str] storage_account_id: The ID of the Storage Account where logs should be sent. Changing this forces a new resource to be created.
        """
        if eventhub_authorization_rule_id is not None:
            pulumi.set(__self__, "eventhub_authorization_rule_id", eventhub_authorization_rule_id)
        if eventhub_name is not None:
            pulumi.set(__self__, "eventhub_name", eventhub_name)
        if log_analytics_workspace_id is not None:
            pulumi.set(__self__, "log_analytics_workspace_id", log_analytics_workspace_id)
        if logs is not None:
            pulumi.set(__self__, "logs", logs)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if storage_account_id is not None:
            pulumi.set(__self__, "storage_account_id", storage_account_id)

    @property
    @pulumi.getter(name="eventhubAuthorizationRuleId")
    def eventhub_authorization_rule_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of an Event Hub Namespace Authorization Rule used to send Diagnostics Data. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "eventhub_authorization_rule_id")

    @eventhub_authorization_rule_id.setter
    def eventhub_authorization_rule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eventhub_authorization_rule_id", value)

    @property
    @pulumi.getter(name="eventhubName")
    def eventhub_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Event Hub where Diagnostics Data should be sent. If not specified, the default Event Hub will be used. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "eventhub_name")

    @eventhub_name.setter
    def eventhub_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eventhub_name", value)

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of a Log Analytics Workspace where Diagnostics Data should be sent.
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_analytics_workspace_id", value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AadDiagnosticSettingLogArgs']]]]:
        """
        One or more `log` blocks as defined below.
        """
        return pulumi.get(self, "logs")

    @logs.setter
    def logs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AadDiagnosticSettingLogArgs']]]]):
        pulumi.set(self, "logs", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Monitor Azure Active Directory Diagnostic Setting. Changing this forces a new Monitor Azure Active Directory Diagnostic Setting to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Storage Account where logs should be sent. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "storage_account_id")

    @storage_account_id.setter
    def storage_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_id", value)


class AadDiagnosticSetting(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 eventhub_authorization_rule_id: Optional[pulumi.Input[str]] = None,
                 eventhub_name: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 logs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AadDiagnosticSettingLogArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an Azure Active Directory Diagnostic Setting for Azure Monitor.

        !> **Authentication** The API for this resource does not support service principal authentication. This resource can only be used with Azure CLI authentication.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="west europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_kind="StorageV2",
            account_replication_type="LRS")
        example_aad_diagnostic_setting = azure.monitoring.AadDiagnosticSetting("exampleAadDiagnosticSetting",
            storage_account_id=example_account.id,
            logs=[
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="SignInLogs",
                    enabled=True,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(
                        enabled=True,
                        days=1,
                    ),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="AuditLogs",
                    enabled=True,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(
                        enabled=True,
                        days=1,
                    ),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="NonInteractiveUserSignInLogs",
                    enabled=True,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(
                        enabled=True,
                        days=1,
                    ),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="ServicePrincipalSignInLogs",
                    enabled=True,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(
                        enabled=True,
                        days=1,
                    ),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="ManagedIdentitySignInLogs",
                    enabled=False,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="ProvisioningLogs",
                    enabled=False,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="ADFSSignInLogs",
                    enabled=False,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(),
                ),
            ])
        ```

        ## Import

        Monitor Azure Active Directory Diagnostic Settings can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:monitoring/aadDiagnosticSetting:AadDiagnosticSetting example /providers/Microsoft.AADIAM/diagnosticSettings/setting1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] eventhub_authorization_rule_id: Specifies the ID of an Event Hub Namespace Authorization Rule used to send Diagnostics Data. Changing this forces a new resource to be created.
        :param pulumi.Input[str] eventhub_name: Specifies the name of the Event Hub where Diagnostics Data should be sent. If not specified, the default Event Hub will be used. Changing this forces a new resource to be created.
        :param pulumi.Input[str] log_analytics_workspace_id: Specifies the ID of a Log Analytics Workspace where Diagnostics Data should be sent.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AadDiagnosticSettingLogArgs']]]] logs: One or more `log` blocks as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Monitor Azure Active Directory Diagnostic Setting. Changing this forces a new Monitor Azure Active Directory Diagnostic Setting to be created.
        :param pulumi.Input[str] storage_account_id: The ID of the Storage Account where logs should be sent. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AadDiagnosticSettingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Azure Active Directory Diagnostic Setting for Azure Monitor.

        !> **Authentication** The API for this resource does not support service principal authentication. This resource can only be used with Azure CLI authentication.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="west europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_kind="StorageV2",
            account_replication_type="LRS")
        example_aad_diagnostic_setting = azure.monitoring.AadDiagnosticSetting("exampleAadDiagnosticSetting",
            storage_account_id=example_account.id,
            logs=[
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="SignInLogs",
                    enabled=True,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(
                        enabled=True,
                        days=1,
                    ),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="AuditLogs",
                    enabled=True,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(
                        enabled=True,
                        days=1,
                    ),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="NonInteractiveUserSignInLogs",
                    enabled=True,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(
                        enabled=True,
                        days=1,
                    ),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="ServicePrincipalSignInLogs",
                    enabled=True,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(
                        enabled=True,
                        days=1,
                    ),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="ManagedIdentitySignInLogs",
                    enabled=False,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="ProvisioningLogs",
                    enabled=False,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(),
                ),
                azure.monitoring.AadDiagnosticSettingLogArgs(
                    category="ADFSSignInLogs",
                    enabled=False,
                    retention_policy=azure.monitoring.AadDiagnosticSettingLogRetentionPolicyArgs(),
                ),
            ])
        ```

        ## Import

        Monitor Azure Active Directory Diagnostic Settings can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:monitoring/aadDiagnosticSetting:AadDiagnosticSetting example /providers/Microsoft.AADIAM/diagnosticSettings/setting1
        ```

        :param str resource_name: The name of the resource.
        :param AadDiagnosticSettingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AadDiagnosticSettingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 eventhub_authorization_rule_id: Optional[pulumi.Input[str]] = None,
                 eventhub_name: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 logs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AadDiagnosticSettingLogArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AadDiagnosticSettingArgs.__new__(AadDiagnosticSettingArgs)

            __props__.__dict__["eventhub_authorization_rule_id"] = eventhub_authorization_rule_id
            __props__.__dict__["eventhub_name"] = eventhub_name
            __props__.__dict__["log_analytics_workspace_id"] = log_analytics_workspace_id
            if logs is None and not opts.urn:
                raise TypeError("Missing required property 'logs'")
            __props__.__dict__["logs"] = logs
            __props__.__dict__["name"] = name
            __props__.__dict__["storage_account_id"] = storage_account_id
        super(AadDiagnosticSetting, __self__).__init__(
            'azure:monitoring/aadDiagnosticSetting:AadDiagnosticSetting',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            eventhub_authorization_rule_id: Optional[pulumi.Input[str]] = None,
            eventhub_name: Optional[pulumi.Input[str]] = None,
            log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
            logs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AadDiagnosticSettingLogArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            storage_account_id: Optional[pulumi.Input[str]] = None) -> 'AadDiagnosticSetting':
        """
        Get an existing AadDiagnosticSetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] eventhub_authorization_rule_id: Specifies the ID of an Event Hub Namespace Authorization Rule used to send Diagnostics Data. Changing this forces a new resource to be created.
        :param pulumi.Input[str] eventhub_name: Specifies the name of the Event Hub where Diagnostics Data should be sent. If not specified, the default Event Hub will be used. Changing this forces a new resource to be created.
        :param pulumi.Input[str] log_analytics_workspace_id: Specifies the ID of a Log Analytics Workspace where Diagnostics Data should be sent.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AadDiagnosticSettingLogArgs']]]] logs: One or more `log` blocks as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Monitor Azure Active Directory Diagnostic Setting. Changing this forces a new Monitor Azure Active Directory Diagnostic Setting to be created.
        :param pulumi.Input[str] storage_account_id: The ID of the Storage Account where logs should be sent. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AadDiagnosticSettingState.__new__(_AadDiagnosticSettingState)

        __props__.__dict__["eventhub_authorization_rule_id"] = eventhub_authorization_rule_id
        __props__.__dict__["eventhub_name"] = eventhub_name
        __props__.__dict__["log_analytics_workspace_id"] = log_analytics_workspace_id
        __props__.__dict__["logs"] = logs
        __props__.__dict__["name"] = name
        __props__.__dict__["storage_account_id"] = storage_account_id
        return AadDiagnosticSetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="eventhubAuthorizationRuleId")
    def eventhub_authorization_rule_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the ID of an Event Hub Namespace Authorization Rule used to send Diagnostics Data. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "eventhub_authorization_rule_id")

    @property
    @pulumi.getter(name="eventhubName")
    def eventhub_name(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the name of the Event Hub where Diagnostics Data should be sent. If not specified, the default Event Hub will be used. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "eventhub_name")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the ID of a Log Analytics Workspace where Diagnostics Data should be sent.
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @property
    @pulumi.getter
    def logs(self) -> pulumi.Output[Sequence['outputs.AadDiagnosticSettingLog']]:
        """
        One or more `log` blocks as defined below.
        """
        return pulumi.get(self, "logs")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Monitor Azure Active Directory Diagnostic Setting. Changing this forces a new Monitor Azure Active Directory Diagnostic Setting to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Storage Account where logs should be sent. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "storage_account_id")

