# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SqlFunctionArgs', 'SqlFunction']

@pulumi.input_type
class SqlFunctionArgs:
    def __init__(__self__, *,
                 body: pulumi.Input[str],
                 container_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SqlFunction resource.
        :param pulumi.Input[str] body: Body of the User Defined Function.
        :param pulumi.Input[str] container_id: The id of the Cosmos DB SQL Container to create the SQL User Defined Function within. Changing this forces a new SQL User Defined Function to be created.
        :param pulumi.Input[str] name: The name which should be used for this SQL User Defined Function. Changing this forces a new SQL User Defined Function to be created.
        """
        pulumi.set(__self__, "body", body)
        pulumi.set(__self__, "container_id", container_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def body(self) -> pulumi.Input[str]:
        """
        Body of the User Defined Function.
        """
        return pulumi.get(self, "body")

    @body.setter
    def body(self, value: pulumi.Input[str]):
        pulumi.set(self, "body", value)

    @property
    @pulumi.getter(name="containerId")
    def container_id(self) -> pulumi.Input[str]:
        """
        The id of the Cosmos DB SQL Container to create the SQL User Defined Function within. Changing this forces a new SQL User Defined Function to be created.
        """
        return pulumi.get(self, "container_id")

    @container_id.setter
    def container_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "container_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this SQL User Defined Function. Changing this forces a new SQL User Defined Function to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _SqlFunctionState:
    def __init__(__self__, *,
                 body: Optional[pulumi.Input[str]] = None,
                 container_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SqlFunction resources.
        :param pulumi.Input[str] body: Body of the User Defined Function.
        :param pulumi.Input[str] container_id: The id of the Cosmos DB SQL Container to create the SQL User Defined Function within. Changing this forces a new SQL User Defined Function to be created.
        :param pulumi.Input[str] name: The name which should be used for this SQL User Defined Function. Changing this forces a new SQL User Defined Function to be created.
        """
        if body is not None:
            pulumi.set(__self__, "body", body)
        if container_id is not None:
            pulumi.set(__self__, "container_id", container_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def body(self) -> Optional[pulumi.Input[str]]:
        """
        Body of the User Defined Function.
        """
        return pulumi.get(self, "body")

    @body.setter
    def body(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "body", value)

    @property
    @pulumi.getter(name="containerId")
    def container_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the Cosmos DB SQL Container to create the SQL User Defined Function within. Changing this forces a new SQL User Defined Function to be created.
        """
        return pulumi.get(self, "container_id")

    @container_id.setter
    def container_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this SQL User Defined Function. Changing this forces a new SQL User Defined Function to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class SqlFunction(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 body: Optional[pulumi.Input[str]] = None,
                 container_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an SQL User Defined Function.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_account = azure.cosmosdb.get_account(name="tfex-cosmosdb-account",
            resource_group_name="tfex-cosmosdb-account-rg")
        example_sql_database = azure.cosmosdb.SqlDatabase("exampleSqlDatabase",
            resource_group_name=example_account.resource_group_name,
            account_name=example_account.name,
            throughput=400)
        example_sql_container = azure.cosmosdb.SqlContainer("exampleSqlContainer",
            resource_group_name=example_account.resource_group_name,
            account_name=example_account.name,
            database_name=example_sql_database.name,
            partition_key_path="/id")
        example_sql_function = azure.cosmosdb.SqlFunction("exampleSqlFunction",
            container_id=example_sql_container.id,
            body="function trigger(){}")
        ```

        ## Import

        SQL User Defined Functions can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:cosmosdb/sqlFunction:SqlFunction example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.DocumentDB/databaseAccounts/account1/sqlDatabases/database1/containers/container1/userDefinedFunctions/userDefinedFunction1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] body: Body of the User Defined Function.
        :param pulumi.Input[str] container_id: The id of the Cosmos DB SQL Container to create the SQL User Defined Function within. Changing this forces a new SQL User Defined Function to be created.
        :param pulumi.Input[str] name: The name which should be used for this SQL User Defined Function. Changing this forces a new SQL User Defined Function to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SqlFunctionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an SQL User Defined Function.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_account = azure.cosmosdb.get_account(name="tfex-cosmosdb-account",
            resource_group_name="tfex-cosmosdb-account-rg")
        example_sql_database = azure.cosmosdb.SqlDatabase("exampleSqlDatabase",
            resource_group_name=example_account.resource_group_name,
            account_name=example_account.name,
            throughput=400)
        example_sql_container = azure.cosmosdb.SqlContainer("exampleSqlContainer",
            resource_group_name=example_account.resource_group_name,
            account_name=example_account.name,
            database_name=example_sql_database.name,
            partition_key_path="/id")
        example_sql_function = azure.cosmosdb.SqlFunction("exampleSqlFunction",
            container_id=example_sql_container.id,
            body="function trigger(){}")
        ```

        ## Import

        SQL User Defined Functions can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:cosmosdb/sqlFunction:SqlFunction example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.DocumentDB/databaseAccounts/account1/sqlDatabases/database1/containers/container1/userDefinedFunctions/userDefinedFunction1
        ```

        :param str resource_name: The name of the resource.
        :param SqlFunctionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SqlFunctionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 body: Optional[pulumi.Input[str]] = None,
                 container_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SqlFunctionArgs.__new__(SqlFunctionArgs)

            if body is None and not opts.urn:
                raise TypeError("Missing required property 'body'")
            __props__.__dict__["body"] = body
            if container_id is None and not opts.urn:
                raise TypeError("Missing required property 'container_id'")
            __props__.__dict__["container_id"] = container_id
            __props__.__dict__["name"] = name
        super(SqlFunction, __self__).__init__(
            'azure:cosmosdb/sqlFunction:SqlFunction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            body: Optional[pulumi.Input[str]] = None,
            container_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'SqlFunction':
        """
        Get an existing SqlFunction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] body: Body of the User Defined Function.
        :param pulumi.Input[str] container_id: The id of the Cosmos DB SQL Container to create the SQL User Defined Function within. Changing this forces a new SQL User Defined Function to be created.
        :param pulumi.Input[str] name: The name which should be used for this SQL User Defined Function. Changing this forces a new SQL User Defined Function to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SqlFunctionState.__new__(_SqlFunctionState)

        __props__.__dict__["body"] = body
        __props__.__dict__["container_id"] = container_id
        __props__.__dict__["name"] = name
        return SqlFunction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def body(self) -> pulumi.Output[str]:
        """
        Body of the User Defined Function.
        """
        return pulumi.get(self, "body")

    @property
    @pulumi.getter(name="containerId")
    def container_id(self) -> pulumi.Output[str]:
        """
        The id of the Cosmos DB SQL Container to create the SQL User Defined Function within. Changing this forces a new SQL User Defined Function to be created.
        """
        return pulumi.get(self, "container_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this SQL User Defined Function. Changing this forces a new SQL User Defined Function to be created.
        """
        return pulumi.get(self, "name")

