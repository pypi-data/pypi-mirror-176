# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['GatewayHostNameConfigurationArgs', 'GatewayHostNameConfiguration']

@pulumi.input_type
class GatewayHostNameConfigurationArgs:
    def __init__(__self__, *,
                 api_management_id: pulumi.Input[str],
                 certificate_id: pulumi.Input[str],
                 gateway_name: pulumi.Input[str],
                 host_name: pulumi.Input[str],
                 http2_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 request_client_certificate_enabled: Optional[pulumi.Input[bool]] = None,
                 tls10_enabled: Optional[pulumi.Input[bool]] = None,
                 tls11_enabled: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a GatewayHostNameConfiguration resource.
        :param pulumi.Input[str] api_management_id: The ID of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] certificate_id: The certificate ID to be used for TLS connection establishment.
        :param pulumi.Input[str] gateway_name: The name of the API Management Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] host_name: The host name to use for the API Management Gateway Host Name Configuration.
        :param pulumi.Input[bool] http2_enabled: Whether HTTP/2.0 is supported.
        :param pulumi.Input[str] name: The name of the API Management Gateway Host Name Configuration. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] request_client_certificate_enabled: Whether the API Management Gateway requests a client certificate.
        :param pulumi.Input[bool] tls10_enabled: Whether TLS 1.0 is supported.
        :param pulumi.Input[bool] tls11_enabled: Whether TLS 1.1 is supported.
        """
        pulumi.set(__self__, "api_management_id", api_management_id)
        pulumi.set(__self__, "certificate_id", certificate_id)
        pulumi.set(__self__, "gateway_name", gateway_name)
        pulumi.set(__self__, "host_name", host_name)
        if http2_enabled is not None:
            pulumi.set(__self__, "http2_enabled", http2_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if request_client_certificate_enabled is not None:
            pulumi.set(__self__, "request_client_certificate_enabled", request_client_certificate_enabled)
        if tls10_enabled is not None:
            pulumi.set(__self__, "tls10_enabled", tls10_enabled)
        if tls11_enabled is not None:
            pulumi.set(__self__, "tls11_enabled", tls11_enabled)

    @property
    @pulumi.getter(name="apiManagementId")
    def api_management_id(self) -> pulumi.Input[str]:
        """
        The ID of the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_id")

    @api_management_id.setter
    def api_management_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_management_id", value)

    @property
    @pulumi.getter(name="certificateId")
    def certificate_id(self) -> pulumi.Input[str]:
        """
        The certificate ID to be used for TLS connection establishment.
        """
        return pulumi.get(self, "certificate_id")

    @certificate_id.setter
    def certificate_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_id", value)

    @property
    @pulumi.getter(name="gatewayName")
    def gateway_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "gateway_name")

    @gateway_name.setter
    def gateway_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "gateway_name", value)

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Input[str]:
        """
        The host name to use for the API Management Gateway Host Name Configuration.
        """
        return pulumi.get(self, "host_name")

    @host_name.setter
    def host_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "host_name", value)

    @property
    @pulumi.getter(name="http2Enabled")
    def http2_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether HTTP/2.0 is supported.
        """
        return pulumi.get(self, "http2_enabled")

    @http2_enabled.setter
    def http2_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "http2_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API Management Gateway Host Name Configuration. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="requestClientCertificateEnabled")
    def request_client_certificate_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the API Management Gateway requests a client certificate.
        """
        return pulumi.get(self, "request_client_certificate_enabled")

    @request_client_certificate_enabled.setter
    def request_client_certificate_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "request_client_certificate_enabled", value)

    @property
    @pulumi.getter(name="tls10Enabled")
    def tls10_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether TLS 1.0 is supported.
        """
        return pulumi.get(self, "tls10_enabled")

    @tls10_enabled.setter
    def tls10_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "tls10_enabled", value)

    @property
    @pulumi.getter(name="tls11Enabled")
    def tls11_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether TLS 1.1 is supported.
        """
        return pulumi.get(self, "tls11_enabled")

    @tls11_enabled.setter
    def tls11_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "tls11_enabled", value)


