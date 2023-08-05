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
    'MonitorDatadogOrganization',
    'MonitorIdentity',
    'MonitorTagRuleLog',
    'MonitorTagRuleLogFilter',
    'MonitorTagRuleMetric',
    'MonitorTagRuleMetricFilter',
    'MonitorUser',
]

@pulumi.output_type
class MonitorDatadogOrganization(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "apiKey":
            suggest = "api_key"
        elif key == "applicationKey":
            suggest = "application_key"
        elif key == "enterpriseAppId":
            suggest = "enterprise_app_id"
        elif key == "linkingAuthCode":
            suggest = "linking_auth_code"
        elif key == "linkingClientId":
            suggest = "linking_client_id"
        elif key == "redirectUri":
            suggest = "redirect_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorDatadogOrganization. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorDatadogOrganization.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorDatadogOrganization.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 api_key: str,
                 application_key: str,
                 enterprise_app_id: Optional[str] = None,
                 id: Optional[str] = None,
                 linking_auth_code: Optional[str] = None,
                 linking_client_id: Optional[str] = None,
                 name: Optional[str] = None,
                 redirect_uri: Optional[str] = None):
        """
        :param str api_key: Api key associated to the Datadog organization. Changing this forces a new Datadog Monitor to be created.
        :param str application_key: Application key associated to the Datadog organization. Changing this forces a new Datadog Monitor to be created.
        :param str enterprise_app_id: The ID of the enterprise_app.
        :param str id: The ID of the Datadog Monitor.
        :param str linking_auth_code: The auth code used to linking to an existing Datadog organization. Changing this forces a new Datadog Monitor to be created.
        :param str linking_client_id: The ID of the linking_client. Changing this forces a new Datadog Monitor to be created.
        :param str name: The name of the user that will be associated with the Datadog Monitor. Changing this forces a new Datadog Monitor to be created.
        :param str redirect_uri: The redirect uri for linking. Changing this forces a new Datadog Monitor to be created.
        """
        pulumi.set(__self__, "api_key", api_key)
        pulumi.set(__self__, "application_key", application_key)
        if enterprise_app_id is not None:
            pulumi.set(__self__, "enterprise_app_id", enterprise_app_id)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if linking_auth_code is not None:
            pulumi.set(__self__, "linking_auth_code", linking_auth_code)
        if linking_client_id is not None:
            pulumi.set(__self__, "linking_client_id", linking_client_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if redirect_uri is not None:
            pulumi.set(__self__, "redirect_uri", redirect_uri)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> str:
        """
        Api key associated to the Datadog organization. Changing this forces a new Datadog Monitor to be created.
        """
        return pulumi.get(self, "api_key")

    @property
    @pulumi.getter(name="applicationKey")
    def application_key(self) -> str:
        """
        Application key associated to the Datadog organization. Changing this forces a new Datadog Monitor to be created.
        """
        return pulumi.get(self, "application_key")

    @property
    @pulumi.getter(name="enterpriseAppId")
    def enterprise_app_id(self) -> Optional[str]:
        """
        The ID of the enterprise_app.
        """
        return pulumi.get(self, "enterprise_app_id")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the Datadog Monitor.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="linkingAuthCode")
    def linking_auth_code(self) -> Optional[str]:
        """
        The auth code used to linking to an existing Datadog organization. Changing this forces a new Datadog Monitor to be created.
        """
        return pulumi.get(self, "linking_auth_code")

    @property
    @pulumi.getter(name="linkingClientId")
    def linking_client_id(self) -> Optional[str]:
        """
        The ID of the linking_client. Changing this forces a new Datadog Monitor to be created.
        """
        return pulumi.get(self, "linking_client_id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the user that will be associated with the Datadog Monitor. Changing this forces a new Datadog Monitor to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="redirectUri")
    def redirect_uri(self) -> Optional[str]:
        """
        The redirect uri for linking. Changing this forces a new Datadog Monitor to be created.
        """
        return pulumi.get(self, "redirect_uri")


@pulumi.output_type
class MonitorIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        :param str type: Specifies the identity type of the Datadog Monitor. At this time the only allowed value is `SystemAssigned`.
        :param str principal_id: The Principal ID for the Service Principal associated with the Identity of this Datadog Monitor.
        :param str tenant_id: The Tenant ID for the Service Principal associated with the Identity of this Datadog Monitor.
        """
        pulumi.set(__self__, "type", type)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the identity type of the Datadog Monitor. At this time the only allowed value is `SystemAssigned`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        """
        The Principal ID for the Service Principal associated with the Identity of this Datadog Monitor.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The Tenant ID for the Service Principal associated with the Identity of this Datadog Monitor.
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class MonitorTagRuleLog(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "aadLogEnabled":
            suggest = "aad_log_enabled"
        elif key == "resourceLogEnabled":
            suggest = "resource_log_enabled"
        elif key == "subscriptionLogEnabled":
            suggest = "subscription_log_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorTagRuleLog. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorTagRuleLog.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorTagRuleLog.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 aad_log_enabled: Optional[bool] = None,
                 filters: Optional[Sequence['outputs.MonitorTagRuleLogFilter']] = None,
                 resource_log_enabled: Optional[bool] = None,
                 subscription_log_enabled: Optional[bool] = None):
        """
        :param bool aad_log_enabled: Whether AAD logs should be sent for the Monitor resource?
        :param Sequence['MonitorTagRuleLogFilterArgs'] filters: A `filter` block as defined below.
        :param bool resource_log_enabled: Whether Azure resource logs should be sent for the Monitor resource?
        :param bool subscription_log_enabled: Whether Azure subscription logs should be sent for the Monitor resource?
        """
        if aad_log_enabled is not None:
            pulumi.set(__self__, "aad_log_enabled", aad_log_enabled)
        if filters is not None:
            pulumi.set(__self__, "filters", filters)
        if resource_log_enabled is not None:
            pulumi.set(__self__, "resource_log_enabled", resource_log_enabled)
        if subscription_log_enabled is not None:
            pulumi.set(__self__, "subscription_log_enabled", subscription_log_enabled)

    @property
    @pulumi.getter(name="aadLogEnabled")
    def aad_log_enabled(self) -> Optional[bool]:
        """
        Whether AAD logs should be sent for the Monitor resource?
        """
        return pulumi.get(self, "aad_log_enabled")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.MonitorTagRuleLogFilter']]:
        """
        A `filter` block as defined below.
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="resourceLogEnabled")
    def resource_log_enabled(self) -> Optional[bool]:
        """
        Whether Azure resource logs should be sent for the Monitor resource?
        """
        return pulumi.get(self, "resource_log_enabled")

    @property
    @pulumi.getter(name="subscriptionLogEnabled")
    def subscription_log_enabled(self) -> Optional[bool]:
        """
        Whether Azure subscription logs should be sent for the Monitor resource?
        """
        return pulumi.get(self, "subscription_log_enabled")


@pulumi.output_type
class MonitorTagRuleLogFilter(dict):
    def __init__(__self__, *,
                 action: str,
                 name: str,
                 value: str):
        """
        :param str action: Allowed values Include or Exclude.
        :param str name: Name of the Tag.
        :param str value: Value of the Tag.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def action(self) -> str:
        """
        Allowed values Include or Exclude.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Tag.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the Tag.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class MonitorTagRuleMetric(dict):
    def __init__(__self__, *,
                 filters: Optional[Sequence['outputs.MonitorTagRuleMetricFilter']] = None):
        """
        :param Sequence['MonitorTagRuleMetricFilterArgs'] filters: A `filter` block as defined below.
        """
        if filters is not None:
            pulumi.set(__self__, "filters", filters)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.MonitorTagRuleMetricFilter']]:
        """
        A `filter` block as defined below.
        """
        return pulumi.get(self, "filters")


@pulumi.output_type
class MonitorTagRuleMetricFilter(dict):
    def __init__(__self__, *,
                 action: str,
                 name: str,
                 value: str):
        """
        :param str action: Allowed values Include or Exclude.
        :param str name: Name of the Tag.
        :param str value: Value of the Tag.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def action(self) -> str:
        """
        Allowed values Include or Exclude.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Tag.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the Tag.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class MonitorUser(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "phoneNumber":
            suggest = "phone_number"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorUser. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorUser.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorUser.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 email: str,
                 name: str,
                 phone_number: Optional[str] = None):
        """
        :param str email: Email of the user used by Datadog for contacting them if needed. Changing this forces a new Datadog Monitor to be created.
        :param str name: The name which should be used for this user_info.
        :param str phone_number: Phone number of the user used by Datadog for contacting them if needed.
        """
        pulumi.set(__self__, "email", email)
        pulumi.set(__self__, "name", name)
        if phone_number is not None:
            pulumi.set(__self__, "phone_number", phone_number)

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        Email of the user used by Datadog for contacting them if needed. Changing this forces a new Datadog Monitor to be created.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name which should be used for this user_info.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="phoneNumber")
    def phone_number(self) -> Optional[str]:
        """
        Phone number of the user used by Datadog for contacting them if needed.
        """
        return pulumi.get(self, "phone_number")


