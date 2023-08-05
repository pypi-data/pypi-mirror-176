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
    'ElasticsearchLogs',
    'ElasticsearchLogsFilteringTag',
    'GetElasticsearchLogResult',
    'GetElasticsearchLogFilteringTagResult',
]

@pulumi.output_type
class ElasticsearchLogs(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "filteringTags":
            suggest = "filtering_tags"
        elif key == "sendActivityLogs":
            suggest = "send_activity_logs"
        elif key == "sendAzureadLogs":
            suggest = "send_azuread_logs"
        elif key == "sendSubscriptionLogs":
            suggest = "send_subscription_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ElasticsearchLogs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ElasticsearchLogs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ElasticsearchLogs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 filtering_tags: Optional[Sequence['outputs.ElasticsearchLogsFilteringTag']] = None,
                 send_activity_logs: Optional[bool] = None,
                 send_azuread_logs: Optional[bool] = None,
                 send_subscription_logs: Optional[bool] = None):
        """
        :param Sequence['ElasticsearchLogsFilteringTagArgs'] filtering_tags: A list of `filtering_tag` blocks as defined above.
        :param bool send_activity_logs: Specifies if the Azure Activity Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        :param bool send_azuread_logs: Specifies if the AzureAD Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        :param bool send_subscription_logs: Specifies if the Azure Subscription Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
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
    def filtering_tags(self) -> Optional[Sequence['outputs.ElasticsearchLogsFilteringTag']]:
        """
        A list of `filtering_tag` blocks as defined above.
        """
        return pulumi.get(self, "filtering_tags")

    @property
    @pulumi.getter(name="sendActivityLogs")
    def send_activity_logs(self) -> Optional[bool]:
        """
        Specifies if the Azure Activity Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        """
        return pulumi.get(self, "send_activity_logs")

    @property
    @pulumi.getter(name="sendAzureadLogs")
    def send_azuread_logs(self) -> Optional[bool]:
        """
        Specifies if the AzureAD Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        """
        return pulumi.get(self, "send_azuread_logs")

    @property
    @pulumi.getter(name="sendSubscriptionLogs")
    def send_subscription_logs(self) -> Optional[bool]:
        """
        Specifies if the Azure Subscription Logs should be sent to the Elasticsearch cluster. Defaults to `false`.
        """
        return pulumi.get(self, "send_subscription_logs")


@pulumi.output_type
class ElasticsearchLogsFilteringTag(dict):
    def __init__(__self__, *,
                 action: str,
                 name: str,
                 value: str):
        """
        :param str action: Specifies the type of action which should be taken when the Tag matches the `name` and `value`. Possible values are `Exclude` and `Include`.
        :param str name: Specifies the name (key) of the Tag which should be filtered.
        :param str value: Specifies the value of the Tag which should be filtered.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def action(self) -> str:
        """
        Specifies the type of action which should be taken when the Tag matches the `name` and `value`. Possible values are `Exclude` and `Include`.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name (key) of the Tag which should be filtered.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Specifies the value of the Tag which should be filtered.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class GetElasticsearchLogResult(dict):
    def __init__(__self__, *,
                 filtering_tags: Sequence['outputs.GetElasticsearchLogFilteringTagResult'],
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
    def filtering_tags(self) -> Sequence['outputs.GetElasticsearchLogFilteringTagResult']:
        """
        A list of `filtering_tag` blocks as defined above.
        """
        return pulumi.get(self, "filtering_tags")

    @property
    @pulumi.getter(name="sendActivityLogs")
    def send_activity_logs(self) -> bool:
        """
        Should the Azure Activity Logs should be sent to the Elasticsearch cluster?
        """
        return pulumi.get(self, "send_activity_logs")

    @property
    @pulumi.getter(name="sendAzureadLogs")
    def send_azuread_logs(self) -> bool:
        """
        Should the AzureAD Logs should be sent to the Elasticsearch cluster?
        """
        return pulumi.get(self, "send_azuread_logs")

    @property
    @pulumi.getter(name="sendSubscriptionLogs")
    def send_subscription_logs(self) -> bool:
        """
        Should the Azure Subscription Logs should be sent to the Elasticsearch cluster?
        """
        return pulumi.get(self, "send_subscription_logs")


@pulumi.output_type
class GetElasticsearchLogFilteringTagResult(dict):
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

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Elasticsearch resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the Tag which should be filtered.
        """
        return pulumi.get(self, "value")


