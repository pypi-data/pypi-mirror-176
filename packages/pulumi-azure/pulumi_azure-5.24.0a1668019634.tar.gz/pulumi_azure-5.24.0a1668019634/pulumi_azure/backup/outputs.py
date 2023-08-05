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
    'PolicyFileShareBackup',
    'PolicyFileShareRetentionDaily',
    'PolicyFileShareRetentionMonthly',
    'PolicyFileShareRetentionWeekly',
    'PolicyFileShareRetentionYearly',
    'PolicyVMBackup',
    'PolicyVMRetentionDaily',
    'PolicyVMRetentionMonthly',
    'PolicyVMRetentionWeekly',
    'PolicyVMRetentionYearly',
    'PolicyVMWorkloadProtectionPolicy',
    'PolicyVMWorkloadProtectionPolicyBackup',
    'PolicyVMWorkloadProtectionPolicyRetentionDaily',
    'PolicyVMWorkloadProtectionPolicyRetentionMonthly',
    'PolicyVMWorkloadProtectionPolicyRetentionWeekly',
    'PolicyVMWorkloadProtectionPolicyRetentionYearly',
    'PolicyVMWorkloadProtectionPolicySimpleRetention',
    'PolicyVMWorkloadSettings',
]

@pulumi.output_type
class PolicyFileShareBackup(dict):
    def __init__(__self__, *,
                 frequency: str,
                 time: str):
        """
        :param str frequency: Sets the backup frequency. Currently, only `Daily` is supported
        :param str time: The time of day to perform the backup in 24-hour format. Times must be either on the hour or half hour (e.g. 12:00, 12:30, 13:00, etc.)
        """
        pulumi.set(__self__, "frequency", frequency)
        pulumi.set(__self__, "time", time)

    @property
    @pulumi.getter
    def frequency(self) -> str:
        """
        Sets the backup frequency. Currently, only `Daily` is supported
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def time(self) -> str:
        """
        The time of day to perform the backup in 24-hour format. Times must be either on the hour or half hour (e.g. 12:00, 12:30, 13:00, etc.)
        """
        return pulumi.get(self, "time")


@pulumi.output_type
class PolicyFileShareRetentionDaily(dict):
    def __init__(__self__, *,
                 count: int):
        """
        :param int count: The number of yearly backups to keep. Must be between `1` and `10`
        """
        pulumi.set(__self__, "count", count)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Must be between `1` and `10`
        """
        return pulumi.get(self, "count")


@pulumi.output_type
class PolicyFileShareRetentionMonthly(dict):
    def __init__(__self__, *,
                 count: int,
                 weekdays: Sequence[str],
                 weeks: Sequence[str]):
        """
        :param int count: The number of yearly backups to keep. Must be between `1` and `10`
        :param Sequence[str] weekdays: The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        :param Sequence[str] weeks: The weeks of the month to retain backups of. Must be one of `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "weekdays", weekdays)
        pulumi.set(__self__, "weeks", weeks)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Must be between `1` and `10`
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def weekdays(self) -> Sequence[str]:
        """
        The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")

    @property
    @pulumi.getter
    def weeks(self) -> Sequence[str]:
        """
        The weeks of the month to retain backups of. Must be one of `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        return pulumi.get(self, "weeks")


@pulumi.output_type
class PolicyFileShareRetentionWeekly(dict):
    def __init__(__self__, *,
                 count: int,
                 weekdays: Sequence[str]):
        """
        :param int count: The number of yearly backups to keep. Must be between `1` and `10`
        :param Sequence[str] weekdays: The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "weekdays", weekdays)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Must be between `1` and `10`
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def weekdays(self) -> Sequence[str]:
        """
        The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")


@pulumi.output_type
class PolicyFileShareRetentionYearly(dict):
    def __init__(__self__, *,
                 count: int,
                 months: Sequence[str],
                 weekdays: Sequence[str],
                 weeks: Sequence[str]):
        """
        :param int count: The number of yearly backups to keep. Must be between `1` and `10`
        :param Sequence[str] months: The months of the year to retain backups of. Must be one of `January`, `February`, `March`, `April`, `May`, `June`, `July`, `Augest`, `September`, `October`, `November` and `December`.
        :param Sequence[str] weekdays: The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        :param Sequence[str] weeks: The weeks of the month to retain backups of. Must be one of `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "months", months)
        pulumi.set(__self__, "weekdays", weekdays)
        pulumi.set(__self__, "weeks", weeks)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Must be between `1` and `10`
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def months(self) -> Sequence[str]:
        """
        The months of the year to retain backups of. Must be one of `January`, `February`, `March`, `April`, `May`, `June`, `July`, `Augest`, `September`, `October`, `November` and `December`.
        """
        return pulumi.get(self, "months")

    @property
    @pulumi.getter
    def weekdays(self) -> Sequence[str]:
        """
        The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")

    @property
    @pulumi.getter
    def weeks(self) -> Sequence[str]:
        """
        The weeks of the month to retain backups of. Must be one of `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        return pulumi.get(self, "weeks")


