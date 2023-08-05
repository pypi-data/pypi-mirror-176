# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RoleAssignmentArgs', 'RoleAssignment']

@pulumi.input_type
class RoleAssignmentArgs:
    def __init__(__self__, *,
                 principal_id: pulumi.Input[str],
                 role_name: pulumi.Input[str],
                 synapse_spark_pool_id: Optional[pulumi.Input[str]] = None,
                 synapse_workspace_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RoleAssignment resource.
        :param pulumi.Input[str] principal_id: The ID of the Principal (User, Group or Service Principal) to assign the Synapse Role Definition to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] role_name: The Role Name of the Synapse Built-In Role. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_spark_pool_id: The Synapse Spark Pool which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_workspace_id: The Synapse Workspace which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "role_name", role_name)
        if synapse_spark_pool_id is not None:
            pulumi.set(__self__, "synapse_spark_pool_id", synapse_spark_pool_id)
        if synapse_workspace_id is not None:
            pulumi.set(__self__, "synapse_workspace_id", synapse_workspace_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Input[str]:
        """
        The ID of the Principal (User, Group or Service Principal) to assign the Synapse Role Definition to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> pulumi.Input[str]:
        """
        The Role Name of the Synapse Built-In Role. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "role_name")

    @role_name.setter
    def role_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_name", value)

    @property
    @pulumi.getter(name="synapseSparkPoolId")
    def synapse_spark_pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Synapse Spark Pool which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_spark_pool_id")

    @synapse_spark_pool_id.setter
    def synapse_spark_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "synapse_spark_pool_id", value)

    @property
    @pulumi.getter(name="synapseWorkspaceId")
    def synapse_workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Synapse Workspace which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_workspace_id")

    @synapse_workspace_id.setter
    def synapse_workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "synapse_workspace_id", value)


@pulumi.input_type
class _RoleAssignmentState:
    def __init__(__self__, *,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 synapse_spark_pool_id: Optional[pulumi.Input[str]] = None,
                 synapse_workspace_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RoleAssignment resources.
        :param pulumi.Input[str] principal_id: The ID of the Principal (User, Group or Service Principal) to assign the Synapse Role Definition to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] role_name: The Role Name of the Synapse Built-In Role. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_spark_pool_id: The Synapse Spark Pool which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_workspace_id: The Synapse Workspace which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if role_name is not None:
            pulumi.set(__self__, "role_name", role_name)
        if synapse_spark_pool_id is not None:
            pulumi.set(__self__, "synapse_spark_pool_id", synapse_spark_pool_id)
        if synapse_workspace_id is not None:
            pulumi.set(__self__, "synapse_workspace_id", synapse_workspace_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Principal (User, Group or Service Principal) to assign the Synapse Role Definition to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Role Name of the Synapse Built-In Role. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "role_name")

    @role_name.setter
    def role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_name", value)

    @property
    @pulumi.getter(name="synapseSparkPoolId")
    def synapse_spark_pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Synapse Spark Pool which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_spark_pool_id")

    @synapse_spark_pool_id.setter
    def synapse_spark_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "synapse_spark_pool_id", value)

    @property
    @pulumi.getter(name="synapseWorkspaceId")
    def synapse_workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Synapse Workspace which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_workspace_id")

    @synapse_workspace_id.setter
    def synapse_workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "synapse_workspace_id", value)


