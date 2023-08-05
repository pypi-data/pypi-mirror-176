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
    'GetFlexibleServerResult',
    'AwaitableGetFlexibleServerResult',
    'get_flexible_server',
    'get_flexible_server_output',
]

@pulumi.output_type
class GetFlexibleServerResult:
    """
    A collection of values returned by getFlexibleServer.
    """
    def __init__(__self__, administrator_login=None, backup_retention_days=None, delegated_subnet_id=None, fqdn=None, geo_redundant_backup_enabled=None, high_availabilities=None, id=None, location=None, maintenance_windows=None, name=None, private_dns_zone_id=None, public_network_access_enabled=None, replica_capacity=None, replication_role=None, resource_group_name=None, restore_point_in_time=None, sku_name=None, storages=None, tags=None, version=None, zone=None):
        if administrator_login and not isinstance(administrator_login, str):
            raise TypeError("Expected argument 'administrator_login' to be a str")
        pulumi.set(__self__, "administrator_login", administrator_login)
        if backup_retention_days and not isinstance(backup_retention_days, int):
            raise TypeError("Expected argument 'backup_retention_days' to be a int")
        pulumi.set(__self__, "backup_retention_days", backup_retention_days)
        if delegated_subnet_id and not isinstance(delegated_subnet_id, str):
            raise TypeError("Expected argument 'delegated_subnet_id' to be a str")
        pulumi.set(__self__, "delegated_subnet_id", delegated_subnet_id)
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if geo_redundant_backup_enabled and not isinstance(geo_redundant_backup_enabled, bool):
            raise TypeError("Expected argument 'geo_redundant_backup_enabled' to be a bool")
        pulumi.set(__self__, "geo_redundant_backup_enabled", geo_redundant_backup_enabled)
        if high_availabilities and not isinstance(high_availabilities, list):
            raise TypeError("Expected argument 'high_availabilities' to be a list")
        pulumi.set(__self__, "high_availabilities", high_availabilities)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if maintenance_windows and not isinstance(maintenance_windows, list):
            raise TypeError("Expected argument 'maintenance_windows' to be a list")
        pulumi.set(__self__, "maintenance_windows", maintenance_windows)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if private_dns_zone_id and not isinstance(private_dns_zone_id, str):
            raise TypeError("Expected argument 'private_dns_zone_id' to be a str")
        pulumi.set(__self__, "private_dns_zone_id", private_dns_zone_id)
        if public_network_access_enabled and not isinstance(public_network_access_enabled, bool):
            raise TypeError("Expected argument 'public_network_access_enabled' to be a bool")
        pulumi.set(__self__, "public_network_access_enabled", public_network_access_enabled)
        if replica_capacity and not isinstance(replica_capacity, int):
            raise TypeError("Expected argument 'replica_capacity' to be a int")
        pulumi.set(__self__, "replica_capacity", replica_capacity)
        if replication_role and not isinstance(replication_role, str):
            raise TypeError("Expected argument 'replication_role' to be a str")
        pulumi.set(__self__, "replication_role", replication_role)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if restore_point_in_time and not isinstance(restore_point_in_time, str):
            raise TypeError("Expected argument 'restore_point_in_time' to be a str")
        pulumi.set(__self__, "restore_point_in_time", restore_point_in_time)
        if sku_name and not isinstance(sku_name, str):
            raise TypeError("Expected argument 'sku_name' to be a str")
        pulumi.set(__self__, "sku_name", sku_name)
        if storages and not isinstance(storages, list):
            raise TypeError("Expected argument 'storages' to be a list")
        pulumi.set(__self__, "storages", storages)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)
        if zone and not isinstance(zone, str):
            raise TypeError("Expected argument 'zone' to be a str")
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="administratorLogin")
    def administrator_login(self) -> str:
        """
        The Administrator login of the MySQL Flexible Server.
        """
        return pulumi.get(self, "administrator_login")

    @property
    @pulumi.getter(name="backupRetentionDays")
    def backup_retention_days(self) -> int:
        """
        The backup retention days of the MySQL Flexible Server.
        """
        return pulumi.get(self, "backup_retention_days")

    @property
    @pulumi.getter(name="delegatedSubnetId")
    def delegated_subnet_id(self) -> str:
        """
        The ID of the virtual network subnet the MySQL Flexible Server is created in.
        """
        return pulumi.get(self, "delegated_subnet_id")

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        The fully qualified domain name of the MySQL Flexible Server.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="geoRedundantBackupEnabled")
    def geo_redundant_backup_enabled(self) -> bool:
        """
        Is geo redundant backup enabled?
        """
        return pulumi.get(self, "geo_redundant_backup_enabled")

    @property
    @pulumi.getter(name="highAvailabilities")
    def high_availabilities(self) -> Sequence['outputs.GetFlexibleServerHighAvailabilityResult']:
        """
        A `high_availability` block for this MySQL Flexible Server as defined below.
        """
        return pulumi.get(self, "high_availabilities")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure Region of the MySQL Flexible Server.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceWindows")
    def maintenance_windows(self) -> Sequence['outputs.GetFlexibleServerMaintenanceWindowResult']:
        """
        A `maintenance_window` block for this MySQL Flexible Server as defined below.
        """
        return pulumi.get(self, "maintenance_windows")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateDnsZoneId")
    def private_dns_zone_id(self) -> str:
        """
        The ID of the Private DNS zone of the MySQL Flexible Server.
        """
        return pulumi.get(self, "private_dns_zone_id")

    @property
    @pulumi.getter(name="publicNetworkAccessEnabled")
    def public_network_access_enabled(self) -> bool:
        """
        Is the public network access enabled?
        """
        return pulumi.get(self, "public_network_access_enabled")

    @property
    @pulumi.getter(name="replicaCapacity")
    def replica_capacity(self) -> int:
        """
        The maximum number of replicas that a primary MySQL Flexible Server can have.
        """
        return pulumi.get(self, "replica_capacity")

    @property
    @pulumi.getter(name="replicationRole")
    def replication_role(self) -> str:
        """
        The replication role of the MySQL Flexible Server.
        """
        return pulumi.get(self, "replication_role")

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
        The SKU Name of the MySQL Flexible Server.
        """
        return pulumi.get(self, "sku_name")

    @property
    @pulumi.getter
    def storages(self) -> Sequence['outputs.GetFlexibleServerStorageResult']:
        """
        A `storage` block for this MySQL Flexible Server as defined below.
        """
        return pulumi.get(self, "storages")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags which are assigned to the MySQL Flexible Server.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The version of the MySQL Flexible Server.
        """
        return pulumi.get(self, "version")

    @property
    @pulumi.getter
    def zone(self) -> str:
        """
        The Availability Zones where this MySQL Flexible Server is located.
        """
        return pulumi.get(self, "zone")