@pulumi.output_type
class PolicyVMBackup(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "hourDuration":
            suggest = "hour_duration"
        elif key == "hourInterval":
            suggest = "hour_interval"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyVMBackup. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyVMBackup.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyVMBackup.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 frequency: str,
                 time: str,
                 hour_duration: Optional[int] = None,
                 hour_interval: Optional[int] = None,
                 weekdays: Optional[Sequence[str]] = None):
        """
        :param str frequency: Sets the backup frequency. Possible values are `Hourly`, `Daily` and `Weekly`.
        :param str time: The time of day to perform the backup in 24hour format.
        :param int hour_duration: Duration of the backup window in hours. Possible values are between `4` and `24` This is used when `frequency` is `Hourly`.
        :param int hour_interval: Interval in hour at which backup is triggered. Possible values are `4`, `6`, `8` and `12`. This is used  when `frequency` is `Hourly`.
        :param Sequence[str] weekdays: The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        pulumi.set(__self__, "frequency", frequency)
        pulumi.set(__self__, "time", time)
        if hour_duration is not None:
            pulumi.set(__self__, "hour_duration", hour_duration)
        if hour_interval is not None:
            pulumi.set(__self__, "hour_interval", hour_interval)
        if weekdays is not None:
            pulumi.set(__self__, "weekdays", weekdays)

    @property
    @pulumi.getter
    def frequency(self) -> str:
        """
        Sets the backup frequency. Possible values are `Hourly`, `Daily` and `Weekly`.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def time(self) -> str:
        """
        The time of day to perform the backup in 24hour format.
        """
        return pulumi.get(self, "time")

    @property
    @pulumi.getter(name="hourDuration")
    def hour_duration(self) -> Optional[int]:
        """
        Duration of the backup window in hours. Possible values are between `4` and `24` This is used when `frequency` is `Hourly`.
        """
        return pulumi.get(self, "hour_duration")

    @property
    @pulumi.getter(name="hourInterval")
    def hour_interval(self) -> Optional[int]:
        """
        Interval in hour at which backup is triggered. Possible values are `4`, `6`, `8` and `12`. This is used  when `frequency` is `Hourly`.
        """
        return pulumi.get(self, "hour_interval")

    @property
    @pulumi.getter
    def weekdays(self) -> Optional[Sequence[str]]:
        """
        The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")


@pulumi.output_type
class PolicyVMRetentionDaily(dict):
    def __init__(__self__, *,
                 count: int):
        """
        :param int count: The number of yearly backups to keep. Must be between `1` and `9999`
        """
        pulumi.set(__self__, "count", count)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Must be between `1` and `9999`
        """
        return pulumi.get(self, "count")