class RoleAssignment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 synapse_spark_pool_id: Optional[pulumi.Input[str]] = None,
                 synapse_workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Synapse Role Assignment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="StorageV2",
            is_hns_enabled=True)
        example_data_lake_gen2_filesystem = azure.storage.DataLakeGen2Filesystem("exampleDataLakeGen2Filesystem", storage_account_id=example_account.id)
        example_workspace = azure.synapse.Workspace("exampleWorkspace",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            storage_data_lake_gen2_filesystem_id=example_data_lake_gen2_filesystem.id,
            sql_administrator_login="sqladminuser",
            sql_administrator_login_password="H@Sh1CoR3!",
            identity=azure.synapse.WorkspaceIdentityArgs(
                type="SystemAssigned",
            ))
        example_firewall_rule = azure.synapse.FirewallRule("exampleFirewallRule",
            synapse_workspace_id=example_workspace.id,
            start_ip_address="0.0.0.0",
            end_ip_address="255.255.255.255")
        current = azure.core.get_client_config()
        example_role_assignment = azure.synapse.RoleAssignment("exampleRoleAssignment",
            synapse_workspace_id=example_workspace.id,
            role_name="Synapse SQL Administrator",
            principal_id=current.object_id,
            opts=pulumi.ResourceOptions(depends_on=[example_firewall_rule]))
        ```

        ## Import

        Synapse Role Assignment can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:synapse/roleAssignment:RoleAssignment example "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Synapse/workspaces/workspace1|000000000000"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] principal_id: The ID of the Principal (User, Group or Service Principal) to assign the Synapse Role Definition to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] role_name: The Role Name of the Synapse Built-In Role. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_spark_pool_id: The Synapse Spark Pool which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_workspace_id: The Synapse Workspace which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RoleAssignmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Synapse Role Assignment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="StorageV2",
            is_hns_enabled=True)
        example_data_lake_gen2_filesystem = azure.storage.DataLakeGen2Filesystem("exampleDataLakeGen2Filesystem", storage_account_id=example_account.id)
        example_workspace = azure.synapse.Workspace("exampleWorkspace",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            storage_data_lake_gen2_filesystem_id=example_data_lake_gen2_filesystem.id,
            sql_administrator_login="sqladminuser",
            sql_administrator_login_password="H@Sh1CoR3!",
            identity=azure.synapse.WorkspaceIdentityArgs(
                type="SystemAssigned",
            ))
        example_firewall_rule = azure.synapse.FirewallRule("exampleFirewallRule",
            synapse_workspace_id=example_workspace.id,
            start_ip_address="0.0.0.0",
            end_ip_address="255.255.255.255")
        current = azure.core.get_client_config()
        example_role_assignment = azure.synapse.RoleAssignment("exampleRoleAssignment",
            synapse_workspace_id=example_workspace.id,
            role_name="Synapse SQL Administrator",
            principal_id=current.object_id,
            opts=pulumi.ResourceOptions(depends_on=[example_firewall_rule]))
        ```

        ## Import

        Synapse Role Assignment can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:synapse/roleAssignment:RoleAssignment example "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Synapse/workspaces/workspace1|000000000000"
        ```

        :param str resource_name: The name of the resource.
        :param RoleAssignmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RoleAssignmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 synapse_spark_pool_id: Optional[pulumi.Input[str]] = None,
                 synapse_workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RoleAssignmentArgs.__new__(RoleAssignmentArgs)

            if principal_id is None and not opts.urn:
                raise TypeError("Missing required property 'principal_id'")
            __props__.__dict__["principal_id"] = principal_id
            if role_name is None and not opts.urn:
                raise TypeError("Missing required property 'role_name'")
            __props__.__dict__["role_name"] = role_name
            __props__.__dict__["synapse_spark_pool_id"] = synapse_spark_pool_id
            __props__.__dict__["synapse_workspace_id"] = synapse_workspace_id
        super(RoleAssignment, __self__).__init__(
            'azure:synapse/roleAssignment:RoleAssignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            principal_id: Optional[pulumi.Input[str]] = None,
            role_name: Optional[pulumi.Input[str]] = None,
            synapse_spark_pool_id: Optional[pulumi.Input[str]] = None,
            synapse_workspace_id: Optional[pulumi.Input[str]] = None) -> 'RoleAssignment':
        """
        Get an existing RoleAssignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] principal_id: The ID of the Principal (User, Group or Service Principal) to assign the Synapse Role Definition to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] role_name: The Role Name of the Synapse Built-In Role. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_spark_pool_id: The Synapse Spark Pool which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_workspace_id: The Synapse Workspace which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RoleAssignmentState.__new__(_RoleAssignmentState)

        __props__.__dict__["principal_id"] = principal_id
        __props__.__dict__["role_name"] = role_name
        __props__.__dict__["synapse_spark_pool_id"] = synapse_spark_pool_id
        __props__.__dict__["synapse_workspace_id"] = synapse_workspace_id
        return RoleAssignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Output[str]:
        """
        The ID of the Principal (User, Group or Service Principal) to assign the Synapse Role Definition to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> pulumi.Output[str]:
        """
        The Role Name of the Synapse Built-In Role. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "role_name")

    @property
    @pulumi.getter(name="synapseSparkPoolId")
    def synapse_spark_pool_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Synapse Spark Pool which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_spark_pool_id")

    @property
    @pulumi.getter(name="synapseWorkspaceId")
    def synapse_workspace_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Synapse Workspace which the Synapse Role Assignment applies to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_workspace_id")

