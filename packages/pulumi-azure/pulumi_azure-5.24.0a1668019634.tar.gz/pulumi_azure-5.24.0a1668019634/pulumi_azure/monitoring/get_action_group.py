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

__all__ = [
    'GetActionGroupResult',
    'AwaitableGetActionGroupResult',
    'get_action_group',
    'get_action_group_output',
]

@pulumi.output_type
class GetActionGroupResult:
    """
    A collection of values returned by getActionGroup.
    """
    def __init__(__self__, arm_role_receivers=None, automation_runbook_receivers=None, azure_app_push_receivers=None, azure_function_receivers=None, email_receivers=None, enabled=None, event_hub_receivers=None, id=None, itsm_receivers=None, logic_app_receivers=None, name=None, resource_group_name=None, short_name=None, sms_receivers=None, voice_receivers=None, webhook_receivers=None):
        if arm_role_receivers and not isinstance(arm_role_receivers, list):
            raise TypeError("Expected argument 'arm_role_receivers' to be a list")
        pulumi.set(__self__, "arm_role_receivers", arm_role_receivers)
        if automation_runbook_receivers and not isinstance(automation_runbook_receivers, list):
            raise TypeError("Expected argument 'automation_runbook_receivers' to be a list")
        pulumi.set(__self__, "automation_runbook_receivers", automation_runbook_receivers)
        if azure_app_push_receivers and not isinstance(azure_app_push_receivers, list):
            raise TypeError("Expected argument 'azure_app_push_receivers' to be a list")
        pulumi.set(__self__, "azure_app_push_receivers", azure_app_push_receivers)
        if azure_function_receivers and not isinstance(azure_function_receivers, list):
            raise TypeError("Expected argument 'azure_function_receivers' to be a list")
        pulumi.set(__self__, "azure_function_receivers", azure_function_receivers)
        if email_receivers and not isinstance(email_receivers, list):
            raise TypeError("Expected argument 'email_receivers' to be a list")
        pulumi.set(__self__, "email_receivers", email_receivers)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if event_hub_receivers and not isinstance(event_hub_receivers, list):
            raise TypeError("Expected argument 'event_hub_receivers' to be a list")
        pulumi.set(__self__, "event_hub_receivers", event_hub_receivers)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if itsm_receivers and not isinstance(itsm_receivers, list):
            raise TypeError("Expected argument 'itsm_receivers' to be a list")
        pulumi.set(__self__, "itsm_receivers", itsm_receivers)
        if logic_app_receivers and not isinstance(logic_app_receivers, list):
            raise TypeError("Expected argument 'logic_app_receivers' to be a list")
        pulumi.set(__self__, "logic_app_receivers", logic_app_receivers)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if short_name and not isinstance(short_name, str):
            raise TypeError("Expected argument 'short_name' to be a str")
        pulumi.set(__self__, "short_name", short_name)
        if sms_receivers and not isinstance(sms_receivers, list):
            raise TypeError("Expected argument 'sms_receivers' to be a list")
        pulumi.set(__self__, "sms_receivers", sms_receivers)
        if voice_receivers and not isinstance(voice_receivers, list):
            raise TypeError("Expected argument 'voice_receivers' to be a list")
        pulumi.set(__self__, "voice_receivers", voice_receivers)
        if webhook_receivers and not isinstance(webhook_receivers, list):
            raise TypeError("Expected argument 'webhook_receivers' to be a list")
        pulumi.set(__self__, "webhook_receivers", webhook_receivers)

    @property
    @pulumi.getter(name="armRoleReceivers")
    def arm_role_receivers(self) -> Sequence['outputs.GetActionGroupArmRoleReceiverResult']:
        """
        One or more `arm_role_receiver` blocks as defined below.
        """
        return pulumi.get(self, "arm_role_receivers")

    @property
    @pulumi.getter(name="automationRunbookReceivers")
    def automation_runbook_receivers(self) -> Sequence['outputs.GetActionGroupAutomationRunbookReceiverResult']:
        """
        One or more `automation_runbook_receiver` blocks as defined below.
        """
        return pulumi.get(self, "automation_runbook_receivers")

    @property
    @pulumi.getter(name="azureAppPushReceivers")
    def azure_app_push_receivers(self) -> Sequence['outputs.GetActionGroupAzureAppPushReceiverResult']:
        """
        One or more `azure_app_push_receiver` blocks as defined below.
        """
        return pulumi.get(self, "azure_app_push_receivers")

    @property
    @pulumi.getter(name="azureFunctionReceivers")
    def azure_function_receivers(self) -> Sequence['outputs.GetActionGroupAzureFunctionReceiverResult']:
        """
        One or more `azure_function_receiver` blocks as defined below.
        """
        return pulumi.get(self, "azure_function_receivers")

    @property
    @pulumi.getter(name="emailReceivers")
    def email_receivers(self) -> Sequence['outputs.GetActionGroupEmailReceiverResult']:
        """
        One or more `email_receiver` blocks as defined below.
        """
        return pulumi.get(self, "email_receivers")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Whether this action group is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="eventHubReceivers")
    def event_hub_receivers(self) -> Sequence['outputs.GetActionGroupEventHubReceiverResult']:
        """
        One or more `event_hub_receiver` blocks as defined below.
        """
        return pulumi.get(self, "event_hub_receivers")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="itsmReceivers")
    def itsm_receivers(self) -> Sequence['outputs.GetActionGroupItsmReceiverResult']:
        """
        One or more `itsm_receiver` blocks as defined below.
        """
        return pulumi.get(self, "itsm_receivers")

    @property
    @pulumi.getter(name="logicAppReceivers")
    def logic_app_receivers(self) -> Sequence['outputs.GetActionGroupLogicAppReceiverResult']:
        """
        One or more `logic_app_receiver` blocks as defined below.
        """
        return pulumi.get(self, "logic_app_receivers")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the webhook receiver.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> str:
        """
        The short name of the action group.
        """
        return pulumi.get(self, "short_name")

    @property
    @pulumi.getter(name="smsReceivers")
    def sms_receivers(self) -> Sequence['outputs.GetActionGroupSmsReceiverResult']:
        """
        One or more `sms_receiver` blocks as defined below.
        """
        return pulumi.get(self, "sms_receivers")

    @property
    @pulumi.getter(name="voiceReceivers")
    def voice_receivers(self) -> Sequence['outputs.GetActionGroupVoiceReceiverResult']:
        """
        One or more `voice_receiver` blocks as defined below.
        """
        return pulumi.get(self, "voice_receivers")

    @property
    @pulumi.getter(name="webhookReceivers")
    def webhook_receivers(self) -> Sequence['outputs.GetActionGroupWebhookReceiverResult']:
        """
        One or more `webhook_receiver` blocks as defined below.
        """
        return pulumi.get(self, "webhook_receivers")


