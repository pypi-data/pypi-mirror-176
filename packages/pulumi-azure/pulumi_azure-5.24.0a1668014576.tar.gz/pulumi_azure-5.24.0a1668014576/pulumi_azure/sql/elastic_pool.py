# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ElasticPoolArgs', 'ElasticPool']

@pulumi.input_type
class ElasticPoolArgs:
    def __init__(__self__, *,
                 dtu: pulumi.Input[int],
                 edition: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 server_name: pulumi.Input[str],
                 db_dtu_max: Optional[pulumi.Input[int]] = None,
                 db_dtu_min: Optional[pulumi.Input[int]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pool_size: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ElasticPool resource.
        :param pulumi.Input[int] dtu: The total shared DTU for the elastic pool. Valid values depend on the `edition` which has been defined. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for valid combinations.
        :param pulumi.Input[str] edition: The edition of the elastic pool to be created. Valid values are `Basic`, `Standard`, and `Premium`. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for details. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the elastic pool. This must be the same as the resource group of the underlying SQL server.
        :param pulumi.Input[str] server_name: The name of the SQL Server on which to create the elastic pool. Changing this forces a new resource to be created.
        :param pulumi.Input[int] db_dtu_max: The maximum DTU which will be guaranteed to all databases in the elastic pool to be created.
        :param pulumi.Input[int] db_dtu_min: The minimum DTU which will be guaranteed to all databases in the elastic pool to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the elastic pool. This needs to be globally unique. Changing this forces a new resource to be created.
        :param pulumi.Input[int] pool_size: The maximum size in MB that all databases in the elastic pool can grow to. The maximum size must be consistent with combination of `edition` and `dtu` and the limits documented in [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). If not defined when creating an elastic pool, the value is set to the size implied by `edition` and `dtu`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "dtu", dtu)
        pulumi.set(__self__, "edition", edition)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "server_name", server_name)
        if db_dtu_max is not None:
            pulumi.set(__self__, "db_dtu_max", db_dtu_max)
        if db_dtu_min is not None:
            pulumi.set(__self__, "db_dtu_min", db_dtu_min)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if pool_size is not None:
            pulumi.set(__self__, "pool_size", pool_size)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def dtu(self) -> pulumi.Input[int]:
        """
        The total shared DTU for the elastic pool. Valid values depend on the `edition` which has been defined. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for valid combinations.
        """
        return pulumi.get(self, "dtu")

    @dtu.setter
    def dtu(self, value: pulumi.Input[int]):
        pulumi.set(self, "dtu", value)

    @property
    @pulumi.getter
    def edition(self) -> pulumi.Input[str]:
        """
        The edition of the elastic pool to be created. Valid values are `Basic`, `Standard`, and `Premium`. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for details. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "edition")

    @edition.setter
    def edition(self, value: pulumi.Input[str]):
        pulumi.set(self, "edition", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the elastic pool. This must be the same as the resource group of the underlying SQL server.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> pulumi.Input[str]:
        """
        The name of the SQL Server on which to create the elastic pool. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server_name")

    @server_name.setter
    def server_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_name", value)

    @property
    @pulumi.getter(name="dbDtuMax")
    def db_dtu_max(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum DTU which will be guaranteed to all databases in the elastic pool to be created.
        """
        return pulumi.get(self, "db_dtu_max")

    @db_dtu_max.setter
    def db_dtu_max(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "db_dtu_max", value)

    @property
    @pulumi.getter(name="dbDtuMin")
    def db_dtu_min(self) -> Optional[pulumi.Input[int]]:
        """
        The minimum DTU which will be guaranteed to all databases in the elastic pool to be created.
        """
        return pulumi.get(self, "db_dtu_min")

    @db_dtu_min.setter
    def db_dtu_min(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "db_dtu_min", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the elastic pool. This needs to be globally unique. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="poolSize")
    def pool_size(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum size in MB that all databases in the elastic pool can grow to. The maximum size must be consistent with combination of `edition` and `dtu` and the limits documented in [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). If not defined when creating an elastic pool, the value is set to the size implied by `edition` and `dtu`.
        """
        return pulumi.get(self, "pool_size")

    @pool_size.setter
    def pool_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "pool_size", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ElasticPoolState:
    def __init__(__self__, *,
                 creation_date: Optional[pulumi.Input[str]] = None,
                 db_dtu_max: Optional[pulumi.Input[int]] = None,
                 db_dtu_min: Optional[pulumi.Input[int]] = None,
                 dtu: Optional[pulumi.Input[int]] = None,
                 edition: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pool_size: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering ElasticPool resources.
        :param pulumi.Input[str] creation_date: The creation date of the SQL Elastic Pool.
        :param pulumi.Input[int] db_dtu_max: The maximum DTU which will be guaranteed to all databases in the elastic pool to be created.
        :param pulumi.Input[int] db_dtu_min: The minimum DTU which will be guaranteed to all databases in the elastic pool to be created.
        :param pulumi.Input[int] dtu: The total shared DTU for the elastic pool. Valid values depend on the `edition` which has been defined. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for valid combinations.
        :param pulumi.Input[str] edition: The edition of the elastic pool to be created. Valid values are `Basic`, `Standard`, and `Premium`. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for details. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the elastic pool. This needs to be globally unique. Changing this forces a new resource to be created.
        :param pulumi.Input[int] pool_size: The maximum size in MB that all databases in the elastic pool can grow to. The maximum size must be consistent with combination of `edition` and `dtu` and the limits documented in [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). If not defined when creating an elastic pool, the value is set to the size implied by `edition` and `dtu`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the elastic pool. This must be the same as the resource group of the underlying SQL server.
        :param pulumi.Input[str] server_name: The name of the SQL Server on which to create the elastic pool. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        if creation_date is not None:
            pulumi.set(__self__, "creation_date", creation_date)
        if db_dtu_max is not None:
            pulumi.set(__self__, "db_dtu_max", db_dtu_max)
        if db_dtu_min is not None:
            pulumi.set(__self__, "db_dtu_min", db_dtu_min)
        if dtu is not None:
            pulumi.set(__self__, "dtu", dtu)
        if edition is not None:
            pulumi.set(__self__, "edition", edition)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if pool_size is not None:
            pulumi.set(__self__, "pool_size", pool_size)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if server_name is not None:
            pulumi.set(__self__, "server_name", server_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> Optional[pulumi.Input[str]]:
        """
        The creation date of the SQL Elastic Pool.
        """
        return pulumi.get(self, "creation_date")

    @creation_date.setter
    def creation_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_date", value)

    @property
    @pulumi.getter(name="dbDtuMax")
    def db_dtu_max(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum DTU which will be guaranteed to all databases in the elastic pool to be created.
        """
        return pulumi.get(self, "db_dtu_max")

    @db_dtu_max.setter
    def db_dtu_max(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "db_dtu_max", value)

    @property
    @pulumi.getter(name="dbDtuMin")
    def db_dtu_min(self) -> Optional[pulumi.Input[int]]:
        """
        The minimum DTU which will be guaranteed to all databases in the elastic pool to be created.
        """
        return pulumi.get(self, "db_dtu_min")

    @db_dtu_min.setter
    def db_dtu_min(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "db_dtu_min", value)

    @property
    @pulumi.getter
    def dtu(self) -> Optional[pulumi.Input[int]]:
        """
        The total shared DTU for the elastic pool. Valid values depend on the `edition` which has been defined. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for valid combinations.
        """
        return pulumi.get(self, "dtu")

    @dtu.setter
    def dtu(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "dtu", value)

    @property
    @pulumi.getter
    def edition(self) -> Optional[pulumi.Input[str]]:
        """
        The edition of the elastic pool to be created. Valid values are `Basic`, `Standard`, and `Premium`. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for details. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "edition")

    @edition.setter
    def edition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "edition", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the elastic pool. This needs to be globally unique. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="poolSize")
    def pool_size(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum size in MB that all databases in the elastic pool can grow to. The maximum size must be consistent with combination of `edition` and `dtu` and the limits documented in [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). If not defined when creating an elastic pool, the value is set to the size implied by `edition` and `dtu`.
        """
        return pulumi.get(self, "pool_size")

    @pool_size.setter
    def pool_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "pool_size", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the elastic pool. This must be the same as the resource group of the underlying SQL server.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the SQL Server on which to create the elastic pool. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server_name")

    @server_name.setter
    def server_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class ElasticPool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_dtu_max: Optional[pulumi.Input[int]] = None,
                 db_dtu_min: Optional[pulumi.Input[int]] = None,
                 dtu: Optional[pulumi.Input[int]] = None,
                 edition: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pool_size: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_sql_server = azure.sql.SqlServer("exampleSqlServer",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            version="12.0",
            administrator_login="4dm1n157r470r",
            administrator_login_password="4-v3ry-53cr37-p455w0rd")
        example_elastic_pool = azure.sql.ElasticPool("exampleElasticPool",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            server_name=example_sql_server.name,
            edition="Basic",
            dtu=50,
            db_dtu_min=0,
            db_dtu_max=5,
            pool_size=5000)
        ```

        > **NOTE on `sql.ElasticPool`:** -  The values of `edition`, `dtu`, and `pool_size` must be consistent with the [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). Any inconsistent argument configuration will be rejected.

        ## Import

        SQL Elastic Pool's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:sql/elasticPool:ElasticPool pool1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myresourcegroup/providers/Microsoft.Sql/servers/myserver/elasticPools/pool1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] db_dtu_max: The maximum DTU which will be guaranteed to all databases in the elastic pool to be created.
        :param pulumi.Input[int] db_dtu_min: The minimum DTU which will be guaranteed to all databases in the elastic pool to be created.
        :param pulumi.Input[int] dtu: The total shared DTU for the elastic pool. Valid values depend on the `edition` which has been defined. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for valid combinations.
        :param pulumi.Input[str] edition: The edition of the elastic pool to be created. Valid values are `Basic`, `Standard`, and `Premium`. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for details. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the elastic pool. This needs to be globally unique. Changing this forces a new resource to be created.
        :param pulumi.Input[int] pool_size: The maximum size in MB that all databases in the elastic pool can grow to. The maximum size must be consistent with combination of `edition` and `dtu` and the limits documented in [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). If not defined when creating an elastic pool, the value is set to the size implied by `edition` and `dtu`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the elastic pool. This must be the same as the resource group of the underlying SQL server.
        :param pulumi.Input[str] server_name: The name of the SQL Server on which to create the elastic pool. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ElasticPoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_sql_server = azure.sql.SqlServer("exampleSqlServer",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            version="12.0",
            administrator_login="4dm1n157r470r",
            administrator_login_password="4-v3ry-53cr37-p455w0rd")
        example_elastic_pool = azure.sql.ElasticPool("exampleElasticPool",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            server_name=example_sql_server.name,
            edition="Basic",
            dtu=50,
            db_dtu_min=0,
            db_dtu_max=5,
            pool_size=5000)
        ```

        > **NOTE on `sql.ElasticPool`:** -  The values of `edition`, `dtu`, and `pool_size` must be consistent with the [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). Any inconsistent argument configuration will be rejected.

        ## Import

        SQL Elastic Pool's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:sql/elasticPool:ElasticPool pool1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myresourcegroup/providers/Microsoft.Sql/servers/myserver/elasticPools/pool1
        ```

        :param str resource_name: The name of the resource.
        :param ElasticPoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ElasticPoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_dtu_max: Optional[pulumi.Input[int]] = None,
                 db_dtu_min: Optional[pulumi.Input[int]] = None,
                 dtu: Optional[pulumi.Input[int]] = None,
                 edition: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pool_size: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ElasticPoolArgs.__new__(ElasticPoolArgs)

            __props__.__dict__["db_dtu_max"] = db_dtu_max
            __props__.__dict__["db_dtu_min"] = db_dtu_min
            if dtu is None and not opts.urn:
                raise TypeError("Missing required property 'dtu'")
            __props__.__dict__["dtu"] = dtu
            if edition is None and not opts.urn:
                raise TypeError("Missing required property 'edition'")
            __props__.__dict__["edition"] = edition
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["pool_size"] = pool_size
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__["server_name"] = server_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["creation_date"] = None
        super(ElasticPool, __self__).__init__(
            'azure:sql/elasticPool:ElasticPool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            creation_date: Optional[pulumi.Input[str]] = None,
            db_dtu_max: Optional[pulumi.Input[int]] = None,
            db_dtu_min: Optional[pulumi.Input[int]] = None,
            dtu: Optional[pulumi.Input[int]] = None,
            edition: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            pool_size: Optional[pulumi.Input[int]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            server_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'ElasticPool':
        """
        Get an existing ElasticPool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] creation_date: The creation date of the SQL Elastic Pool.
        :param pulumi.Input[int] db_dtu_max: The maximum DTU which will be guaranteed to all databases in the elastic pool to be created.
        :param pulumi.Input[int] db_dtu_min: The minimum DTU which will be guaranteed to all databases in the elastic pool to be created.
        :param pulumi.Input[int] dtu: The total shared DTU for the elastic pool. Valid values depend on the `edition` which has been defined. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for valid combinations.
        :param pulumi.Input[str] edition: The edition of the elastic pool to be created. Valid values are `Basic`, `Standard`, and `Premium`. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for details. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the elastic pool. This needs to be globally unique. Changing this forces a new resource to be created.
        :param pulumi.Input[int] pool_size: The maximum size in MB that all databases in the elastic pool can grow to. The maximum size must be consistent with combination of `edition` and `dtu` and the limits documented in [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). If not defined when creating an elastic pool, the value is set to the size implied by `edition` and `dtu`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the elastic pool. This must be the same as the resource group of the underlying SQL server.
        :param pulumi.Input[str] server_name: The name of the SQL Server on which to create the elastic pool. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ElasticPoolState.__new__(_ElasticPoolState)

        __props__.__dict__["creation_date"] = creation_date
        __props__.__dict__["db_dtu_max"] = db_dtu_max
        __props__.__dict__["db_dtu_min"] = db_dtu_min
        __props__.__dict__["dtu"] = dtu
        __props__.__dict__["edition"] = edition
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["pool_size"] = pool_size
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["server_name"] = server_name
        __props__.__dict__["tags"] = tags
        return ElasticPool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The creation date of the SQL Elastic Pool.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="dbDtuMax")
    def db_dtu_max(self) -> pulumi.Output[int]:
        """
        The maximum DTU which will be guaranteed to all databases in the elastic pool to be created.
        """
        return pulumi.get(self, "db_dtu_max")

    @property
    @pulumi.getter(name="dbDtuMin")
    def db_dtu_min(self) -> pulumi.Output[int]:
        """
        The minimum DTU which will be guaranteed to all databases in the elastic pool to be created.
        """
        return pulumi.get(self, "db_dtu_min")

    @property
    @pulumi.getter
    def dtu(self) -> pulumi.Output[int]:
        """
        The total shared DTU for the elastic pool. Valid values depend on the `edition` which has been defined. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for valid combinations.
        """
        return pulumi.get(self, "dtu")

    @property
    @pulumi.getter
    def edition(self) -> pulumi.Output[str]:
        """
        The edition of the elastic pool to be created. Valid values are `Basic`, `Standard`, and `Premium`. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for details. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "edition")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the elastic pool. This needs to be globally unique. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="poolSize")
    def pool_size(self) -> pulumi.Output[int]:
        """
        The maximum size in MB that all databases in the elastic pool can grow to. The maximum size must be consistent with combination of `edition` and `dtu` and the limits documented in [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). If not defined when creating an elastic pool, the value is set to the size implied by `edition` and `dtu`.
        """
        return pulumi.get(self, "pool_size")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the elastic pool. This must be the same as the resource group of the underlying SQL server.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> pulumi.Output[str]:
        """
        The name of the SQL Server on which to create the elastic pool. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

