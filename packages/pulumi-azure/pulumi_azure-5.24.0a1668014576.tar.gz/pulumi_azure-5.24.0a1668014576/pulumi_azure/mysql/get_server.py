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
    'GetServerResult',
    'AwaitableGetServerResult',
    'get_server',
    'get_server_output',
]

@pulumi.output_type
class GetServerResult:
    """
    A collection of values returned by getServer.
    """
    def __init__(__self__, administrator_login=None, auto_grow_enabled=None, backup_retention_days=None, fqdn=None, geo_redundant_backup_enabled=None, id=None, identities=None, infrastructure_encryption_enabled=None, location=None, name=None, public_network_access_enabled=None, resource_group_name=None, restore_point_in_time=None, sku_name=None, ssl_enforcement_enabled=None, ssl_minimal_tls_version_enforced=None, storage_mb=None, tags=None, threat_detection_policies=None, version=None):
        if administrator_login and not isinstance(administrator_login, str):
            raise TypeError("Expected argument 'administrator_login' to be a str")
        pulumi.set(__self__, "administrator_login", administrator_login)
        if auto_grow_enabled and not isinstance(auto_grow_enabled, bool):
            raise TypeError("Expected argument 'auto_grow_enabled' to be a bool")
        pulumi.set(__self__, "auto_grow_enabled", auto_grow_enabled)
        if backup_retention_days and not isinstance(backup_retention_days, int):
            raise TypeError("Expected argument 'backup_retention_days' to be a int")
        pulumi.set(__self__, "backup_retention_days", backup_retention_days)
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if geo_redundant_backup_enabled and not isinstance(geo_redundant_backup_enabled, bool):
            raise TypeError("Expected argument 'geo_redundant_backup_enabled' to be a bool")
        pulumi.set(__self__, "geo_redundant_backup_enabled", geo_redundant_backup_enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        pulumi.set(__self__, "identities", identities)
        if infrastructure_encryption_enabled and not isinstance(infrastructure_encryption_enabled, bool):
            raise TypeError("Expected argument 'infrastructure_encryption_enabled' to be a bool")
        pulumi.set(__self__, "infrastructure_encryption_enabled", infrastructure_encryption_enabled)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if public_network_access_enabled and not isinstance(public_network_access_enabled, bool):
            raise TypeError("Expected argument 'public_network_access_enabled' to be a bool")
        pulumi.set(__self__, "public_network_access_enabled", public_network_access_enabled)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if restore_point_in_time and not isinstance(restore_point_in_time, str):
            raise TypeError("Expected argument 'restore_point_in_time' to be a str")
        pulumi.set(__self__, "restore_point_in_time", restore_point_in_time)
        if sku_name and not isinstance(sku_name, str):
            raise TypeError("Expected argument 'sku_name' to be a str")
        pulumi.set(__self__, "sku_name", sku_name)
        if ssl_enforcement_enabled and not isinstance(ssl_enforcement_enabled, bool):
            raise TypeError("Expected argument 'ssl_enforcement_enabled' to be a bool")
        pulumi.set(__self__, "ssl_enforcement_enabled", ssl_enforcement_enabled)
        if ssl_minimal_tls_version_enforced and not isinstance(ssl_minimal_tls_version_enforced, str):
            raise TypeError("Expected argument 'ssl_minimal_tls_version_enforced' to be a str")
        pulumi.set(__self__, "ssl_minimal_tls_version_enforced", ssl_minimal_tls_version_enforced)
        if storage_mb and not isinstance(storage_mb, int):
            raise TypeError("Expected argument 'storage_mb' to be a int")
        pulumi.set(__self__, "storage_mb", storage_mb)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if threat_detection_policies and not isinstance(threat_detection_policies, list):
            raise TypeError("Expected argument 'threat_detection_policies' to be a list")
        pulumi.set(__self__, "threat_detection_policies", threat_detection_policies)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="administratorLogin")
    def administrator_login(self) -> str:
        """
        The Administrator login for the MySQL Server.
        """
        return pulumi.get(self, "administrator_login")

    @property
    @pulumi.getter(name="autoGrowEnabled")
    def auto_grow_enabled(self) -> bool:
        """
        The auto grow setting for this MySQL Server.
        """
        return pulumi.get(self, "auto_grow_enabled")

    @property
    @pulumi.getter(name="backupRetentionDays")
    def backup_retention_days(self) -> int:
        """
        The backup retention days for this MySQL server.
        """
        return pulumi.get(self, "backup_retention_days")

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        The FQDN of the MySQL Server.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="geoRedundantBackupEnabled")
    def geo_redundant_backup_enabled(self) -> bool:
        """
        The geo redundant backup setting for this MySQL Server.
        """
        return pulumi.get(self, "geo_redundant_backup_enabled")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetServerIdentityResult']:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter(name="infrastructureEncryptionEnabled")
    def infrastructure_encryption_enabled(self) -> bool:
        """
        Whether or not infrastructure is encrypted for this MySQL Server.
        """
        return pulumi.get(self, "infrastructure_encryption_enabled")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure location where the resource exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicNetworkAccessEnabled")
    def public_network_access_enabled(self) -> bool:
        """
        Whether or not public network access is allowed for this MySQL Server.
        """
        return pulumi.get(self, "public_network_access_enabled")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="restorePointInTime")
    def restore_point_in_time(self) -> str:
        return pulumi.get(self, "restore_point_in_time")

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> str:
        """
        The SKU Name for this MySQL Server.
        """
        return pulumi.get(self, "sku_name")

    @property
    @pulumi.getter(name="sslEnforcementEnabled")
    def ssl_enforcement_enabled(self) -> bool:
        """
        Specifies if SSL should be enforced on connections for this MySQL Server.
        """
        return pulumi.get(self, "ssl_enforcement_enabled")

    @property
    @pulumi.getter(name="sslMinimalTlsVersionEnforced")
    def ssl_minimal_tls_version_enforced(self) -> str:
        """
        The minimum TLS version to support for this MySQL Server.
        """
        return pulumi.get(self, "ssl_minimal_tls_version_enforced")

    @property
    @pulumi.getter(name="storageMb")
    def storage_mb(self) -> int:
        """
        Max storage allowed for this MySQL Server.
        """
        return pulumi.get(self, "storage_mb")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="threatDetectionPolicies")
    def threat_detection_policies(self) -> Sequence['outputs.GetServerThreatDetectionPolicyResult']:
        """
        Threat detection policy configuration, known in the API as Server Security Alerts Policy. The `threat_detection_policy` block exports fields documented below.
        """
        return pulumi.get(self, "threat_detection_policies")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The version of this MySQL Server.
        """
        return pulumi.get(self, "version")


class AwaitableGetServerResult(GetServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerResult(
            administrator_login=self.administrator_login,
            auto_grow_enabled=self.auto_grow_enabled,
            backup_retention_days=self.backup_retention_days,
            fqdn=self.fqdn,
            geo_redundant_backup_enabled=self.geo_redundant_backup_enabled,
            id=self.id,
            identities=self.identities,
            infrastructure_encryption_enabled=self.infrastructure_encryption_enabled,
            location=self.location,
            name=self.name,
            public_network_access_enabled=self.public_network_access_enabled,
            resource_group_name=self.resource_group_name,
            restore_point_in_time=self.restore_point_in_time,
            sku_name=self.sku_name,
            ssl_enforcement_enabled=self.ssl_enforcement_enabled,
            ssl_minimal_tls_version_enforced=self.ssl_minimal_tls_version_enforced,
            storage_mb=self.storage_mb,
            tags=self.tags,
            threat_detection_policies=self.threat_detection_policies,
            version=self.version)


def get_server(name: Optional[str] = None,
               resource_group_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerResult:
    """
    Use this data source to access information about an existing MySQL Server.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.mysql.get_server(name="existingMySqlServer",
        resource_group_name="existingResGroup")
    pulumi.export("id", example.id)
    ```


    :param str name: Specifies the name of the MySQL Server.
    :param str resource_group_name: The name of the resource group for the MySQL Server.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:mysql/getServer:getServer', __args__, opts=opts, typ=GetServerResult).value

    return AwaitableGetServerResult(
        administrator_login=__ret__.administrator_login,
        auto_grow_enabled=__ret__.auto_grow_enabled,
        backup_retention_days=__ret__.backup_retention_days,
        fqdn=__ret__.fqdn,
        geo_redundant_backup_enabled=__ret__.geo_redundant_backup_enabled,
        id=__ret__.id,
        identities=__ret__.identities,
        infrastructure_encryption_enabled=__ret__.infrastructure_encryption_enabled,
        location=__ret__.location,
        name=__ret__.name,
        public_network_access_enabled=__ret__.public_network_access_enabled,
        resource_group_name=__ret__.resource_group_name,
        restore_point_in_time=__ret__.restore_point_in_time,
        sku_name=__ret__.sku_name,
        ssl_enforcement_enabled=__ret__.ssl_enforcement_enabled,
        ssl_minimal_tls_version_enforced=__ret__.ssl_minimal_tls_version_enforced,
        storage_mb=__ret__.storage_mb,
        tags=__ret__.tags,
        threat_detection_policies=__ret__.threat_detection_policies,
        version=__ret__.version)


@_utilities.lift_output_func(get_server)
def get_server_output(name: Optional[pulumi.Input[str]] = None,
                      resource_group_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServerResult]:
    """
    Use this data source to access information about an existing MySQL Server.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.mysql.get_server(name="existingMySqlServer",
        resource_group_name="existingResGroup")
    pulumi.export("id", example.id)
    ```


    :param str name: Specifies the name of the MySQL Server.
    :param str resource_group_name: The name of the resource group for the MySQL Server.
    """
    ...
