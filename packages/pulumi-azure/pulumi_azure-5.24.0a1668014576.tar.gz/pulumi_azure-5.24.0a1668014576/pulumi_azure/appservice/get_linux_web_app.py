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
    'GetLinuxWebAppResult',
    'AwaitableGetLinuxWebAppResult',
    'get_linux_web_app',
    'get_linux_web_app_output',
]

@pulumi.output_type
class GetLinuxWebAppResult:
    """
    A collection of values returned by getLinuxWebApp.
    """
    def __init__(__self__, app_metadata=None, app_settings=None, auth_settings=None, backups=None, client_affinity_enabled=None, client_certificate_enabled=None, client_certificate_exclusion_paths=None, client_certificate_mode=None, connection_strings=None, custom_domain_verification_id=None, default_hostname=None, enabled=None, https_only=None, id=None, identities=None, key_vault_reference_identity_id=None, kind=None, location=None, logs=None, name=None, outbound_ip_address_lists=None, outbound_ip_addresses=None, possible_outbound_ip_address_lists=None, possible_outbound_ip_addresses=None, resource_group_name=None, service_plan_id=None, site_configs=None, site_credentials=None, sticky_settings=None, storage_accounts=None, tags=None, virtual_network_subnet_id=None):
        if app_metadata and not isinstance(app_metadata, dict):
            raise TypeError("Expected argument 'app_metadata' to be a dict")
        pulumi.set(__self__, "app_metadata", app_metadata)
        if app_settings and not isinstance(app_settings, dict):
            raise TypeError("Expected argument 'app_settings' to be a dict")
        pulumi.set(__self__, "app_settings", app_settings)
        if auth_settings and not isinstance(auth_settings, list):
            raise TypeError("Expected argument 'auth_settings' to be a list")
        pulumi.set(__self__, "auth_settings", auth_settings)
        if backups and not isinstance(backups, list):
            raise TypeError("Expected argument 'backups' to be a list")
        pulumi.set(__self__, "backups", backups)
        if client_affinity_enabled and not isinstance(client_affinity_enabled, bool):
            raise TypeError("Expected argument 'client_affinity_enabled' to be a bool")
        pulumi.set(__self__, "client_affinity_enabled", client_affinity_enabled)
        if client_certificate_enabled and not isinstance(client_certificate_enabled, bool):
            raise TypeError("Expected argument 'client_certificate_enabled' to be a bool")
        pulumi.set(__self__, "client_certificate_enabled", client_certificate_enabled)
        if client_certificate_exclusion_paths and not isinstance(client_certificate_exclusion_paths, str):
            raise TypeError("Expected argument 'client_certificate_exclusion_paths' to be a str")
        pulumi.set(__self__, "client_certificate_exclusion_paths", client_certificate_exclusion_paths)
        if client_certificate_mode and not isinstance(client_certificate_mode, str):
            raise TypeError("Expected argument 'client_certificate_mode' to be a str")
        pulumi.set(__self__, "client_certificate_mode", client_certificate_mode)
        if connection_strings and not isinstance(connection_strings, list):
            raise TypeError("Expected argument 'connection_strings' to be a list")
        pulumi.set(__self__, "connection_strings", connection_strings)
        if custom_domain_verification_id and not isinstance(custom_domain_verification_id, str):
            raise TypeError("Expected argument 'custom_domain_verification_id' to be a str")
        pulumi.set(__self__, "custom_domain_verification_id", custom_domain_verification_id)
        if default_hostname and not isinstance(default_hostname, str):
            raise TypeError("Expected argument 'default_hostname' to be a str")
        pulumi.set(__self__, "default_hostname", default_hostname)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if https_only and not isinstance(https_only, bool):
            raise TypeError("Expected argument 'https_only' to be a bool")
        pulumi.set(__self__, "https_only", https_only)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        pulumi.set(__self__, "identities", identities)
        if key_vault_reference_identity_id and not isinstance(key_vault_reference_identity_id, str):
            raise TypeError("Expected argument 'key_vault_reference_identity_id' to be a str")
        pulumi.set(__self__, "key_vault_reference_identity_id", key_vault_reference_identity_id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if logs and not isinstance(logs, list):
            raise TypeError("Expected argument 'logs' to be a list")
        pulumi.set(__self__, "logs", logs)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if outbound_ip_address_lists and not isinstance(outbound_ip_address_lists, list):
            raise TypeError("Expected argument 'outbound_ip_address_lists' to be a list")
        pulumi.set(__self__, "outbound_ip_address_lists", outbound_ip_address_lists)
        if outbound_ip_addresses and not isinstance(outbound_ip_addresses, str):
            raise TypeError("Expected argument 'outbound_ip_addresses' to be a str")
        pulumi.set(__self__, "outbound_ip_addresses", outbound_ip_addresses)
        if possible_outbound_ip_address_lists and not isinstance(possible_outbound_ip_address_lists, list):
            raise TypeError("Expected argument 'possible_outbound_ip_address_lists' to be a list")
        pulumi.set(__self__, "possible_outbound_ip_address_lists", possible_outbound_ip_address_lists)
        if possible_outbound_ip_addresses and not isinstance(possible_outbound_ip_addresses, str):
            raise TypeError("Expected argument 'possible_outbound_ip_addresses' to be a str")
        pulumi.set(__self__, "possible_outbound_ip_addresses", possible_outbound_ip_addresses)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if service_plan_id and not isinstance(service_plan_id, str):
            raise TypeError("Expected argument 'service_plan_id' to be a str")
        pulumi.set(__self__, "service_plan_id", service_plan_id)
        if site_configs and not isinstance(site_configs, list):
            raise TypeError("Expected argument 'site_configs' to be a list")
        pulumi.set(__self__, "site_configs", site_configs)
        if site_credentials and not isinstance(site_credentials, list):
            raise TypeError("Expected argument 'site_credentials' to be a list")
        pulumi.set(__self__, "site_credentials", site_credentials)
        if sticky_settings and not isinstance(sticky_settings, list):
            raise TypeError("Expected argument 'sticky_settings' to be a list")
        pulumi.set(__self__, "sticky_settings", sticky_settings)
        if storage_accounts and not isinstance(storage_accounts, list):
            raise TypeError("Expected argument 'storage_accounts' to be a list")
        pulumi.set(__self__, "storage_accounts", storage_accounts)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if virtual_network_subnet_id and not isinstance(virtual_network_subnet_id, str):
            raise TypeError("Expected argument 'virtual_network_subnet_id' to be a str")
        pulumi.set(__self__, "virtual_network_subnet_id", virtual_network_subnet_id)

    @property
    @pulumi.getter(name="appMetadata")
    def app_metadata(self) -> Mapping[str, str]:
        """
        An `app_metadata` block as defined below.
        """
        return pulumi.get(self, "app_metadata")

    @property
    @pulumi.getter(name="appSettings")
    def app_settings(self) -> Mapping[str, str]:
        """
        An `app_settings` block as defined below.
        """
        return pulumi.get(self, "app_settings")

    @property
    @pulumi.getter(name="authSettings")
    def auth_settings(self) -> Sequence['outputs.GetLinuxWebAppAuthSettingResult']:
        """
        An `auth_settings` block as defined below.
        """
        return pulumi.get(self, "auth_settings")

    @property
    @pulumi.getter
    def backups(self) -> Sequence['outputs.GetLinuxWebAppBackupResult']:
        """
        A `backup` block as defined below.
        """
        return pulumi.get(self, "backups")

    @property
    @pulumi.getter(name="clientAffinityEnabled")
    def client_affinity_enabled(self) -> bool:
        """
        Is Client Affinity enabled?
        """
        return pulumi.get(self, "client_affinity_enabled")

    @property
    @pulumi.getter(name="clientCertificateEnabled")
    def client_certificate_enabled(self) -> bool:
        """
        Are Client Certificates enabled?
        """
        return pulumi.get(self, "client_certificate_enabled")

    @property
    @pulumi.getter(name="clientCertificateExclusionPaths")
    def client_certificate_exclusion_paths(self) -> str:
        """
        Paths to exclude when using client certificates, separated by ;
        """
        return pulumi.get(self, "client_certificate_exclusion_paths")

    @property
    @pulumi.getter(name="clientCertificateMode")
    def client_certificate_mode(self) -> str:
        """
        The Client Certificate mode.
        """
        return pulumi.get(self, "client_certificate_mode")

    @property
    @pulumi.getter(name="connectionStrings")
    def connection_strings(self) -> Sequence['outputs.GetLinuxWebAppConnectionStringResult']:
        """
        A `connection_string` block as defined below.
        """
        return pulumi.get(self, "connection_strings")

    @property
    @pulumi.getter(name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> str:
        """
        The identifier used by App Service to perform domain ownership verification via DNS TXT record.
        """
        return pulumi.get(self, "custom_domain_verification_id")

    @property
    @pulumi.getter(name="defaultHostname")
    def default_hostname(self) -> str:
        """
        The default hostname of the Linux Web App.
        """
        return pulumi.get(self, "default_hostname")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Is the Backup enabled?
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="httpsOnly")
    def https_only(self) -> bool:
        """
        Should the Linux Web App require HTTPS connections.
        """
        return pulumi.get(self, "https_only")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetLinuxWebAppIdentityResult']:
        """
        A `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter(name="keyVaultReferenceIdentityId")
    def key_vault_reference_identity_id(self) -> str:
        return pulumi.get(self, "key_vault_reference_identity_id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The Kind value for this Linux Web App.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure Region where the Linux Web App exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def logs(self) -> Sequence['outputs.GetLinuxWebAppLogResult']:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, "logs")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of this Storage Account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outboundIpAddressLists")
    def outbound_ip_address_lists(self) -> Sequence[str]:
        """
        A `outbound_ip_address_list` block as defined below.
        """
        return pulumi.get(self, "outbound_ip_address_lists")

    @property
    @pulumi.getter(name="outboundIpAddresses")
    def outbound_ip_addresses(self) -> str:
        """
        A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12`.
        """
        return pulumi.get(self, "outbound_ip_addresses")

    @property
    @pulumi.getter(name="possibleOutboundIpAddressLists")
    def possible_outbound_ip_address_lists(self) -> Sequence[str]:
        """
        A `possible_outbound_ip_address_list` block as defined below.
        """
        return pulumi.get(self, "possible_outbound_ip_address_lists")

    @property
    @pulumi.getter(name="possibleOutboundIpAddresses")
    def possible_outbound_ip_addresses(self) -> str:
        """
        A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12,52.143.43.17` - not all of which are necessarily in use. Superset of `outbound_ip_addresses`.
        """
        return pulumi.get(self, "possible_outbound_ip_addresses")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="servicePlanId")
    def service_plan_id(self) -> str:
        """
        The ID of the Service Plan that this Linux Web App exists in.
        """
        return pulumi.get(self, "service_plan_id")

    @property
    @pulumi.getter(name="siteConfigs")
    def site_configs(self) -> Sequence['outputs.GetLinuxWebAppSiteConfigResult']:
        """
        A `site_config` block as defined below.
        """
        return pulumi.get(self, "site_configs")

    @property
    @pulumi.getter(name="siteCredentials")
    def site_credentials(self) -> Sequence['outputs.GetLinuxWebAppSiteCredentialResult']:
        """
        A `site_credential` block as defined below.
        """
        return pulumi.get(self, "site_credentials")

    @property
    @pulumi.getter(name="stickySettings")
    def sticky_settings(self) -> Sequence['outputs.GetLinuxWebAppStickySettingResult']:
        """
        A `sticky_settings` block as defined below.
        """
        return pulumi.get(self, "sticky_settings")

    @property
    @pulumi.getter(name="storageAccounts")
    def storage_accounts(self) -> Sequence['outputs.GetLinuxWebAppStorageAccountResult']:
        """
        A `storage_account` block as defined below.
        """
        return pulumi.get(self, "storage_accounts")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the Linux Web App.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> str:
        return pulumi.get(self, "virtual_network_subnet_id")


class AwaitableGetLinuxWebAppResult(GetLinuxWebAppResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLinuxWebAppResult(
            app_metadata=self.app_metadata,
            app_settings=self.app_settings,
            auth_settings=self.auth_settings,
            backups=self.backups,
            client_affinity_enabled=self.client_affinity_enabled,
            client_certificate_enabled=self.client_certificate_enabled,
            client_certificate_exclusion_paths=self.client_certificate_exclusion_paths,
            client_certificate_mode=self.client_certificate_mode,
            connection_strings=self.connection_strings,
            custom_domain_verification_id=self.custom_domain_verification_id,
            default_hostname=self.default_hostname,
            enabled=self.enabled,
            https_only=self.https_only,
            id=self.id,
            identities=self.identities,
            key_vault_reference_identity_id=self.key_vault_reference_identity_id,
            kind=self.kind,
            location=self.location,
            logs=self.logs,
            name=self.name,
            outbound_ip_address_lists=self.outbound_ip_address_lists,
            outbound_ip_addresses=self.outbound_ip_addresses,
            possible_outbound_ip_address_lists=self.possible_outbound_ip_address_lists,
            possible_outbound_ip_addresses=self.possible_outbound_ip_addresses,
            resource_group_name=self.resource_group_name,
            service_plan_id=self.service_plan_id,
            site_configs=self.site_configs,
            site_credentials=self.site_credentials,
            sticky_settings=self.sticky_settings,
            storage_accounts=self.storage_accounts,
            tags=self.tags,
            virtual_network_subnet_id=self.virtual_network_subnet_id)


def get_linux_web_app(name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLinuxWebAppResult:
    """
    Use this data source to access information about an existing Linux Web App.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.appservice.get_linux_web_app(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Linux Web App.
    :param str resource_group_name: The name of the Resource Group where the Linux Web App exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:appservice/getLinuxWebApp:getLinuxWebApp', __args__, opts=opts, typ=GetLinuxWebAppResult).value

    return AwaitableGetLinuxWebAppResult(
        app_metadata=__ret__.app_metadata,
        app_settings=__ret__.app_settings,
        auth_settings=__ret__.auth_settings,
        backups=__ret__.backups,
        client_affinity_enabled=__ret__.client_affinity_enabled,
        client_certificate_enabled=__ret__.client_certificate_enabled,
        client_certificate_exclusion_paths=__ret__.client_certificate_exclusion_paths,
        client_certificate_mode=__ret__.client_certificate_mode,
        connection_strings=__ret__.connection_strings,
        custom_domain_verification_id=__ret__.custom_domain_verification_id,
        default_hostname=__ret__.default_hostname,
        enabled=__ret__.enabled,
        https_only=__ret__.https_only,
        id=__ret__.id,
        identities=__ret__.identities,
        key_vault_reference_identity_id=__ret__.key_vault_reference_identity_id,
        kind=__ret__.kind,
        location=__ret__.location,
        logs=__ret__.logs,
        name=__ret__.name,
        outbound_ip_address_lists=__ret__.outbound_ip_address_lists,
        outbound_ip_addresses=__ret__.outbound_ip_addresses,
        possible_outbound_ip_address_lists=__ret__.possible_outbound_ip_address_lists,
        possible_outbound_ip_addresses=__ret__.possible_outbound_ip_addresses,
        resource_group_name=__ret__.resource_group_name,
        service_plan_id=__ret__.service_plan_id,
        site_configs=__ret__.site_configs,
        site_credentials=__ret__.site_credentials,
        sticky_settings=__ret__.sticky_settings,
        storage_accounts=__ret__.storage_accounts,
        tags=__ret__.tags,
        virtual_network_subnet_id=__ret__.virtual_network_subnet_id)


@_utilities.lift_output_func(get_linux_web_app)
def get_linux_web_app_output(name: Optional[pulumi.Input[str]] = None,
                             resource_group_name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLinuxWebAppResult]:
    """
    Use this data source to access information about an existing Linux Web App.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.appservice.get_linux_web_app(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Linux Web App.
    :param str resource_group_name: The name of the Resource Group where the Linux Web App exists.
    """
    ...
