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
    'ElasticsearchLogsArgs',
    'ElasticsearchLogsFilteringTagArgs',
    'GetElasticsearchLogArgs',
    'GetElasticsearchLogFilteringTagArgs',
]

@pulumi.input_type
class ElasticsearchLogsArgs:
    def __init__(__self__, *,
                 filtering_tags: Optional[pulumi.Input[Sequence[pulumi.Input['ElasticsearchLogsFilteringTagArgs']]]] = None,
                 send_activity_logs: Optional[pulumi.Input[bool]] = None,
                 send_azuread_logs: Optional[pulumi.Input[bool]] = None,
                 send_subscription_logs: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['ElasticsearchLogsFilteringTagArgs']]] filtering_tags: A list of `filtering_tag` blocks as defined above.
        :param pulumi.Input[bool] send_activity_logs: Specifies if the Azure Activity Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        :param pulumi.Input[bool] send_azuread_logs: Specifies if the AzureAD Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        :param pulumi.Input[bool] send_subscription_logs: Specifies if the Azure Subscription Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        """
        if filtering_tags is not None:
            pulumi.set(__self__, "filtering_tags", filtering_tags)
        if send_activity_logs is not None:
            pulumi.set(__self__, "send_activity_logs", send_activity_logs)
        if send_azuread_logs is not None:
            pulumi.set(__self__, "send_azuread_logs", send_azuread_logs)
        if send_subscription_logs is not None:
            pulumi.set(__self__, "send_subscription_logs", send_subscription_logs)

    @property
    @pulumi.getter(name="filteringTags")
    def filtering_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ElasticsearchLogsFilteringTagArgs']]]]:
        """
        A list of `filtering_tag` blocks as defined above.
        """
        return pulumi.get(self, "filtering_tags")

    @filtering_tags.setter
    def filtering_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ElasticsearchLogsFilteringTagArgs']]]]):
        pulumi.set(self, "filtering_tags", value)

    @property
    @pulumi.getter(name="sendActivityLogs")
    def send_activity_logs(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if the Azure Activity Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        """
        return pulumi.get(self, "send_activity_logs")

    @send_activity_logs.setter
    def send_activity_logs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_activity_logs", value)

    @property
    @pulumi.getter(name="sendAzureadLogs")
    def send_azuread_logs(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if the AzureAD Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        """
        return pulumi.get(self, "send_azuread_logs")

    @send_azuread_logs.setter
    def send_azuread_logs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_azuread_logs", value)

    @property
    @pulumi.getter(name="sendSubscriptionLogs")
    def send_subscription_logs(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if the Azure Subscription Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        """
        return pulumi.get(self, "send_subscription_logs")

    @send_subscription_logs.setter
    def send_subscription_logs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_subscription_logs", value)


@pulumi.input_type
class ElasticsearchLogsFilteringTagArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] action: Specifies the type of action which should be taken when the Tag matches the `name` and `value`. Possible values are `Exclude` and `Include`.
        :param pulumi.Input[str] name: Specifies the name (key) of the Tag which should be filtered.
        :param pulumi.Input[str] value: Specifies the value of the Tag which should be filtered.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        Specifies the type of action which should be taken when the Tag matches the `name` and `value`. Possible values are `Exclude` and `Include`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Specifies the name (key) of the Tag which should be filtered.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Specifies the value of the Tag which should be filtered.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class GetElasticsearchLogArgs:
    def __init__(__self__, *,
                 filtering_tags: Sequence['GetElasticsearchLogFilteringTagArgs'],
                 send_activity_logs: bool,
                 send_azuread_logs: bool,
                 send_subscription_logs: bool):
        """
        :param Sequence['GetElasticsearchLogFilteringTagArgs'] filtering_tags: A list of `filtering_tag` blocks as defined above.
        :param bool send_activity_logs: Should the Azure Activity Logs should be sent to the Elasticsearch cluster?
        :param bool send_azuread_logs: Should the AzureAD Logs should be sent to the Elasticsearch cluster?
        :param bool send_subscription_logs: Should the Azure Subscription Logs should be sent to the Elasticsearch cluster?
        """
        pulumi.set(__self__, "filtering_tags", filtering_tags)
        pulumi.set(__self__, "send_activity_logs", send_activity_logs)
        pulumi.set(__self__, "send_azuread_logs", send_azuread_logs)
        pulumi.set(__self__, "send_subscription_logs", send_subscription_logs)

    @property
    @pulumi.getter(name="filteringTags")
    def filtering_tags(self) -> Sequence['GetElasticsearchLogFilteringTagArgs']:
        """
        A list of `filtering_tag` blocks as defined above.
        """
        return pulumi.get(self, "filtering_tags")

    @filtering_tags.setter
    def filtering_tags(self, value: Sequence['GetElasticsearchLogFilteringTagArgs']):
        pulumi.set(self, "filtering_tags", value)

    @property
    @pulumi.getter(name="sendActivityLogs")
    def send_activity_logs(self) -> bool:
        """
        Should the Azure Activity Logs should be sent to the Elasticsearch cluster?
        """
        return pulumi.get(self, "send_activity_logs")

    @send_activity_logs.setter
    def send_activity_logs(self, value: bool):
        pulumi.set(self, "send_activity_logs", value)

    @property
    @pulumi.getter(name="sendAzureadLogs")
    def send_azuread_logs(self) -> bool:
        """
        Should the AzureAD Logs should be sent to the Elasticsearch cluster?
        """
        return pulumi.get(self, "send_azuread_logs")

    @send_azuread_logs.setter
    def send_azuread_logs(self, value: bool):
        pulumi.set(self, "send_azuread_logs", value)

    @property
    @pulumi.getter(name="sendSubscriptionLogs")
    def send_subscription_logs(self) -> bool:
        """
        Should the Azure Subscription Logs should be sent to the Elasticsearch cluster?
        """
        return pulumi.get(self, "send_subscription_logs")

    @send_subscription_logs.setter
    def send_subscription_logs(self, value: bool):
        pulumi.set(self, "send_subscription_logs", value)


@pulumi.input_type
class GetElasticsearchLogFilteringTagArgs:
    def __init__(__self__, *,
                 action: str,
                 name: str,
                 value: str):
        """
        :param str action: The type of action which is taken when the Tag matches the `name` and `value`.
        :param str name: The name of the Elasticsearch resource.
        :param str value: The value of the Tag which should be filtered.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def action(self) -> str:
        """
        The type of action which is taken when the Tag matches the `name` and `value`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: str):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Elasticsearch resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: str):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the Tag which should be filtered.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: str):
        pulumi.set(self, "value", value)