@pulumi.output_type
class PolicyVMRetentionMonthly(dict):
    def __init__(__self__, *,
                 count: int,
                 weekdays: Sequence[str],
                 weeks: Sequence[str]):
        """
        :param int count: The number of yearly backups to keep. Must be between `1` and `9999`
        :param Sequence[str] weekdays: The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        :param Sequence[str] weeks: The weeks of the month to retain backups of. Must be one of `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "weekdays", weekdays)
        pulumi.set(__self__, "weeks", weeks)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Must be between `1` and `9999`
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def weekdays(self) -> Sequence[str]:
        """
        The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")

    @property
    @pulumi.getter
    def weeks(self) -> Sequence[str]:
        """
        The weeks of the month to retain backups of. Must be one of `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        return pulumi.get(self, "weeks")


@pulumi.output_type
class PolicyVMRetentionWeekly(dict):
    def __init__(__self__, *,
                 count: int,
                 weekdays: Sequence[str]):
        """
        :param int count: The number of yearly backups to keep. Must be between `1` and `9999`
        :param Sequence[str] weekdays: The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "weekdays", weekdays)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Must be between `1` and `9999`
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def weekdays(self) -> Sequence[str]:
        """
        The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")


@pulumi.output_type
class PolicyVMRetentionYearly(dict):
    def __init__(__self__, *,
                 count: int,
                 months: Sequence[str],
                 weekdays: Sequence[str],
                 weeks: Sequence[str]):
        """
        :param int count: The number of yearly backups to keep. Must be between `1` and `9999`
        :param Sequence[str] months: The months of the year to retain backups of. Must be one of `January`, `February`, `March`, `April`, `May`, `June`, `July`, `August`, `September`, `October`, `November` and `December`.
        :param Sequence[str] weekdays: The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        :param Sequence[str] weeks: The weeks of the month to retain backups of. Must be one of `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "months", months)
        pulumi.set(__self__, "weekdays", weekdays)
        pulumi.set(__self__, "weeks", weeks)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Must be between `1` and `9999`
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def months(self) -> Sequence[str]:
        """
        The months of the year to retain backups of. Must be one of `January`, `February`, `March`, `April`, `May`, `June`, `July`, `August`, `September`, `October`, `November` and `December`.
        """
        return pulumi.get(self, "months")

    @property
    @pulumi.getter
    def weekdays(self) -> Sequence[str]:
        """
        The weekday backups to retain . Must be one of `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")

    @property
    @pulumi.getter
    def weeks(self) -> Sequence[str]:
        """
        The weeks of the month to retain backups of. Must be one of `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        return pulumi.get(self, "weeks")


@pulumi.output_type
class PolicyVMWorkloadProtectionPolicy(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "policyType":
            suggest = "policy_type"
        elif key == "retentionDaily":
            suggest = "retention_daily"
        elif key == "retentionMonthly":
            suggest = "retention_monthly"
        elif key == "retentionWeekly":
            suggest = "retention_weekly"
        elif key == "retentionYearly":
            suggest = "retention_yearly"
        elif key == "simpleRetention":
            suggest = "simple_retention"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyVMWorkloadProtectionPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyVMWorkloadProtectionPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyVMWorkloadProtectionPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 backup: 'outputs.PolicyVMWorkloadProtectionPolicyBackup',
                 policy_type: str,
                 retention_daily: Optional['outputs.PolicyVMWorkloadProtectionPolicyRetentionDaily'] = None,
                 retention_monthly: Optional['outputs.PolicyVMWorkloadProtectionPolicyRetentionMonthly'] = None,
                 retention_weekly: Optional['outputs.PolicyVMWorkloadProtectionPolicyRetentionWeekly'] = None,
                 retention_yearly: Optional['outputs.PolicyVMWorkloadProtectionPolicyRetentionYearly'] = None,
                 simple_retention: Optional['outputs.PolicyVMWorkloadProtectionPolicySimpleRetention'] = None):
        """
        :param 'PolicyVMWorkloadProtectionPolicyBackupArgs' backup: A `backup` block as defined below.
        :param str policy_type: The type of the VM Workload Backup Policy. Possible values are `Differential`, `Full`, `Incremental` and `Log`.
        :param 'PolicyVMWorkloadProtectionPolicyRetentionDailyArgs' retention_daily: A `retention_daily` block as defined below.
        :param 'PolicyVMWorkloadProtectionPolicyRetentionMonthlyArgs' retention_monthly: A `retention_monthly` block as defined below.
        :param 'PolicyVMWorkloadProtectionPolicyRetentionWeeklyArgs' retention_weekly: A `retention_weekly` block as defined below.
        :param 'PolicyVMWorkloadProtectionPolicyRetentionYearlyArgs' retention_yearly: A `retention_yearly` block as defined below.
        :param 'PolicyVMWorkloadProtectionPolicySimpleRetentionArgs' simple_retention: A `simple_retention` block as defined below.
        """
        pulumi.set(__self__, "backup", backup)
        pulumi.set(__self__, "policy_type", policy_type)
        if retention_daily is not None:
            pulumi.set(__self__, "retention_daily", retention_daily)
        if retention_monthly is not None:
            pulumi.set(__self__, "retention_monthly", retention_monthly)
        if retention_weekly is not None:
            pulumi.set(__self__, "retention_weekly", retention_weekly)
        if retention_yearly is not None:
            pulumi.set(__self__, "retention_yearly", retention_yearly)
        if simple_retention is not None:
            pulumi.set(__self__, "simple_retention", simple_retention)

    @property
    @pulumi.getter
    def backup(self) -> 'outputs.PolicyVMWorkloadProtectionPolicyBackup':
        """
        A `backup` block as defined below.
        """
        return pulumi.get(self, "backup")

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> str:
        """
        The type of the VM Workload Backup Policy. Possible values are `Differential`, `Full`, `Incremental` and `Log`.
        """
        return pulumi.get(self, "policy_type")

    @property
    @pulumi.getter(name="retentionDaily")
    def retention_daily(self) -> Optional['outputs.PolicyVMWorkloadProtectionPolicyRetentionDaily']:
        """
        A `retention_daily` block as defined below.
        """
        return pulumi.get(self, "retention_daily")

    @property
    @pulumi.getter(name="retentionMonthly")
    def retention_monthly(self) -> Optional['outputs.PolicyVMWorkloadProtectionPolicyRetentionMonthly']:
        """
        A `retention_monthly` block as defined below.
        """
        return pulumi.get(self, "retention_monthly")

    @property
    @pulumi.getter(name="retentionWeekly")
    def retention_weekly(self) -> Optional['outputs.PolicyVMWorkloadProtectionPolicyRetentionWeekly']:
        """
        A `retention_weekly` block as defined below.
        """
        return pulumi.get(self, "retention_weekly")

    @property
    @pulumi.getter(name="retentionYearly")
    def retention_yearly(self) -> Optional['outputs.PolicyVMWorkloadProtectionPolicyRetentionYearly']:
        """
        A `retention_yearly` block as defined below.
        """
        return pulumi.get(self, "retention_yearly")

    @property
    @pulumi.getter(name="simpleRetention")
    def simple_retention(self) -> Optional['outputs.PolicyVMWorkloadProtectionPolicySimpleRetention']:
        """
        A `simple_retention` block as defined below.
        """
        return pulumi.get(self, "simple_retention")


@pulumi.output_type
class PolicyVMWorkloadProtectionPolicyBackup(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "frequencyInMinutes":
            suggest = "frequency_in_minutes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyVMWorkloadProtectionPolicyBackup. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyVMWorkloadProtectionPolicyBackup.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyVMWorkloadProtectionPolicyBackup.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 frequency: Optional[str] = None,
                 frequency_in_minutes: Optional[int] = None,
                 time: Optional[str] = None,
                 weekdays: Optional[Sequence[str]] = None):
        """
        :param str frequency: The backup frequency for the VM Workload Backup Policy. Possible values are `Daily` and `Weekly`.
        :param int frequency_in_minutes: The backup frequency in minutes for the VM Workload Backup Policy. Possible values are `15`, `30`, `60`, `120`, `240`, `480`, `720` and `1440`.
        :param str time: The time of day to perform the backup in 24hour format.
        :param Sequence[str] weekdays: The days of the week to perform backups on. Possible values are `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`. This is used when `frequency` is `Weekly`.
        """
        if frequency is not None:
            pulumi.set(__self__, "frequency", frequency)
        if frequency_in_minutes is not None:
            pulumi.set(__self__, "frequency_in_minutes", frequency_in_minutes)
        if time is not None:
            pulumi.set(__self__, "time", time)
        if weekdays is not None:
            pulumi.set(__self__, "weekdays", weekdays)

    @property
    @pulumi.getter
    def frequency(self) -> Optional[str]:
        """
        The backup frequency for the VM Workload Backup Policy. Possible values are `Daily` and `Weekly`.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter(name="frequencyInMinutes")
    def frequency_in_minutes(self) -> Optional[int]:
        """
        The backup frequency in minutes for the VM Workload Backup Policy. Possible values are `15`, `30`, `60`, `120`, `240`, `480`, `720` and `1440`.
        """
        return pulumi.get(self, "frequency_in_minutes")

    @property
    @pulumi.getter
    def time(self) -> Optional[str]:
        """
        The time of day to perform the backup in 24hour format.
        """
        return pulumi.get(self, "time")

    @property
    @pulumi.getter
    def weekdays(self) -> Optional[Sequence[str]]:
        """
        The days of the week to perform backups on. Possible values are `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`. This is used when `frequency` is `Weekly`.
        """
        return pulumi.get(self, "weekdays")


