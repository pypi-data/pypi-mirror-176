# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['OutputSynapseArgs', 'OutputSynapse']

@pulumi.input_type
class OutputSynapseArgs:
    def __init__(__self__, *,
                 database: pulumi.Input[str],
                 password: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 server: pulumi.Input[str],
                 stream_analytics_job_name: pulumi.Input[str],
                 table: pulumi.Input[str],
                 user: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OutputSynapse resource.
        :param pulumi.Input[str] database: The name of the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: The password that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server: The name of the SQL server containing the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_job_name: The name of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: The name of the table in the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] user: The user name that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "database", database)
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "server", server)
        pulumi.set(__self__, "stream_analytics_job_name", stream_analytics_job_name)
        pulumi.set(__self__, "table", table)
        pulumi.set(__self__, "user", user)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Input[str]:
        """
        The name of the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: pulumi.Input[str]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        """
        The password that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def server(self) -> pulumi.Input[str]:
        """
        The name of the SQL server containing the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server")

    @server.setter
    def server(self, value: pulumi.Input[str]):
        pulumi.set(self, "server", value)

    @property
    @pulumi.getter(name="streamAnalyticsJobName")
    def stream_analytics_job_name(self) -> pulumi.Input[str]:
        """
        The name of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_name")

    @stream_analytics_job_name.setter
    def stream_analytics_job_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "stream_analytics_job_name", value)

    @property
    @pulumi.getter
    def table(self) -> pulumi.Input[str]:
        """
        The name of the table in the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "table")

    @table.setter
    def table(self, value: pulumi.Input[str]):
        pulumi.set(self, "table", value)

    @property
    @pulumi.getter
    def user(self) -> pulumi.Input[str]:
        """
        The user name that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: pulumi.Input[str]):
        pulumi.set(self, "user", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Stream Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _OutputSynapseState:
    def __init__(__self__, *,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_name: Optional[pulumi.Input[str]] = None,
                 table: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OutputSynapse resources.
        :param pulumi.Input[str] database: The name of the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: The password that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server: The name of the SQL server containing the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_job_name: The name of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: The name of the table in the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] user: The user name that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        if database is not None:
            pulumi.set(__self__, "database", database)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if server is not None:
            pulumi.set(__self__, "server", server)
        if stream_analytics_job_name is not None:
            pulumi.set(__self__, "stream_analytics_job_name", stream_analytics_job_name)
        if table is not None:
            pulumi.set(__self__, "table", table)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Stream Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def server(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the SQL server containing the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server")

    @server.setter
    def server(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server", value)

    @property
    @pulumi.getter(name="streamAnalyticsJobName")
    def stream_analytics_job_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_name")

    @stream_analytics_job_name.setter
    def stream_analytics_job_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stream_analytics_job_name", value)

    @property
    @pulumi.getter
    def table(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the table in the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "table")

    @table.setter
    def table(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        The user name that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)


class OutputSynapse(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_name: Optional[pulumi.Input[str]] = None,
                 table: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Stream Analytics Output to an Azure Synapse Analytics Workspace.

        ## Import

        A Stream Analytics Output to an Azure Synapse Analytics Workspace can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:streamanalytics/outputSynapse:OutputSynapse example /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/group1/providers/Microsoft.StreamAnalytics/streamingjobs/job1/outputs/output1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: The name of the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: The password that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server: The name of the SQL server containing the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_job_name: The name of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: The name of the table in the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] user: The user name that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OutputSynapseArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Stream Analytics Output to an Azure Synapse Analytics Workspace.

        ## Import

        A Stream Analytics Output to an Azure Synapse Analytics Workspace can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:streamanalytics/outputSynapse:OutputSynapse example /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/group1/providers/Microsoft.StreamAnalytics/streamingjobs/job1/outputs/output1
        ```

        :param str resource_name: The name of the resource.
        :param OutputSynapseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OutputSynapseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_name: Optional[pulumi.Input[str]] = None,
                 table: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OutputSynapseArgs.__new__(OutputSynapseArgs)

            if database is None and not opts.urn:
                raise TypeError("Missing required property 'database'")
            __props__.__dict__["database"] = database
            __props__.__dict__["name"] = name
            if password is None and not opts.urn:
                raise TypeError("Missing required property 'password'")
            __props__.__dict__["password"] = password
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if server is None and not opts.urn:
                raise TypeError("Missing required property 'server'")
            __props__.__dict__["server"] = server
            if stream_analytics_job_name is None and not opts.urn:
                raise TypeError("Missing required property 'stream_analytics_job_name'")
            __props__.__dict__["stream_analytics_job_name"] = stream_analytics_job_name
            if table is None and not opts.urn:
                raise TypeError("Missing required property 'table'")
            __props__.__dict__["table"] = table
            if user is None and not opts.urn:
                raise TypeError("Missing required property 'user'")
            __props__.__dict__["user"] = user
        super(OutputSynapse, __self__).__init__(
            'azure:streamanalytics/outputSynapse:OutputSynapse',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            database: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            server: Optional[pulumi.Input[str]] = None,
            stream_analytics_job_name: Optional[pulumi.Input[str]] = None,
            table: Optional[pulumi.Input[str]] = None,
            user: Optional[pulumi.Input[str]] = None) -> 'OutputSynapse':
        """
        Get an existing OutputSynapse resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: The name of the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: The password that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server: The name of the SQL server containing the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_job_name: The name of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: The name of the table in the Azure SQL database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] user: The user name that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OutputSynapseState.__new__(_OutputSynapseState)

        __props__.__dict__["database"] = database
        __props__.__dict__["name"] = name
        __props__.__dict__["password"] = password
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["server"] = server
        __props__.__dict__["stream_analytics_job_name"] = stream_analytics_job_name
        __props__.__dict__["table"] = table
        __props__.__dict__["user"] = user
        return OutputSynapse(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        The name of the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Stream Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        The password that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def server(self) -> pulumi.Output[str]:
        """
        The name of the SQL server containing the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server")

    @property
    @pulumi.getter(name="streamAnalyticsJobName")
    def stream_analytics_job_name(self) -> pulumi.Output[str]:
        """
        The name of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_name")

    @property
    @pulumi.getter
    def table(self) -> pulumi.Output[str]:
        """
        The name of the table in the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "table")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        """
        The user name that will be used to connect to the Azure SQL database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "user")

