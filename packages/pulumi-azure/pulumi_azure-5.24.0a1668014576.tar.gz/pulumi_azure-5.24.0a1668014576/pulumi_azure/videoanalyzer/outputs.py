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
    'AnalyzerIdentity',
    'AnalyzerStorageAccount',
]

@pulumi.output_type
class AnalyzerIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "identityIds":
            suggest = "identity_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnalyzerIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnalyzerIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnalyzerIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 identity_ids: Sequence[str],
                 type: str):
        """
        :param Sequence[str] identity_ids: Specifies a list of User Assigned Managed Identity IDs to be assigned to this Video Analyzer instance.
        :param str type: Specifies the type of Managed Service Identity that should be configured on this Video Analyzer instance. Only possible value is `UserAssigned`.
        """
        pulumi.set(__self__, "identity_ids", identity_ids)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Sequence[str]:
        """
        Specifies a list of User Assigned Managed Identity IDs to be assigned to this Video Analyzer instance.
        """
        return pulumi.get(self, "identity_ids")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of Managed Service Identity that should be configured on this Video Analyzer instance. Only possible value is `UserAssigned`.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class AnalyzerStorageAccount(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "userAssignedIdentityId":
            suggest = "user_assigned_identity_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnalyzerStorageAccount. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnalyzerStorageAccount.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnalyzerStorageAccount.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 user_assigned_identity_id: str):
        """
        :param str id: Specifies the ID of the Storage Account that will be associated with the Video Analyzer instance.
        :param str user_assigned_identity_id: Specifies the User Assigned Identity ID which should be assigned to access this Storage Account.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "user_assigned_identity_id", user_assigned_identity_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Specifies the ID of the Storage Account that will be associated with the Video Analyzer instance.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> str:
        """
        Specifies the User Assigned Identity ID which should be assigned to access this Storage Account.
        """
        return pulumi.get(self, "user_assigned_identity_id")


