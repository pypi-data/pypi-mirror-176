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
    'FlexibleServerHighAvailabilityArgs',
    'FlexibleServerMaintenanceWindowArgs',
    'FlexibleServerStorageArgs',
    'ServerIdentityArgs',
    'ServerThreatDetectionPolicyArgs',
]

@pulumi.input_type
class FlexibleServerHighAvailabilityArgs:
    def __init__(__self__, *,
                 mode: pulumi.Input[str],
                 standby_availability_zone: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] mode: The high availability mode for the MySQL Flexible Server. Possibles values are `SameZone` and `ZoneRedundant`.
        :param pulumi.Input[str] standby_availability_zone: Specifies the Availability Zone in which the standby Flexible Server should be located. Possible values are `1`, `2` and `3`.
        """
        pulumi.set(__self__, "mode", mode)
        if standby_availability_zone is not None:
            pulumi.set(__self__, "standby_availability_zone", standby_availability_zone)

    @property
    @pulumi.getter
    def mode(self) -> pulumi.Input[str]:
        """
        The high availability mode for the MySQL Flexible Server. Possibles values are `SameZone` and `ZoneRedundant`.
        """
        return pulumi.get(self, "mode")

    @mode.setter
    def mode(self, value: pulumi.Input[str]):
        pulumi.set(self, "mode", value)

    @property
    @pulumi.getter(name="standbyAvailabilityZone")
    def standby_availability_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Availability Zone in which the standby Flexible Server should be located. Possible values are `1`, `2` and `3`.
        """
        return pulumi.get(self, "standby_availability_zone")

    @standby_availability_zone.setter
    def standby_availability_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "standby_availability_zone", value)


@pulumi.input_type
class FlexibleServerMaintenanceWindowArgs:
    def __init__(__self__, *,
                 day_of_week: Optional[pulumi.Input[int]] = None,
                 start_hour: Optional[pulumi.Input[int]] = None,
                 start_minute: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] day_of_week: The day of week for maintenance window. Defaults to `0`.
        :param pulumi.Input[int] start_hour: The start hour for maintenance window. Defaults to `0`.
        :param pulumi.Input[int] start_minute: The start minute for maintenance window. Defaults to `0`.
        """
        if day_of_week is not None:
            pulumi.set(__self__, "day_of_week", day_of_week)
        if start_hour is not None:
            pulumi.set(__self__, "start_hour", start_hour)
        if start_minute is not None:
            pulumi.set(__self__, "start_minute", start_minute)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> Optional[pulumi.Input[int]]:
        """
        The day of week for maintenance window. Defaults to `0`.
        """
        return pulumi.get(self, "day_of_week")

    @day_of_week.setter
    def day_of_week(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "day_of_week", value)

    @property
    @pulumi.getter(name="startHour")
    def start_hour(self) -> Optional[pulumi.Input[int]]:
        """
        The start hour for maintenance window. Defaults to `0`.
        """
        return pulumi.get(self, "start_hour")

    @start_hour.setter
    def start_hour(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "start_hour", value)

    @property
    @pulumi.getter(name="startMinute")
    def start_minute(self) -> Optional[pulumi.Input[int]]:
        """
        The start minute for maintenance window. Defaults to `0`.
        """
        return pulumi.get(self, "start_minute")

    @start_minute.setter
    def start_minute(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "start_minute", value)


@pulumi.input_type
class FlexibleServerStorageArgs:
    def __init__(__self__, *,
                 auto_grow_enabled: Optional[pulumi.Input[bool]] = None,
                 iops: Optional[pulumi.Input[int]] = None,
                 size_gb: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[bool] auto_grow_enabled: Should Storage Auto Grow be enabled? Defaults to `true`.
        :param pulumi.Input[int] iops: The storage IOPS for the MySQL Flexible Server. Possible values are between `360` and `20000`.
        :param pulumi.Input[int] size_gb: The max storage allowed for the MySQL Flexible Server. Possible values are between `20` and `16384`.
        """
        if auto_grow_enabled is not None:
            pulumi.set(__self__, "auto_grow_enabled", auto_grow_enabled)
        if iops is not None:
            pulumi.set(__self__, "iops", iops)
        if size_gb is not None:
            pulumi.set(__self__, "size_gb", size_gb)

    @property
    @pulumi.getter(name="autoGrowEnabled")
    def auto_grow_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should Storage Auto Grow be enabled? Defaults to `true`.
        """
        return pulumi.get(self, "auto_grow_enabled")

    @auto_grow_enabled.setter
    def auto_grow_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_grow_enabled", value)

    @property
    @pulumi.getter
    def iops(self) -> Optional[pulumi.Input[int]]:
        """
        The storage IOPS for the MySQL Flexible Server. Possible values are between `360` and `20000`.
        """
        return pulumi.get(self, "iops")

    @iops.setter
    def iops(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "iops", value)

    @property
    @pulumi.getter(name="sizeGb")
    def size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        The max storage allowed for the MySQL Flexible Server. Possible values are between `20` and `16384`.
        """
        return pulumi.get(self, "size_gb")

    @size_gb.setter
    def size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size_gb", value)