class AwaitableGetFlexibleServerResult(GetFlexibleServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFlexibleServerResult(
            administrator_login=self.administrator_login,
            backup_retention_days=self.backup_retention_days,
            delegated_subnet_id=self.delegated_subnet_id,
            fqdn=self.fqdn,
            geo_redundant_backup_enabled=self.geo_redundant_backup_enabled,
            high_availabilities=self.high_availabilities,
            id=self.id,
            location=self.location,
            maintenance_windows=self.maintenance_windows,
            name=self.name,
            private_dns_zone_id=self.private_dns_zone_id,
            public_network_access_enabled=self.public_network_access_enabled,
            replica_capacity=self.replica_capacity,
            replication_role=self.replication_role,
            resource_group_name=self.resource_group_name,
            restore_point_in_time=self.restore_point_in_time,
            sku_name=self.sku_name,
            storages=self.storages,
            tags=self.tags,
            version=self.version,
            zone=self.zone)


def get_flexible_server(name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFlexibleServerResult:
    """
    Use this data source to access information about an existing MySQL Flexible Server.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.mysql.get_flexible_server(name="existingMySqlFlexibleServer",
        resource_group_name="existingResGroup")
    pulumi.export("id", example.id)
    ```


    :param str name: Specifies the name of the MySQL Flexible Server.
    :param str resource_group_name: The name of the resource group for the MySQL Flexible Server.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:mysql/getFlexibleServer:getFlexibleServer', __args__, opts=opts, typ=GetFlexibleServerResult).value

    return AwaitableGetFlexibleServerResult(
        administrator_login=__ret__.administrator_login,
        backup_retention_days=__ret__.backup_retention_days,
        delegated_subnet_id=__ret__.delegated_subnet_id,
        fqdn=__ret__.fqdn,
        geo_redundant_backup_enabled=__ret__.geo_redundant_backup_enabled,
        high_availabilities=__ret__.high_availabilities,
        id=__ret__.id,
        location=__ret__.location,
        maintenance_windows=__ret__.maintenance_windows,
        name=__ret__.name,
        private_dns_zone_id=__ret__.private_dns_zone_id,
        public_network_access_enabled=__ret__.public_network_access_enabled,
        replica_capacity=__ret__.replica_capacity,
        replication_role=__ret__.replication_role,
        resource_group_name=__ret__.resource_group_name,
        restore_point_in_time=__ret__.restore_point_in_time,
        sku_name=__ret__.sku_name,
        storages=__ret__.storages,
        tags=__ret__.tags,
        version=__ret__.version,
        zone=__ret__.zone)


@_utilities.lift_output_func(get_flexible_server)
def get_flexible_server_output(name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFlexibleServerResult]:
    """
    Use this data source to access information about an existing MySQL Flexible Server.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.mysql.get_flexible_server(name="existingMySqlFlexibleServer",
        resource_group_name="existingResGroup")
    pulumi.export("id", example.id)
    ```


    :param str name: Specifies the name of the MySQL Flexible Server.
    :param str resource_group_name: The name of the resource group for the MySQL Flexible Server.
    """
    ...