@pulumi.input_type
class _GatewayHostNameConfigurationState:
    def __init__(__self__, *,
                 api_management_id: Optional[pulumi.Input[str]] = None,
                 certificate_id: Optional[pulumi.Input[str]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 http2_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 request_client_certificate_enabled: Optional[pulumi.Input[bool]] = None,
                 tls10_enabled: Optional[pulumi.Input[bool]] = None,
                 tls11_enabled: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering GatewayHostNameConfiguration resources.
        :param pulumi.Input[str] api_management_id: The ID of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] certificate_id: The certificate ID to be used for TLS connection establishment.
        :param pulumi.Input[str] gateway_name: The name of the API Management Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] host_name: The host name to use for the API Management Gateway Host Name Configuration.
        :param pulumi.Input[bool] http2_enabled: Whether HTTP/2.0 is supported.
        :param pulumi.Input[str] name: The name of the API Management Gateway Host Name Configuration. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] request_client_certificate_enabled: Whether the API Management Gateway requests a client certificate.
        :param pulumi.Input[bool] tls10_enabled: Whether TLS 1.0 is supported.
        :param pulumi.Input[bool] tls11_enabled: Whether TLS 1.1 is supported.
        """
        if api_management_id is not None:
            pulumi.set(__self__, "api_management_id", api_management_id)
        if certificate_id is not None:
            pulumi.set(__self__, "certificate_id", certificate_id)
        if gateway_name is not None:
            pulumi.set(__self__, "gateway_name", gateway_name)
        if host_name is not None:
            pulumi.set(__self__, "host_name", host_name)
        if http2_enabled is not None:
            pulumi.set(__self__, "http2_enabled", http2_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if request_client_certificate_enabled is not None:
            pulumi.set(__self__, "request_client_certificate_enabled", request_client_certificate_enabled)
        if tls10_enabled is not None:
            pulumi.set(__self__, "tls10_enabled", tls10_enabled)
        if tls11_enabled is not None:
            pulumi.set(__self__, "tls11_enabled", tls11_enabled)

    @property
    @pulumi.getter(name="apiManagementId")
    def api_management_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_id")

    @api_management_id.setter
    def api_management_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_management_id", value)

    @property
    @pulumi.getter(name="certificateId")
    def certificate_id(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate ID to be used for TLS connection establishment.
        """
        return pulumi.get(self, "certificate_id")

    @certificate_id.setter
    def certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_id", value)

    @property
    @pulumi.getter(name="gatewayName")
    def gateway_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API Management Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "gateway_name")

    @gateway_name.setter
    def gateway_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gateway_name", value)

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> Optional[pulumi.Input[str]]:
        """
        The host name to use for the API Management Gateway Host Name Configuration.
        """
        return pulumi.get(self, "host_name")

    @host_name.setter
    def host_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_name", value)

    @property
    @pulumi.getter(name="http2Enabled")
    def http2_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether HTTP/2.0 is supported.
        """
        return pulumi.get(self, "http2_enabled")

    @http2_enabled.setter
    def http2_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "http2_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API Management Gateway Host Name Configuration. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="requestClientCertificateEnabled")
    def request_client_certificate_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the API Management Gateway requests a client certificate.
        """
        return pulumi.get(self, "request_client_certificate_enabled")

    @request_client_certificate_enabled.setter
    def request_client_certificate_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "request_client_certificate_enabled", value)

    @property
    @pulumi.getter(name="tls10Enabled")
    def tls10_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether TLS 1.0 is supported.
        """
        return pulumi.get(self, "tls10_enabled")

    @tls10_enabled.setter
    def tls10_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "tls10_enabled", value)

    @property
    @pulumi.getter(name="tls11Enabled")
    def tls11_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether TLS 1.1 is supported.
        """
        return pulumi.get(self, "tls11_enabled")

    @tls11_enabled.setter
    def tls11_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "tls11_enabled", value)


class GatewayHostNameConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_id: Optional[pulumi.Input[str]] = None,
                 certificate_id: Optional[pulumi.Input[str]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 http2_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 request_client_certificate_enabled: Optional[pulumi.Input[bool]] = None,
                 tls10_enabled: Optional[pulumi.Input[bool]] = None,
                 tls11_enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Manages an API Management Gateway Host Name Configuration.

        ## Example Usage

        ```python
        import pulumi
        import base64
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="pub1",
            publisher_email="pub1@email.com",
            sku_name="Consumption_0")
        example_gateway = azure.apimanagement.Gateway("exampleGateway",
            api_management_id=example_service.id,
            description="Example API Management gateway",
            location_data=azure.apimanagement.GatewayLocationDataArgs(
                name="example name",
                city="example city",
                district="example district",
                region="example region",
            ))
        example_certificate = azure.apimanagement.Certificate("exampleCertificate",
            api_management_name=example_service.name,
            resource_group_name=example_resource_group.name,
            data=(lambda path: base64.b64encode(open(path).read().encode()).decode())("example.pfx"))
        example_gateway_host_name_configuration = azure.apimanagement.GatewayHostNameConfiguration("exampleGatewayHostNameConfiguration",
            api_management_id=example_service.id,
            gateway_name=example_gateway.name,
            certificate_id=example_certificate.id,
            host_name="example-host-name",
            request_client_certificate_enabled=True,
            http2_enabled=True,
            tls10_enabled=True,
            tls11_enabled=False)
        ```

        ## Import

        API Management Gateway Host Name Configuration can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/gatewayHostNameConfiguration:GatewayHostNameConfiguration example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ApiManagement/service/service1/gateways/gateway1/hostnameConfigurations/hc1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_id: The ID of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] certificate_id: The certificate ID to be used for TLS connection establishment.
        :param pulumi.Input[str] gateway_name: The name of the API Management Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] host_name: The host name to use for the API Management Gateway Host Name Configuration.
        :param pulumi.Input[bool] http2_enabled: Whether HTTP/2.0 is supported.
        :param pulumi.Input[str] name: The name of the API Management Gateway Host Name Configuration. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] request_client_certificate_enabled: Whether the API Management Gateway requests a client certificate.
        :param pulumi.Input[bool] tls10_enabled: Whether TLS 1.0 is supported.
        :param pulumi.Input[bool] tls11_enabled: Whether TLS 1.1 is supported.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GatewayHostNameConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an API Management Gateway Host Name Configuration.

        ## Example Usage

        ```python
        import pulumi
        import base64
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="pub1",
            publisher_email="pub1@email.com",
            sku_name="Consumption_0")
        example_gateway = azure.apimanagement.Gateway("exampleGateway",
            api_management_id=example_service.id,
            description="Example API Management gateway",
            location_data=azure.apimanagement.GatewayLocationDataArgs(
                name="example name",
                city="example city",
                district="example district",
                region="example region",
            ))
        example_certificate = azure.apimanagement.Certificate("exampleCertificate",
            api_management_name=example_service.name,
            resource_group_name=example_resource_group.name,
            data=(lambda path: base64.b64encode(open(path).read().encode()).decode())("example.pfx"))
        example_gateway_host_name_configuration = azure.apimanagement.GatewayHostNameConfiguration("exampleGatewayHostNameConfiguration",
            api_management_id=example_service.id,
            gateway_name=example_gateway.name,
            certificate_id=example_certificate.id,
            host_name="example-host-name",
            request_client_certificate_enabled=True,
            http2_enabled=True,
            tls10_enabled=True,
            tls11_enabled=False)
        ```

        ## Import

        API Management Gateway Host Name Configuration can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/gatewayHostNameConfiguration:GatewayHostNameConfiguration example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ApiManagement/service/service1/gateways/gateway1/hostnameConfigurations/hc1
        ```

        :param str resource_name: The name of the resource.
        :param GatewayHostNameConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GatewayHostNameConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_id: Optional[pulumi.Input[str]] = None,
                 certificate_id: Optional[pulumi.Input[str]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 http2_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 request_client_certificate_enabled: Optional[pulumi.Input[bool]] = None,
                 tls10_enabled: Optional[pulumi.Input[bool]] = None,
                 tls11_enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GatewayHostNameConfigurationArgs.__new__(GatewayHostNameConfigurationArgs)

            if api_management_id is None and not opts.urn:
                raise TypeError("Missing required property 'api_management_id'")
            __props__.__dict__["api_management_id"] = api_management_id
            if certificate_id is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_id'")
            __props__.__dict__["certificate_id"] = certificate_id
            if gateway_name is None and not opts.urn:
                raise TypeError("Missing required property 'gateway_name'")
            __props__.__dict__["gateway_name"] = gateway_name
            if host_name is None and not opts.urn:
                raise TypeError("Missing required property 'host_name'")
            __props__.__dict__["host_name"] = host_name
            __props__.__dict__["http2_enabled"] = http2_enabled
            __props__.__dict__["name"] = name
            __props__.__dict__["request_client_certificate_enabled"] = request_client_certificate_enabled
            __props__.__dict__["tls10_enabled"] = tls10_enabled
            __props__.__dict__["tls11_enabled"] = tls11_enabled
        super(GatewayHostNameConfiguration, __self__).__init__(
            'azure:apimanagement/gatewayHostNameConfiguration:GatewayHostNameConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_management_id: Optional[pulumi.Input[str]] = None,
            certificate_id: Optional[pulumi.Input[str]] = None,
            gateway_name: Optional[pulumi.Input[str]] = None,
            host_name: Optional[pulumi.Input[str]] = None,
            http2_enabled: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            request_client_certificate_enabled: Optional[pulumi.Input[bool]] = None,
            tls10_enabled: Optional[pulumi.Input[bool]] = None,
            tls11_enabled: Optional[pulumi.Input[bool]] = None) -> 'GatewayHostNameConfiguration':
        """
        Get an existing GatewayHostNameConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_id: The ID of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] certificate_id: The certificate ID to be used for TLS connection establishment.
        :param pulumi.Input[str] gateway_name: The name of the API Management Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] host_name: The host name to use for the API Management Gateway Host Name Configuration.
        :param pulumi.Input[bool] http2_enabled: Whether HTTP/2.0 is supported.
        :param pulumi.Input[str] name: The name of the API Management Gateway Host Name Configuration. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] request_client_certificate_enabled: Whether the API Management Gateway requests a client certificate.
        :param pulumi.Input[bool] tls10_enabled: Whether TLS 1.0 is supported.
        :param pulumi.Input[bool] tls11_enabled: Whether TLS 1.1 is supported.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GatewayHostNameConfigurationState.__new__(_GatewayHostNameConfigurationState)

        __props__.__dict__["api_management_id"] = api_management_id
        __props__.__dict__["certificate_id"] = certificate_id
        __props__.__dict__["gateway_name"] = gateway_name
        __props__.__dict__["host_name"] = host_name
        __props__.__dict__["http2_enabled"] = http2_enabled
        __props__.__dict__["name"] = name
        __props__.__dict__["request_client_certificate_enabled"] = request_client_certificate_enabled
        __props__.__dict__["tls10_enabled"] = tls10_enabled
        __props__.__dict__["tls11_enabled"] = tls11_enabled
        return GatewayHostNameConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiManagementId")
    def api_management_id(self) -> pulumi.Output[str]:
        """
        The ID of the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_id")

    @property
    @pulumi.getter(name="certificateId")
    def certificate_id(self) -> pulumi.Output[str]:
        """
        The certificate ID to be used for TLS connection establishment.
        """
        return pulumi.get(self, "certificate_id")

    @property
    @pulumi.getter(name="gatewayName")
    def gateway_name(self) -> pulumi.Output[str]:
        """
        The name of the API Management Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "gateway_name")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        The host name to use for the API Management Gateway Host Name Configuration.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter(name="http2Enabled")
    def http2_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether HTTP/2.0 is supported.
        """
        return pulumi.get(self, "http2_enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the API Management Gateway Host Name Configuration. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requestClientCertificateEnabled")
    def request_client_certificate_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the API Management Gateway requests a client certificate.
        """
        return pulumi.get(self, "request_client_certificate_enabled")

    @property
    @pulumi.getter(name="tls10Enabled")
    def tls10_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether TLS 1.0 is supported.
        """
        return pulumi.get(self, "tls10_enabled")

    @property
    @pulumi.getter(name="tls11Enabled")
    def tls11_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether TLS 1.1 is supported.
        """
        return pulumi.get(self, "tls11_enabled")