@pulumi.input_type
class ServerIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] type: Specifies the type of Managed Service Identity that should be configured on this MySQL Server. The only possible value is `SystemAssigned`.
        :param pulumi.Input[str] principal_id: The Principal ID associated with this Managed Service Identity.
        :param pulumi.Input[str] tenant_id: The Tenant ID associated with this Managed Service Identity.
        """
        pulumi.set(__self__, "type", type)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Specifies the type of Managed Service Identity that should be configured on this MySQL Server. The only possible value is `SystemAssigned`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Principal ID associated with this Managed Service Identity.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Tenant ID associated with this Managed Service Identity.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


@pulumi.input_type
class ServerThreatDetectionPolicyArgs:
    def __init__(__self__, *,
                 disabled_alerts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 email_account_admins: Optional[pulumi.Input[bool]] = None,
                 email_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 retention_days: Optional[pulumi.Input[int]] = None,
                 storage_account_access_key: Optional[pulumi.Input[str]] = None,
                 storage_endpoint: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] disabled_alerts: Specifies a list of alerts which should be disabled. Possible values include `Access_Anomaly`, `Sql_Injection` and `Sql_Injection_Vulnerability`.
        :param pulumi.Input[bool] email_account_admins: Should the account administrators be emailed when this alert is triggered?
        :param pulumi.Input[Sequence[pulumi.Input[str]]] email_addresses: A list of email addresses which alerts should be sent to.
        :param pulumi.Input[bool] enabled: Is the policy enabled?
        :param pulumi.Input[int] retention_days: Specifies the number of days to keep in the Threat Detection audit logs.
        :param pulumi.Input[str] storage_account_access_key: Specifies the identifier key of the Threat Detection audit storage account.
        :param pulumi.Input[str] storage_endpoint: Specifies the blob storage endpoint (e.g. <https://example.blob.core.windows.net>). This blob storage will hold all Threat Detection audit logs.
        """
        if disabled_alerts is not None:
            pulumi.set(__self__, "disabled_alerts", disabled_alerts)
        if email_account_admins is not None:
            pulumi.set(__self__, "email_account_admins", email_account_admins)
        if email_addresses is not None:
            pulumi.set(__self__, "email_addresses", email_addresses)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if retention_days is not None:
            pulumi.set(__self__, "retention_days", retention_days)
        if storage_account_access_key is not None:
            pulumi.set(__self__, "storage_account_access_key", storage_account_access_key)
        if storage_endpoint is not None:
            pulumi.set(__self__, "storage_endpoint", storage_endpoint)

    @property
    @pulumi.getter(name="disabledAlerts")
    def disabled_alerts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of alerts which should be disabled. Possible values include `Access_Anomaly`, `Sql_Injection` and `Sql_Injection_Vulnerability`.
        """
        return pulumi.get(self, "disabled_alerts")

    @disabled_alerts.setter
    def disabled_alerts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "disabled_alerts", value)

    @property
    @pulumi.getter(name="emailAccountAdmins")
    def email_account_admins(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the account administrators be emailed when this alert is triggered?
        """
        return pulumi.get(self, "email_account_admins")

    @email_account_admins.setter
    def email_account_admins(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "email_account_admins", value)

    @property
    @pulumi.getter(name="emailAddresses")
    def email_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of email addresses which alerts should be sent to.
        """
        return pulumi.get(self, "email_addresses")

    @email_addresses.setter
    def email_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "email_addresses", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the policy enabled?
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="retentionDays")
    def retention_days(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days to keep in the Threat Detection audit logs.
        """
        return pulumi.get(self, "retention_days")

    @retention_days.setter
    def retention_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_days", value)

    @property
    @pulumi.getter(name="storageAccountAccessKey")
    def storage_account_access_key(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier key of the Threat Detection audit storage account.
        """
        return pulumi.get(self, "storage_account_access_key")

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_access_key", value)

    @property
    @pulumi.getter(name="storageEndpoint")
    def storage_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the blob storage endpoint (e.g. <https://example.blob.core.windows.net>). This blob storage will hold all Threat Detection audit logs.
        """
        return pulumi.get(self, "storage_endpoint")

    @storage_endpoint.setter
    def storage_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_endpoint", value)