class AwaitableGetActionGroupResult(GetActionGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetActionGroupResult(
            arm_role_receivers=self.arm_role_receivers,
            automation_runbook_receivers=self.automation_runbook_receivers,
            azure_app_push_receivers=self.azure_app_push_receivers,
            azure_function_receivers=self.azure_function_receivers,
            email_receivers=self.email_receivers,
            enabled=self.enabled,
            event_hub_receivers=self.event_hub_receivers,
            id=self.id,
            itsm_receivers=self.itsm_receivers,
            logic_app_receivers=self.logic_app_receivers,
            name=self.name,
            resource_group_name=self.resource_group_name,
            short_name=self.short_name,
            sms_receivers=self.sms_receivers,
            voice_receivers=self.voice_receivers,
            webhook_receivers=self.webhook_receivers)


def get_action_group(name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetActionGroupResult:
    """
    Use this data source to access the properties of an Action Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.monitoring.get_action_group(resource_group_name="example-rg",
        name="tfex-actiongroup")
    pulumi.export("actionGroupId", example.id)
    ```


    :param str name: Specifies the name of the Action Group.
    :param str resource_group_name: Specifies the name of the resource group the Action Group is located in.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:monitoring/getActionGroup:getActionGroup', __args__, opts=opts, typ=GetActionGroupResult).value

    return AwaitableGetActionGroupResult(
        arm_role_receivers=__ret__.arm_role_receivers,
        automation_runbook_receivers=__ret__.automation_runbook_receivers,
        azure_app_push_receivers=__ret__.azure_app_push_receivers,
        azure_function_receivers=__ret__.azure_function_receivers,
        email_receivers=__ret__.email_receivers,
        enabled=__ret__.enabled,
        event_hub_receivers=__ret__.event_hub_receivers,
        id=__ret__.id,
        itsm_receivers=__ret__.itsm_receivers,
        logic_app_receivers=__ret__.logic_app_receivers,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        short_name=__ret__.short_name,
        sms_receivers=__ret__.sms_receivers,
        voice_receivers=__ret__.voice_receivers,
        webhook_receivers=__ret__.webhook_receivers)


@_utilities.lift_output_func(get_action_group)
def get_action_group_output(name: Optional[pulumi.Input[str]] = None,
                            resource_group_name: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetActionGroupResult]:
    """
    Use this data source to access the properties of an Action Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.monitoring.get_action_group(resource_group_name="example-rg",
        name="tfex-actiongroup")
    pulumi.export("actionGroupId", example.id)
    ```


    :param str name: Specifies the name of the Action Group.
    :param str resource_group_name: Specifies the name of the resource group the Action Group is located in.
    """
    ...
