# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ServerMicrosoftSupportAuditingPolicyArgs', 'ServerMicrosoftSupportAuditingPolicy']

@pulumi.input_type
class ServerMicrosoftSupportAuditingPolicyArgs:
    def __init__(__self__, *,
                 server_id: pulumi.Input[str],
                 blob_storage_endpoint: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_monitoring_enabled: Optional[pulumi.Input[bool]] = None,
                 storage_account_access_key: Optional[pulumi.Input[str]] = None,
                 storage_account_subscription_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ServerMicrosoftSupportAuditingPolicy resource.
        :param pulumi.Input[str] server_id: The ID of the SQL Server to set the extended auditing policy. Changing this forces a new resource to be created.
        :param pulumi.Input[str] blob_storage_endpoint: The blob storage endpoint (e.g. https://example.blob.core.windows.net). This blob storage will hold all Microsoft support auditing logs.
        :param pulumi.Input[bool] enabled: Whether to enable the extended auditing policy. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[bool] log_monitoring_enabled: Enable audit events to Azure Monitor? To enable server audit events to Azure Monitor, please enable its main database audit events to Azure Monitor.
        :param pulumi.Input[str] storage_account_access_key: The access key to use for the auditing storage account.
        :param pulumi.Input[str] storage_account_subscription_id: The ID of the Subscription containing the Storage Account.
        """
        pulumi.set(__self__, "server_id", server_id)
        if blob_storage_endpoint is not None:
            pulumi.set(__self__, "blob_storage_endpoint", blob_storage_endpoint)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if log_monitoring_enabled is not None:
            pulumi.set(__self__, "log_monitoring_enabled", log_monitoring_enabled)
        if storage_account_access_key is not None:
            pulumi.set(__self__, "storage_account_access_key", storage_account_access_key)
        if storage_account_subscription_id is not None:
            pulumi.set(__self__, "storage_account_subscription_id", storage_account_subscription_id)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Input[str]:
        """
        The ID of the SQL Server to set the extended auditing policy. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter(name="blobStorageEndpoint")
    def blob_storage_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The blob storage endpoint (e.g. https://example.blob.core.windows.net). This blob storage will hold all Microsoft support auditing logs.
        """
        return pulumi.get(self, "blob_storage_endpoint")

    @blob_storage_endpoint.setter
    def blob_storage_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "blob_storage_endpoint", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable the extended auditing policy. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="logMonitoringEnabled")
    def log_monitoring_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable audit events to Azure Monitor? To enable server audit events to Azure Monitor, please enable its main database audit events to Azure Monitor.
        """
        return pulumi.get(self, "log_monitoring_enabled")

    @log_monitoring_enabled.setter
    def log_monitoring_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "log_monitoring_enabled", value)

    @property
    @pulumi.getter(name="storageAccountAccessKey")
    def storage_account_access_key(self) -> Optional[pulumi.Input[str]]:
        """
        The access key to use for the auditing storage account.
        """
        return pulumi.get(self, "storage_account_access_key")

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_access_key", value)

    @property
    @pulumi.getter(name="storageAccountSubscriptionId")
    def storage_account_subscription_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Subscription containing the Storage Account.
        """
        return pulumi.get(self, "storage_account_subscription_id")

    @storage_account_subscription_id.setter
    def storage_account_subscription_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_subscription_id", value)


@pulumi.input_type
class _ServerMicrosoftSupportAuditingPolicyState:
    def __init__(__self__, *,
                 blob_storage_endpoint: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_monitoring_enabled: Optional[pulumi.Input[bool]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 storage_account_access_key: Optional[pulumi.Input[str]] = None,
                 storage_account_subscription_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServerMicrosoftSupportAuditingPolicy resources.
        :param pulumi.Input[str] blob_storage_endpoint: The blob storage endpoint (e.g. https://example.blob.core.windows.net). This blob storage will hold all Microsoft support auditing logs.
        :param pulumi.Input[bool] enabled: Whether to enable the extended auditing policy. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[bool] log_monitoring_enabled: Enable audit events to Azure Monitor? To enable server audit events to Azure Monitor, please enable its main database audit events to Azure Monitor.
        :param pulumi.Input[str] server_id: The ID of the SQL Server to set the extended auditing policy. Changing this forces a new resource to be created.
        :param pulumi.Input[str] storage_account_access_key: The access key to use for the auditing storage account.
        :param pulumi.Input[str] storage_account_subscription_id: The ID of the Subscription containing the Storage Account.
        """
        if blob_storage_endpoint is not None:
            pulumi.set(__self__, "blob_storage_endpoint", blob_storage_endpoint)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if log_monitoring_enabled is not None:
            pulumi.set(__self__, "log_monitoring_enabled", log_monitoring_enabled)
        if server_id is not None:
            pulumi.set(__self__, "server_id", server_id)
        if storage_account_access_key is not None:
            pulumi.set(__self__, "storage_account_access_key", storage_account_access_key)
        if storage_account_subscription_id is not None:
            pulumi.set(__self__, "storage_account_subscription_id", storage_account_subscription_id)

    @property
    @pulumi.getter(name="blobStorageEndpoint")
    def blob_storage_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The blob storage endpoint (e.g. https://example.blob.core.windows.net). This blob storage will hold all Microsoft support auditing logs.
        """
        return pulumi.get(self, "blob_storage_endpoint")

    @blob_storage_endpoint.setter
    def blob_storage_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "blob_storage_endpoint", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable the extended auditing policy. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="logMonitoringEnabled")
    def log_monitoring_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable audit events to Azure Monitor? To enable server audit events to Azure Monitor, please enable its main database audit events to Azure Monitor.
        """
        return pulumi.get(self, "log_monitoring_enabled")

    @log_monitoring_enabled.setter
    def log_monitoring_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "log_monitoring_enabled", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the SQL Server to set the extended auditing policy. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter(name="storageAccountAccessKey")
    def storage_account_access_key(self) -> Optional[pulumi.Input[str]]:
        """
        The access key to use for the auditing storage account.
        """
        return pulumi.get(self, "storage_account_access_key")

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_access_key", value)

    @property
    @pulumi.getter(name="storageAccountSubscriptionId")
    def storage_account_subscription_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Subscription containing the Storage Account.
        """
        return pulumi.get(self, "storage_account_subscription_id")

    @storage_account_subscription_id.setter
    def storage_account_subscription_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_subscription_id", value)


class ServerMicrosoftSupportAuditingPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 blob_storage_endpoint: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_monitoring_enabled: Optional[pulumi.Input[bool]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 storage_account_access_key: Optional[pulumi.Input[str]] = None,
                 storage_account_subscription_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a MS SQL Server Microsoft Support Auditing Policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_server = azure.mssql.Server("exampleServer",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            version="12.0",
            administrator_login="missadministrator",
            administrator_login_password="AdminPassword123!")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS")
        example_server_microsoft_support_auditing_policy = azure.mssql.ServerMicrosoftSupportAuditingPolicy("exampleServerMicrosoftSupportAuditingPolicy",
            server_id=example_server.id,
            blob_storage_endpoint=example_account.primary_blob_endpoint,
            storage_account_access_key=example_account.primary_access_key)
        ```
        ### With Storage Account Behind VNet And Firewall
        ```python
        import pulumi
        import pulumi_azure as azure

        primary = azure.core.get_subscription()
        example_client_config = azure.core.get_client_config()
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.0.2.0/24"],
            service_endpoints=[
                "Microsoft.Sql",
                "Microsoft.Storage",
            ],
            enforce_private_link_endpoint_network_policies=True)
        example_server = azure.mssql.Server("exampleServer",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            version="12.0",
            administrator_login="missadministrator",
            administrator_login_password="AdminPassword123!",
            minimum_tls_version="1.2",
            identity=azure.mssql.ServerIdentityArgs(
                type="SystemAssigned",
            ))
        example_assignment = azure.authorization.Assignment("exampleAssignment",
            scope=primary.id,
            role_definition_name="Storage Blob Data Contributor",
            principal_id=example_server.identity.principal_id)
        sqlvnetrule = azure.sql.VirtualNetworkRule("sqlvnetrule",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            subnet_id=example_subnet.id)
        example_firewall_rule = azure.sql.FirewallRule("exampleFirewallRule",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            start_ip_address="0.0.0.0",
            end_ip_address="0.0.0.0")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="StorageV2",
            allow_nested_items_to_be_public=False,
            network_rules=azure.storage.AccountNetworkRulesArgs(
                default_action="Deny",
                ip_rules=["127.0.0.1"],
                virtual_network_subnet_ids=[example_subnet.id],
                bypasses=["AzureServices"],
            ),
            identity=azure.storage.AccountIdentityArgs(
                type="SystemAssigned",
            ))
        example_server_microsoft_support_auditing_policy = azure.mssql.ServerMicrosoftSupportAuditingPolicy("exampleServerMicrosoftSupportAuditingPolicy",
            blob_storage_endpoint=example_account.primary_blob_endpoint,
            server_id=example_server.id,
            log_monitoring_enabled=False,
            storage_account_subscription_id=azurerm_subscription["primary"]["subscription_id"],
            opts=pulumi.ResourceOptions(depends_on=[
                    example_assignment,
                    example_account,
                ]))
        ```

        ## Import

        MS SQL Server Microsoft Support Auditing Policies can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:mssql/serverMicrosoftSupportAuditingPolicy:ServerMicrosoftSupportAuditingPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Sql/servers/sqlServer1/devOpsAuditingSettings/default
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] blob_storage_endpoint: The blob storage endpoint (e.g. https://example.blob.core.windows.net). This blob storage will hold all Microsoft support auditing logs.
        :param pulumi.Input[bool] enabled: Whether to enable the extended auditing policy. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[bool] log_monitoring_enabled: Enable audit events to Azure Monitor? To enable server audit events to Azure Monitor, please enable its main database audit events to Azure Monitor.
        :param pulumi.Input[str] server_id: The ID of the SQL Server to set the extended auditing policy. Changing this forces a new resource to be created.
        :param pulumi.Input[str] storage_account_access_key: The access key to use for the auditing storage account.
        :param pulumi.Input[str] storage_account_subscription_id: The ID of the Subscription containing the Storage Account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServerMicrosoftSupportAuditingPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a MS SQL Server Microsoft Support Auditing Policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_server = azure.mssql.Server("exampleServer",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            version="12.0",
            administrator_login="missadministrator",
            administrator_login_password="AdminPassword123!")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS")
        example_server_microsoft_support_auditing_policy = azure.mssql.ServerMicrosoftSupportAuditingPolicy("exampleServerMicrosoftSupportAuditingPolicy",
            server_id=example_server.id,
            blob_storage_endpoint=example_account.primary_blob_endpoint,
            storage_account_access_key=example_account.primary_access_key)
        ```
        ### With Storage Account Behind VNet And Firewall
        ```python
        import pulumi
        import pulumi_azure as azure

        primary = azure.core.get_subscription()
        example_client_config = azure.core.get_client_config()
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.0.2.0/24"],
            service_endpoints=[
                "Microsoft.Sql",
                "Microsoft.Storage",
            ],
            enforce_private_link_endpoint_network_policies=True)
        example_server = azure.mssql.Server("exampleServer",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            version="12.0",
            administrator_login="missadministrator",
            administrator_login_password="AdminPassword123!",
            minimum_tls_version="1.2",
            identity=azure.mssql.ServerIdentityArgs(
                type="SystemAssigned",
            ))
        example_assignment = azure.authorization.Assignment("exampleAssignment",
            scope=primary.id,
            role_definition_name="Storage Blob Data Contributor",
            principal_id=example_server.identity.principal_id)
        sqlvnetrule = azure.sql.VirtualNetworkRule("sqlvnetrule",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            subnet_id=example_subnet.id)
        example_firewall_rule = azure.sql.FirewallRule("exampleFirewallRule",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            start_ip_address="0.0.0.0",
            end_ip_address="0.0.0.0")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="StorageV2",
            allow_nested_items_to_be_public=False,
            network_rules=azure.storage.AccountNetworkRulesArgs(
                default_action="Deny",
                ip_rules=["127.0.0.1"],
                virtual_network_subnet_ids=[example_subnet.id],
                bypasses=["AzureServices"],
            ),
            identity=azure.storage.AccountIdentityArgs(
                type="SystemAssigned",
            ))
        example_server_microsoft_support_auditing_policy = azure.mssql.ServerMicrosoftSupportAuditingPolicy("exampleServerMicrosoftSupportAuditingPolicy",
            blob_storage_endpoint=example_account.primary_blob_endpoint,
            server_id=example_server.id,
            log_monitoring_enabled=False,
            storage_account_subscription_id=azurerm_subscription["primary"]["subscription_id"],
            opts=pulumi.ResourceOptions(depends_on=[
                    example_assignment,
                    example_account,
                ]))
        ```

        ## Import

        MS SQL Server Microsoft Support Auditing Policies can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:mssql/serverMicrosoftSupportAuditingPolicy:ServerMicrosoftSupportAuditingPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Sql/servers/sqlServer1/devOpsAuditingSettings/default
        ```

        :param str resource_name: The name of the resource.
        :param ServerMicrosoftSupportAuditingPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServerMicrosoftSupportAuditingPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 blob_storage_endpoint: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_monitoring_enabled: Optional[pulumi.Input[bool]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 storage_account_access_key: Optional[pulumi.Input[str]] = None,
                 storage_account_subscription_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServerMicrosoftSupportAuditingPolicyArgs.__new__(ServerMicrosoftSupportAuditingPolicyArgs)

            __props__.__dict__["blob_storage_endpoint"] = blob_storage_endpoint
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["log_monitoring_enabled"] = log_monitoring_enabled
            if server_id is None and not opts.urn:
                raise TypeError("Missing required property 'server_id'")
            __props__.__dict__["server_id"] = server_id
            __props__.__dict__["storage_account_access_key"] = storage_account_access_key
            __props__.__dict__["storage_account_subscription_id"] = storage_account_subscription_id
        super(ServerMicrosoftSupportAuditingPolicy, __self__).__init__(
            'azure:mssql/serverMicrosoftSupportAuditingPolicy:ServerMicrosoftSupportAuditingPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            blob_storage_endpoint: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            log_monitoring_enabled: Optional[pulumi.Input[bool]] = None,
            server_id: Optional[pulumi.Input[str]] = None,
            storage_account_access_key: Optional[pulumi.Input[str]] = None,
            storage_account_subscription_id: Optional[pulumi.Input[str]] = None) -> 'ServerMicrosoftSupportAuditingPolicy':
        """
        Get an existing ServerMicrosoftSupportAuditingPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] blob_storage_endpoint: The blob storage endpoint (e.g. https://example.blob.core.windows.net). This blob storage will hold all Microsoft support auditing logs.
        :param pulumi.Input[bool] enabled: Whether to enable the extended auditing policy. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[bool] log_monitoring_enabled: Enable audit events to Azure Monitor? To enable server audit events to Azure Monitor, please enable its main database audit events to Azure Monitor.
        :param pulumi.Input[str] server_id: The ID of the SQL Server to set the extended auditing policy. Changing this forces a new resource to be created.
        :param pulumi.Input[str] storage_account_access_key: The access key to use for the auditing storage account.
        :param pulumi.Input[str] storage_account_subscription_id: The ID of the Subscription containing the Storage Account.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServerMicrosoftSupportAuditingPolicyState.__new__(_ServerMicrosoftSupportAuditingPolicyState)

        __props__.__dict__["blob_storage_endpoint"] = blob_storage_endpoint
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["log_monitoring_enabled"] = log_monitoring_enabled
        __props__.__dict__["server_id"] = server_id
        __props__.__dict__["storage_account_access_key"] = storage_account_access_key
        __props__.__dict__["storage_account_subscription_id"] = storage_account_subscription_id
        return ServerMicrosoftSupportAuditingPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="blobStorageEndpoint")
    def blob_storage_endpoint(self) -> pulumi.Output[Optional[str]]:
        """
        The blob storage endpoint (e.g. https://example.blob.core.windows.net). This blob storage will hold all Microsoft support auditing logs.
        """
        return pulumi.get(self, "blob_storage_endpoint")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to enable the extended auditing policy. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="logMonitoringEnabled")
    def log_monitoring_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable audit events to Azure Monitor? To enable server audit events to Azure Monitor, please enable its main database audit events to Azure Monitor.
        """
        return pulumi.get(self, "log_monitoring_enabled")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Output[str]:
        """
        The ID of the SQL Server to set the extended auditing policy. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter(name="storageAccountAccessKey")
    def storage_account_access_key(self) -> pulumi.Output[Optional[str]]:
        """
        The access key to use for the auditing storage account.
        """
        return pulumi.get(self, "storage_account_access_key")

    @property
    @pulumi.getter(name="storageAccountSubscriptionId")
    def storage_account_subscription_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Subscription containing the Storage Account.
        """
        return pulumi.get(self, "storage_account_subscription_id")