@pulumi.output_type
class PolicyVMWorkloadProtectionPolicyRetentionDaily(dict):
    def __init__(__self__, *,
                 count: int):
        """
        :param int count: The number of daily backups to keep. Possible values are between `7` and `9999`.
        """
        pulumi.set(__self__, "count", count)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of daily backups to keep. Possible values are between `7` and `9999`.
        """
        return pulumi.get(self, "count")


@pulumi.output_type
class PolicyVMWorkloadProtectionPolicyRetentionMonthly(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "formatType":
            suggest = "format_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyVMWorkloadProtectionPolicyRetentionMonthly. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyVMWorkloadProtectionPolicyRetentionMonthly.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyVMWorkloadProtectionPolicyRetentionMonthly.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 count: int,
                 format_type: str,
                 monthdays: Optional[Sequence[int]] = None,
                 weekdays: Optional[Sequence[str]] = None,
                 weeks: Optional[Sequence[str]] = None):
        """
        :param int count: The number of monthly backups to keep. Must be between `1` and `1188`.
        :param str format_type: The retention schedule format type for monthly retention policy. Possible values are `Daily` and `Weekly`.
        :param Sequence[int] monthdays: The monthday backups to retain. Possible values are between `0` and `28`.
        :param Sequence[str] weekdays: The weekday backups to retain. Possible values are `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        :param Sequence[str] weeks: The weeks of the month to retain backups of. Possible values are `First`, `Second`, `Third`, `Fourth` and `Last`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "format_type", format_type)
        if monthdays is not None:
            pulumi.set(__self__, "monthdays", monthdays)
        if weekdays is not None:
            pulumi.set(__self__, "weekdays", weekdays)
        if weeks is not None:
            pulumi.set(__self__, "weeks", weeks)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of monthly backups to keep. Must be between `1` and `1188`.
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter(name="formatType")
    def format_type(self) -> str:
        """
        The retention schedule format type for monthly retention policy. Possible values are `Daily` and `Weekly`.
        """
        return pulumi.get(self, "format_type")

    @property
    @pulumi.getter
    def monthdays(self) -> Optional[Sequence[int]]:
        """
        The monthday backups to retain. Possible values are between `0` and `28`.
        """
        return pulumi.get(self, "monthdays")

    @property
    @pulumi.getter
    def weekdays(self) -> Optional[Sequence[str]]:
        """
        The weekday backups to retain. Possible values are `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")

    @property
    @pulumi.getter
    def weeks(self) -> Optional[Sequence[str]]:
        """
        The weeks of the month to retain backups of. Possible values are `First`, `Second`, `Third`, `Fourth` and `Last`.
        """
        return pulumi.get(self, "weeks")


