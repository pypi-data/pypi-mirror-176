# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BackupInstancePostgresqlArgs', 'BackupInstancePostgresql']

@pulumi.input_type
class BackupInstancePostgresqlArgs:
    def __init__(__self__, *,
                 backup_policy_id: pulumi.Input[str],
                 database_id: pulumi.Input[str],
                 vault_id: pulumi.Input[str],
                 database_credential_key_vault_secret_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BackupInstancePostgresql resource.
        :param pulumi.Input[str] backup_policy_id: The ID of the Backup Policy.
        :param pulumi.Input[str] database_id: The ID of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] vault_id: The ID of the Backup Vault within which the PostgreSQL Backup Instance should exist. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] database_credential_key_vault_secret_id: The ID or versionless ID of the key vault secret which stores the connection string of the database.
        :param pulumi.Input[str] location: The location of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] name: The name which should be used for this Backup Instance PostgreSQL. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        pulumi.set(__self__, "backup_policy_id", backup_policy_id)
        pulumi.set(__self__, "database_id", database_id)
        pulumi.set(__self__, "vault_id", vault_id)
        if database_credential_key_vault_secret_id is not None:
            pulumi.set(__self__, "database_credential_key_vault_secret_id", database_credential_key_vault_secret_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="backupPolicyId")
    def backup_policy_id(self) -> pulumi.Input[str]:
        """
        The ID of the Backup Policy.
        """
        return pulumi.get(self, "backup_policy_id")

    @backup_policy_id.setter
    def backup_policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "backup_policy_id", value)

    @property
    @pulumi.getter(name="databaseId")
    def database_id(self) -> pulumi.Input[str]:
        """
        The ID of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "database_id")

    @database_id.setter
    def database_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_id", value)

    @property
    @pulumi.getter(name="vaultId")
    def vault_id(self) -> pulumi.Input[str]:
        """
        The ID of the Backup Vault within which the PostgreSQL Backup Instance should exist. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "vault_id")

    @vault_id.setter
    def vault_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_id", value)

    @property
    @pulumi.getter(name="databaseCredentialKeyVaultSecretId")
    def database_credential_key_vault_secret_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID or versionless ID of the key vault secret which stores the connection string of the database.
        """
        return pulumi.get(self, "database_credential_key_vault_secret_id")

    @database_credential_key_vault_secret_id.setter
    def database_credential_key_vault_secret_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_credential_key_vault_secret_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Backup Instance PostgreSQL. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _BackupInstancePostgresqlState:
    def __init__(__self__, *,
                 backup_policy_id: Optional[pulumi.Input[str]] = None,
                 database_credential_key_vault_secret_id: Optional[pulumi.Input[str]] = None,
                 database_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 vault_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BackupInstancePostgresql resources.
        :param pulumi.Input[str] backup_policy_id: The ID of the Backup Policy.
        :param pulumi.Input[str] database_credential_key_vault_secret_id: The ID or versionless ID of the key vault secret which stores the connection string of the database.
        :param pulumi.Input[str] database_id: The ID of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] location: The location of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] name: The name which should be used for this Backup Instance PostgreSQL. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] vault_id: The ID of the Backup Vault within which the PostgreSQL Backup Instance should exist. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        if backup_policy_id is not None:
            pulumi.set(__self__, "backup_policy_id", backup_policy_id)
        if database_credential_key_vault_secret_id is not None:
            pulumi.set(__self__, "database_credential_key_vault_secret_id", database_credential_key_vault_secret_id)
        if database_id is not None:
            pulumi.set(__self__, "database_id", database_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if vault_id is not None:
            pulumi.set(__self__, "vault_id", vault_id)

    @property
    @pulumi.getter(name="backupPolicyId")
    def backup_policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Backup Policy.
        """
        return pulumi.get(self, "backup_policy_id")

    @backup_policy_id.setter
    def backup_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backup_policy_id", value)

    @property
    @pulumi.getter(name="databaseCredentialKeyVaultSecretId")
    def database_credential_key_vault_secret_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID or versionless ID of the key vault secret which stores the connection string of the database.
        """
        return pulumi.get(self, "database_credential_key_vault_secret_id")

    @database_credential_key_vault_secret_id.setter
    def database_credential_key_vault_secret_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_credential_key_vault_secret_id", value)

    @property
    @pulumi.getter(name="databaseId")
    def database_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "database_id")

    @database_id.setter
    def database_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Backup Instance PostgreSQL. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="vaultId")
    def vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Backup Vault within which the PostgreSQL Backup Instance should exist. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "vault_id")

    @vault_id.setter
    def vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vault_id", value)


class BackupInstancePostgresql(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_policy_id: Optional[pulumi.Input[str]] = None,
                 database_credential_key_vault_secret_id: Optional[pulumi.Input[str]] = None,
                 database_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 vault_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Backup Instance to back up PostgreSQL.

        > **Note:** Before using this resource, there are some prerequisite permissions for configure backup and restore. See more details from <https://docs.microsoft.com/azure/backup/backup-azure-database-postgresql#prerequisite-permissions-for-configure-backup-and-restore>.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_server = azure.postgresql.Server("exampleServer",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="B_Gen5_2",
            storage_mb=5120,
            backup_retention_days=7,
            geo_redundant_backup_enabled=False,
            auto_grow_enabled=True,
            administrator_login="psqladmin",
            administrator_login_password="H@Sh1CoR3!",
            version="9.5",
            ssl_enforcement_enabled=True)
        example_firewall_rule = azure.postgresql.FirewallRule("exampleFirewallRule",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            start_ip_address="0.0.0.0",
            end_ip_address="0.0.0.0")
        example_database = azure.postgresql.Database("exampleDatabase",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            charset="UTF8",
            collation="English_United States.1252")
        example_backup_vault = azure.dataprotection.BackupVault("exampleBackupVault",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            datastore_type="VaultStore",
            redundancy="LocallyRedundant",
            identity=azure.dataprotection.BackupVaultIdentityArgs(
                type="SystemAssigned",
            ))
        example_key_vault = azure.keyvault.KeyVault("exampleKeyVault",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            tenant_id=current.tenant_id,
            sku_name="premium",
            soft_delete_retention_days=7,
            access_policies=[
                azure.keyvault.KeyVaultAccessPolicyArgs(
                    tenant_id=current.tenant_id,
                    object_id=current.object_id,
                    key_permissions=[
                        "Create",
                        "Get",
                    ],
                    secret_permissions=[
                        "Set",
                        "Get",
                        "Delete",
                        "Purge",
                        "Recover",
                    ],
                ),
                azure.keyvault.KeyVaultAccessPolicyArgs(
                    tenant_id=example_backup_vault.identity.tenant_id,
                    object_id=example_backup_vault.identity.principal_id,
                    key_permissions=[
                        "Create",
                        "Get",
                    ],
                    secret_permissions=[
                        "Set",
                        "Get",
                        "Delete",
                        "Purge",
                        "Recover",
                    ],
                ),
            ])
        example_secret = azure.keyvault.Secret("exampleSecret",
            value=pulumi.Output.all(example_server.name, example_database.name, example_server.name).apply(lambda exampleServerName, exampleDatabaseName, exampleServerName1: f"Server={example_server_name}.postgres.database.azure.com;Database={example_database_name};Port=5432;User Id=psqladmin@{example_server_name1};Password=H@Sh1CoR3!;Ssl Mode=Require;"),
            key_vault_id=example_key_vault.id)
        example_backup_policy_postgresql = azure.dataprotection.BackupPolicyPostgresql("exampleBackupPolicyPostgresql",
            resource_group_name=example_resource_group.name,
            vault_name=example_backup_vault.name,
            backup_repeating_time_intervals=["R/2021-05-23T02:30:00+00:00/P1W"],
            default_retention_duration="P4M")
        example_assignment = azure.authorization.Assignment("exampleAssignment",
            scope=example_server.id,
            role_definition_name="Reader",
            principal_id=example_backup_vault.identity.principal_id)
        example_backup_instance_postgresql = azure.dataprotection.BackupInstancePostgresql("exampleBackupInstancePostgresql",
            location=example_resource_group.location,
            vault_id=example_backup_vault.id,
            database_id=example_database.id,
            backup_policy_id=example_backup_policy_postgresql.id,
            database_credential_key_vault_secret_id=example_secret.versionless_id)
        ```

        ## Import

        Backup Instance PostgreSQL can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:dataprotection/backupInstancePostgresql:BackupInstancePostgresql example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.DataProtection/backupVaults/vault1/backupInstances/backupInstance1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_policy_id: The ID of the Backup Policy.
        :param pulumi.Input[str] database_credential_key_vault_secret_id: The ID or versionless ID of the key vault secret which stores the connection string of the database.
        :param pulumi.Input[str] database_id: The ID of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] location: The location of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] name: The name which should be used for this Backup Instance PostgreSQL. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] vault_id: The ID of the Backup Vault within which the PostgreSQL Backup Instance should exist. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BackupInstancePostgresqlArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Backup Instance to back up PostgreSQL.

        > **Note:** Before using this resource, there are some prerequisite permissions for configure backup and restore. See more details from <https://docs.microsoft.com/azure/backup/backup-azure-database-postgresql#prerequisite-permissions-for-configure-backup-and-restore>.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_server = azure.postgresql.Server("exampleServer",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="B_Gen5_2",
            storage_mb=5120,
            backup_retention_days=7,
            geo_redundant_backup_enabled=False,
            auto_grow_enabled=True,
            administrator_login="psqladmin",
            administrator_login_password="H@Sh1CoR3!",
            version="9.5",
            ssl_enforcement_enabled=True)
        example_firewall_rule = azure.postgresql.FirewallRule("exampleFirewallRule",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            start_ip_address="0.0.0.0",
            end_ip_address="0.0.0.0")
        example_database = azure.postgresql.Database("exampleDatabase",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            charset="UTF8",
            collation="English_United States.1252")
        example_backup_vault = azure.dataprotection.BackupVault("exampleBackupVault",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            datastore_type="VaultStore",
            redundancy="LocallyRedundant",
            identity=azure.dataprotection.BackupVaultIdentityArgs(
                type="SystemAssigned",
            ))
        example_key_vault = azure.keyvault.KeyVault("exampleKeyVault",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            tenant_id=current.tenant_id,
            sku_name="premium",
            soft_delete_retention_days=7,
            access_policies=[
                azure.keyvault.KeyVaultAccessPolicyArgs(
                    tenant_id=current.tenant_id,
                    object_id=current.object_id,
                    key_permissions=[
                        "Create",
                        "Get",
                    ],
                    secret_permissions=[
                        "Set",
                        "Get",
                        "Delete",
                        "Purge",
                        "Recover",
                    ],
                ),
                azure.keyvault.KeyVaultAccessPolicyArgs(
                    tenant_id=example_backup_vault.identity.tenant_id,
                    object_id=example_backup_vault.identity.principal_id,
                    key_permissions=[
                        "Create",
                        "Get",
                    ],
                    secret_permissions=[
                        "Set",
                        "Get",
                        "Delete",
                        "Purge",
                        "Recover",
                    ],
                ),
            ])
        example_secret = azure.keyvault.Secret("exampleSecret",
            value=pulumi.Output.all(example_server.name, example_database.name, example_server.name).apply(lambda exampleServerName, exampleDatabaseName, exampleServerName1: f"Server={example_server_name}.postgres.database.azure.com;Database={example_database_name};Port=5432;User Id=psqladmin@{example_server_name1};Password=H@Sh1CoR3!;Ssl Mode=Require;"),
            key_vault_id=example_key_vault.id)
        example_backup_policy_postgresql = azure.dataprotection.BackupPolicyPostgresql("exampleBackupPolicyPostgresql",
            resource_group_name=example_resource_group.name,
            vault_name=example_backup_vault.name,
            backup_repeating_time_intervals=["R/2021-05-23T02:30:00+00:00/P1W"],
            default_retention_duration="P4M")
        example_assignment = azure.authorization.Assignment("exampleAssignment",
            scope=example_server.id,
            role_definition_name="Reader",
            principal_id=example_backup_vault.identity.principal_id)
        example_backup_instance_postgresql = azure.dataprotection.BackupInstancePostgresql("exampleBackupInstancePostgresql",
            location=example_resource_group.location,
            vault_id=example_backup_vault.id,
            database_id=example_database.id,
            backup_policy_id=example_backup_policy_postgresql.id,
            database_credential_key_vault_secret_id=example_secret.versionless_id)
        ```

        ## Import

        Backup Instance PostgreSQL can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:dataprotection/backupInstancePostgresql:BackupInstancePostgresql example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.DataProtection/backupVaults/vault1/backupInstances/backupInstance1
        ```

        :param str resource_name: The name of the resource.
        :param BackupInstancePostgresqlArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BackupInstancePostgresqlArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_policy_id: Optional[pulumi.Input[str]] = None,
                 database_credential_key_vault_secret_id: Optional[pulumi.Input[str]] = None,
                 database_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 vault_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BackupInstancePostgresqlArgs.__new__(BackupInstancePostgresqlArgs)

            if backup_policy_id is None and not opts.urn:
                raise TypeError("Missing required property 'backup_policy_id'")
            __props__.__dict__["backup_policy_id"] = backup_policy_id
            __props__.__dict__["database_credential_key_vault_secret_id"] = database_credential_key_vault_secret_id
            if database_id is None and not opts.urn:
                raise TypeError("Missing required property 'database_id'")
            __props__.__dict__["database_id"] = database_id
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if vault_id is None and not opts.urn:
                raise TypeError("Missing required property 'vault_id'")
            __props__.__dict__["vault_id"] = vault_id
        super(BackupInstancePostgresql, __self__).__init__(
            'azure:dataprotection/backupInstancePostgresql:BackupInstancePostgresql',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backup_policy_id: Optional[pulumi.Input[str]] = None,
            database_credential_key_vault_secret_id: Optional[pulumi.Input[str]] = None,
            database_id: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            vault_id: Optional[pulumi.Input[str]] = None) -> 'BackupInstancePostgresql':
        """
        Get an existing BackupInstancePostgresql resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_policy_id: The ID of the Backup Policy.
        :param pulumi.Input[str] database_credential_key_vault_secret_id: The ID or versionless ID of the key vault secret which stores the connection string of the database.
        :param pulumi.Input[str] database_id: The ID of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] location: The location of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] name: The name which should be used for this Backup Instance PostgreSQL. Changing this forces a new Backup Instance PostgreSQL to be created.
        :param pulumi.Input[str] vault_id: The ID of the Backup Vault within which the PostgreSQL Backup Instance should exist. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BackupInstancePostgresqlState.__new__(_BackupInstancePostgresqlState)

        __props__.__dict__["backup_policy_id"] = backup_policy_id
        __props__.__dict__["database_credential_key_vault_secret_id"] = database_credential_key_vault_secret_id
        __props__.__dict__["database_id"] = database_id
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["vault_id"] = vault_id
        return BackupInstancePostgresql(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backupPolicyId")
    def backup_policy_id(self) -> pulumi.Output[str]:
        """
        The ID of the Backup Policy.
        """
        return pulumi.get(self, "backup_policy_id")

    @property
    @pulumi.getter(name="databaseCredentialKeyVaultSecretId")
    def database_credential_key_vault_secret_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID or versionless ID of the key vault secret which stores the connection string of the database.
        """
        return pulumi.get(self, "database_credential_key_vault_secret_id")

    @property
    @pulumi.getter(name="databaseId")
    def database_id(self) -> pulumi.Output[str]:
        """
        The ID of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "database_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the source database. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Backup Instance PostgreSQL. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="vaultId")
    def vault_id(self) -> pulumi.Output[str]:
        """
        The ID of the Backup Vault within which the PostgreSQL Backup Instance should exist. Changing this forces a new Backup Instance PostgreSQL to be created.
        """
        return pulumi.get(self, "vault_id")

