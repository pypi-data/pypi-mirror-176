# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SqlDedicatedGatewayArgs', 'SqlDedicatedGateway']

@pulumi.input_type
class SqlDedicatedGatewayArgs:
    def __init__(__self__, *,
                 cosmosdb_account_id: pulumi.Input[str],
                 instance_count: pulumi.Input[int],
                 instance_size: pulumi.Input[str]):
        """
        The set of arguments for constructing a SqlDedicatedGateway resource.
        :param pulumi.Input[str] cosmosdb_account_id: The resource ID of the CosmosDB Account. Changing this forces a new resource to be created.
        :param pulumi.Input[int] instance_count: The instance count for the CosmosDB SQL Dedicated Gateway. Possible value is between `1` and `5`.
        :param pulumi.Input[str] instance_size: The instance size for the CosmosDB SQL Dedicated Gateway. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "cosmosdb_account_id", cosmosdb_account_id)
        pulumi.set(__self__, "instance_count", instance_count)
        pulumi.set(__self__, "instance_size", instance_size)

    @property
    @pulumi.getter(name="cosmosdbAccountId")
    def cosmosdb_account_id(self) -> pulumi.Input[str]:
        """
        The resource ID of the CosmosDB Account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "cosmosdb_account_id")

    @cosmosdb_account_id.setter
    def cosmosdb_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "cosmosdb_account_id", value)

    @property
    @pulumi.getter(name="instanceCount")
    def instance_count(self) -> pulumi.Input[int]:
        """
        The instance count for the CosmosDB SQL Dedicated Gateway. Possible value is between `1` and `5`.
        """
        return pulumi.get(self, "instance_count")

    @instance_count.setter
    def instance_count(self, value: pulumi.Input[int]):
        pulumi.set(self, "instance_count", value)

    @property
    @pulumi.getter(name="instanceSize")
    def instance_size(self) -> pulumi.Input[str]:
        """
        The instance size for the CosmosDB SQL Dedicated Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "instance_size")

    @instance_size.setter
    def instance_size(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_size", value)


@pulumi.input_type
class _SqlDedicatedGatewayState:
    def __init__(__self__, *,
                 cosmosdb_account_id: Optional[pulumi.Input[str]] = None,
                 instance_count: Optional[pulumi.Input[int]] = None,
                 instance_size: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SqlDedicatedGateway resources.
        :param pulumi.Input[str] cosmosdb_account_id: The resource ID of the CosmosDB Account. Changing this forces a new resource to be created.
        :param pulumi.Input[int] instance_count: The instance count for the CosmosDB SQL Dedicated Gateway. Possible value is between `1` and `5`.
        :param pulumi.Input[str] instance_size: The instance size for the CosmosDB SQL Dedicated Gateway. Changing this forces a new resource to be created.
        """
        if cosmosdb_account_id is not None:
            pulumi.set(__self__, "cosmosdb_account_id", cosmosdb_account_id)
        if instance_count is not None:
            pulumi.set(__self__, "instance_count", instance_count)
        if instance_size is not None:
            pulumi.set(__self__, "instance_size", instance_size)

    @property
    @pulumi.getter(name="cosmosdbAccountId")
    def cosmosdb_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource ID of the CosmosDB Account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "cosmosdb_account_id")

    @cosmosdb_account_id.setter
    def cosmosdb_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cosmosdb_account_id", value)

    @property
    @pulumi.getter(name="instanceCount")
    def instance_count(self) -> Optional[pulumi.Input[int]]:
        """
        The instance count for the CosmosDB SQL Dedicated Gateway. Possible value is between `1` and `5`.
        """
        return pulumi.get(self, "instance_count")

    @instance_count.setter
    def instance_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "instance_count", value)

    @property
    @pulumi.getter(name="instanceSize")
    def instance_size(self) -> Optional[pulumi.Input[str]]:
        """
        The instance size for the CosmosDB SQL Dedicated Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "instance_size")

    @instance_size.setter
    def instance_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_size", value)


class SqlDedicatedGateway(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cosmosdb_account_id: Optional[pulumi.Input[str]] = None,
                 instance_count: Optional[pulumi.Input[int]] = None,
                 instance_size: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a SQL Dedicated Gateway within a Cosmos DB Account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.cosmosdb.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            offer_type="Standard",
            kind="GlobalDocumentDB",
            consistency_policy=azure.cosmosdb.AccountConsistencyPolicyArgs(
                consistency_level="BoundedStaleness",
            ),
            geo_locations=[azure.cosmosdb.AccountGeoLocationArgs(
                location=example_resource_group.location,
                failover_priority=0,
            )])
        example_sql_dedicated_gateway = azure.cosmosdb.SqlDedicatedGateway("exampleSqlDedicatedGateway",
            cosmosdb_account_id=example_account.id,
            instance_count=1,
            instance_size="Cosmos.D4s")
        ```

        ## Import

        CosmosDB SQL Dedicated Gateways can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:cosmosdb/sqlDedicatedGateway:SqlDedicatedGateway example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.DocumentDB/databaseAccounts/account1/services/SqlDedicatedGateway
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cosmosdb_account_id: The resource ID of the CosmosDB Account. Changing this forces a new resource to be created.
        :param pulumi.Input[int] instance_count: The instance count for the CosmosDB SQL Dedicated Gateway. Possible value is between `1` and `5`.
        :param pulumi.Input[str] instance_size: The instance size for the CosmosDB SQL Dedicated Gateway. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SqlDedicatedGatewayArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a SQL Dedicated Gateway within a Cosmos DB Account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.cosmosdb.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            offer_type="Standard",
            kind="GlobalDocumentDB",
            consistency_policy=azure.cosmosdb.AccountConsistencyPolicyArgs(
                consistency_level="BoundedStaleness",
            ),
            geo_locations=[azure.cosmosdb.AccountGeoLocationArgs(
                location=example_resource_group.location,
                failover_priority=0,
            )])
        example_sql_dedicated_gateway = azure.cosmosdb.SqlDedicatedGateway("exampleSqlDedicatedGateway",
            cosmosdb_account_id=example_account.id,
            instance_count=1,
            instance_size="Cosmos.D4s")
        ```

        ## Import

        CosmosDB SQL Dedicated Gateways can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:cosmosdb/sqlDedicatedGateway:SqlDedicatedGateway example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.DocumentDB/databaseAccounts/account1/services/SqlDedicatedGateway
        ```

        :param str resource_name: The name of the resource.
        :param SqlDedicatedGatewayArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SqlDedicatedGatewayArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cosmosdb_account_id: Optional[pulumi.Input[str]] = None,
                 instance_count: Optional[pulumi.Input[int]] = None,
                 instance_size: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SqlDedicatedGatewayArgs.__new__(SqlDedicatedGatewayArgs)

            if cosmosdb_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'cosmosdb_account_id'")
            __props__.__dict__["cosmosdb_account_id"] = cosmosdb_account_id
            if instance_count is None and not opts.urn:
                raise TypeError("Missing required property 'instance_count'")
            __props__.__dict__["instance_count"] = instance_count
            if instance_size is None and not opts.urn:
                raise TypeError("Missing required property 'instance_size'")
            __props__.__dict__["instance_size"] = instance_size
        super(SqlDedicatedGateway, __self__).__init__(
            'azure:cosmosdb/sqlDedicatedGateway:SqlDedicatedGateway',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cosmosdb_account_id: Optional[pulumi.Input[str]] = None,
            instance_count: Optional[pulumi.Input[int]] = None,
            instance_size: Optional[pulumi.Input[str]] = None) -> 'SqlDedicatedGateway':
        """
        Get an existing SqlDedicatedGateway resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cosmosdb_account_id: The resource ID of the CosmosDB Account. Changing this forces a new resource to be created.
        :param pulumi.Input[int] instance_count: The instance count for the CosmosDB SQL Dedicated Gateway. Possible value is between `1` and `5`.
        :param pulumi.Input[str] instance_size: The instance size for the CosmosDB SQL Dedicated Gateway. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SqlDedicatedGatewayState.__new__(_SqlDedicatedGatewayState)

        __props__.__dict__["cosmosdb_account_id"] = cosmosdb_account_id
        __props__.__dict__["instance_count"] = instance_count
        __props__.__dict__["instance_size"] = instance_size
        return SqlDedicatedGateway(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cosmosdbAccountId")
    def cosmosdb_account_id(self) -> pulumi.Output[str]:
        """
        The resource ID of the CosmosDB Account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "cosmosdb_account_id")

    @property
    @pulumi.getter(name="instanceCount")
    def instance_count(self) -> pulumi.Output[int]:
        """
        The instance count for the CosmosDB SQL Dedicated Gateway. Possible value is between `1` and `5`.
        """
        return pulumi.get(self, "instance_count")

    @property
    @pulumi.getter(name="instanceSize")
    def instance_size(self) -> pulumi.Output[str]:
        """
        The instance size for the CosmosDB SQL Dedicated Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "instance_size")