@pulumi.output_type
class PolicyVMWorkloadProtectionPolicyRetentionWeekly(dict):
    def __init__(__self__, *,
                 count: int,
                 weekdays: Sequence[str]):
        """
        :param int count: The number of weekly backups to keep. Possible values are between `1` and `5163`.
        :param Sequence[str] weekdays: The weekday backups to retain. Possible values are `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "weekdays", weekdays)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of weekly backups to keep. Possible values are between `1` and `5163`.
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def weekdays(self) -> Sequence[str]:
        """
        The weekday backups to retain. Possible values are `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")


@pulumi.output_type
class PolicyVMWorkloadProtectionPolicyRetentionYearly(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "formatType":
            suggest = "format_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyVMWorkloadProtectionPolicyRetentionYearly. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyVMWorkloadProtectionPolicyRetentionYearly.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyVMWorkloadProtectionPolicyRetentionYearly.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 count: int,
                 format_type: str,
                 months: Sequence[str],
                 monthdays: Optional[Sequence[int]] = None,
                 weekdays: Optional[Sequence[str]] = None,
                 weeks: Optional[Sequence[str]] = None):
        """
        :param int count: The number of yearly backups to keep. Possible values are between `1` and `99`
        :param str format_type: The retention schedule format type for yearly retention policy. Possible values are `Daily` and `Weekly`.
        :param Sequence[str] months: The months of the year to retain backups of. Possible values are `January`, `February`, `March`, `April`, `May`, `June`, `July`, `August`, `September`, `October`, `November` and `December`.
        :param Sequence[int] monthdays: The monthday backups to retain. Possible values are between `0` and `28`.
        :param Sequence[str] weekdays: The weekday backups to retain. Possible values are `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        :param Sequence[str] weeks: The weeks of the month to retain backups of. Possible values are `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "format_type", format_type)
        pulumi.set(__self__, "months", months)
        if monthdays is not None:
            pulumi.set(__self__, "monthdays", monthdays)
        if weekdays is not None:
            pulumi.set(__self__, "weekdays", weekdays)
        if weeks is not None:
            pulumi.set(__self__, "weeks", weeks)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The number of yearly backups to keep. Possible values are between `1` and `99`
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter(name="formatType")
    def format_type(self) -> str:
        """
        The retention schedule format type for yearly retention policy. Possible values are `Daily` and `Weekly`.
        """
        return pulumi.get(self, "format_type")

    @property
    @pulumi.getter
    def months(self) -> Sequence[str]:
        """
        The months of the year to retain backups of. Possible values are `January`, `February`, `March`, `April`, `May`, `June`, `July`, `August`, `September`, `October`, `November` and `December`.
        """
        return pulumi.get(self, "months")

    @property
    @pulumi.getter
    def monthdays(self) -> Optional[Sequence[int]]:
        """
        The monthday backups to retain. Possible values are between `0` and `28`.
        """
        return pulumi.get(self, "monthdays")

    @property
    @pulumi.getter
    def weekdays(self) -> Optional[Sequence[str]]:
        """
        The weekday backups to retain. Possible values are `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` or `Saturday`.
        """
        return pulumi.get(self, "weekdays")

    @property
    @pulumi.getter
    def weeks(self) -> Optional[Sequence[str]]:
        """
        The weeks of the month to retain backups of. Possible values are `First`, `Second`, `Third`, `Fourth`, `Last`.
        """
        return pulumi.get(self, "weeks")


@pulumi.output_type
class PolicyVMWorkloadProtectionPolicySimpleRetention(dict):
    def __init__(__self__, *,
                 count: int):
        """
        :param int count: The count that is used to count retention duration with duration type `Days`. Possible values are between `7` and `35`.
        """
        pulumi.set(__self__, "count", count)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The count that is used to count retention duration with duration type `Days`. Possible values are between `7` and `35`.
        """
        return pulumi.get(self, "count")


@pulumi.output_type
class PolicyVMWorkloadSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "timeZone":
            suggest = "time_zone"
        elif key == "compressionEnabled":
            suggest = "compression_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyVMWorkloadSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyVMWorkloadSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyVMWorkloadSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 time_zone: str,
                 compression_enabled: Optional[bool] = None):
        """
        :param str time_zone: The timezone for the VM Workload Backup Policy. [The possible values are defined here](https://jackstromberg.com/2017/01/list-of-time-zones-consumed-by-azure/).
        :param bool compression_enabled: The compression setting for the VM Workload Backup Policy. Defaults to `false`.
        """
        pulumi.set(__self__, "time_zone", time_zone)
        if compression_enabled is not None:
            pulumi.set(__self__, "compression_enabled", compression_enabled)

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> str:
        """
        The timezone for the VM Workload Backup Policy. [The possible values are defined here](https://jackstromberg.com/2017/01/list-of-time-zones-consumed-by-azure/).
        """
        return pulumi.get(self, "time_zone")

    @property
    @pulumi.getter(name="compressionEnabled")
    def compression_enabled(self) -> Optional[bool]:
        """
        The compression setting for the VM Workload Backup Policy. Defaults to `false`.
        """
        return pulumi.get(self, "compression_enabled")


