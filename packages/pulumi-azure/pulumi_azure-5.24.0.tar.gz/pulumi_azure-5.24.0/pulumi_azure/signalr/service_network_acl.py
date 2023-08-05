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
from ._inputs import *

__all__ = ['ServiceNetworkAclArgs', 'ServiceNetworkAcl']

@pulumi.input_type
class ServiceNetworkAclArgs:
    def __init__(__self__, *,
                 default_action: pulumi.Input[str],
                 public_network: pulumi.Input['ServiceNetworkAclPublicNetworkArgs'],
                 signalr_service_id: pulumi.Input[str],
                 private_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceNetworkAclPrivateEndpointArgs']]]] = None):
        """
        The set of arguments for constructing a ServiceNetworkAcl resource.
        :param pulumi.Input[str] default_action: The default action to control the network access when no other rule matches. Possible values are `Allow` and `Deny`.
        :param pulumi.Input['ServiceNetworkAclPublicNetworkArgs'] public_network: A `public_network` block as defined below.
        :param pulumi.Input[str] signalr_service_id: The ID of the SignalR service. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['ServiceNetworkAclPrivateEndpointArgs']]] private_endpoints: A `private_endpoint` block as defined below.
        """
        pulumi.set(__self__, "default_action", default_action)
        pulumi.set(__self__, "public_network", public_network)
        pulumi.set(__self__, "signalr_service_id", signalr_service_id)
        if private_endpoints is not None:
            pulumi.set(__self__, "private_endpoints", private_endpoints)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> pulumi.Input[str]:
        """
        The default action to control the network access when no other rule matches. Possible values are `Allow` and `Deny`.
        """
        return pulumi.get(self, "default_action")

    @default_action.setter
    def default_action(self, value: pulumi.Input[str]):
        pulumi.set(self, "default_action", value)

    @property
    @pulumi.getter(name="publicNetwork")
    def public_network(self) -> pulumi.Input['ServiceNetworkAclPublicNetworkArgs']:
        """
        A `public_network` block as defined below.
        """
        return pulumi.get(self, "public_network")

    @public_network.setter
    def public_network(self, value: pulumi.Input['ServiceNetworkAclPublicNetworkArgs']):
        pulumi.set(self, "public_network", value)

    @property
    @pulumi.getter(name="signalrServiceId")
    def signalr_service_id(self) -> pulumi.Input[str]:
        """
        The ID of the SignalR service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "signalr_service_id")

    @signalr_service_id.setter
    def signalr_service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "signalr_service_id", value)

    @property
    @pulumi.getter(name="privateEndpoints")
    def private_endpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceNetworkAclPrivateEndpointArgs']]]]:
        """
        A `private_endpoint` block as defined below.
        """
        return pulumi.get(self, "private_endpoints")

    @private_endpoints.setter
    def private_endpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceNetworkAclPrivateEndpointArgs']]]]):
        pulumi.set(self, "private_endpoints", value)


@pulumi.input_type
class _ServiceNetworkAclState:
    def __init__(__self__, *,
                 default_action: Optional[pulumi.Input[str]] = None,
                 private_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceNetworkAclPrivateEndpointArgs']]]] = None,
                 public_network: Optional[pulumi.Input['ServiceNetworkAclPublicNetworkArgs']] = None,
                 signalr_service_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceNetworkAcl resources.
        :param pulumi.Input[str] default_action: The default action to control the network access when no other rule matches. Possible values are `Allow` and `Deny`.
        :param pulumi.Input[Sequence[pulumi.Input['ServiceNetworkAclPrivateEndpointArgs']]] private_endpoints: A `private_endpoint` block as defined below.
        :param pulumi.Input['ServiceNetworkAclPublicNetworkArgs'] public_network: A `public_network` block as defined below.
        :param pulumi.Input[str] signalr_service_id: The ID of the SignalR service. Changing this forces a new resource to be created.
        """
        if default_action is not None:
            pulumi.set(__self__, "default_action", default_action)
        if private_endpoints is not None:
            pulumi.set(__self__, "private_endpoints", private_endpoints)
        if public_network is not None:
            pulumi.set(__self__, "public_network", public_network)
        if signalr_service_id is not None:
            pulumi.set(__self__, "signalr_service_id", signalr_service_id)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> Optional[pulumi.Input[str]]:
        """
        The default action to control the network access when no other rule matches. Possible values are `Allow` and `Deny`.
        """
        return pulumi.get(self, "default_action")

    @default_action.setter
    def default_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_action", value)

    @property
    @pulumi.getter(name="privateEndpoints")
    def private_endpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceNetworkAclPrivateEndpointArgs']]]]:
        """
        A `private_endpoint` block as defined below.
        """
        return pulumi.get(self, "private_endpoints")

    @private_endpoints.setter
    def private_endpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceNetworkAclPrivateEndpointArgs']]]]):
        pulumi.set(self, "private_endpoints", value)

    @property
    @pulumi.getter(name="publicNetwork")
    def public_network(self) -> Optional[pulumi.Input['ServiceNetworkAclPublicNetworkArgs']]:
        """
        A `public_network` block as defined below.
        """
        return pulumi.get(self, "public_network")

    @public_network.setter
    def public_network(self, value: Optional[pulumi.Input['ServiceNetworkAclPublicNetworkArgs']]):
        pulumi.set(self, "public_network", value)

    @property
    @pulumi.getter(name="signalrServiceId")
    def signalr_service_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the SignalR service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "signalr_service_id")

    @signalr_service_id.setter
    def signalr_service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "signalr_service_id", value)


class ServiceNetworkAcl(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 default_action: Optional[pulumi.Input[str]] = None,
                 private_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceNetworkAclPrivateEndpointArgs']]]]] = None,
                 public_network: Optional[pulumi.Input[pulumi.InputType['ServiceNetworkAclPublicNetworkArgs']]] = None,
                 signalr_service_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages the Network ACL for a SignalR service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.signalr.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku=azure.signalr.ServiceSkuArgs(
                name="Standard_S1",
                capacity=1,
            ))
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            address_spaces=["10.5.0.0/16"])
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.5.2.0/24"],
            enforce_private_link_endpoint_network_policies=True)
        example_endpoint = azure.privatelink.Endpoint("exampleEndpoint",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            subnet_id=example_subnet.id,
            private_service_connection=azure.privatelink.EndpointPrivateServiceConnectionArgs(
                name="psc-sig-test",
                is_manual_connection=False,
                private_connection_resource_id=example_service.id,
                subresource_names=["signalr"],
            ))
        example_service_network_acl = azure.signalr.ServiceNetworkAcl("exampleServiceNetworkAcl",
            signalr_service_id=example_service.id,
            default_action="Deny",
            public_network=azure.signalr.ServiceNetworkAclPublicNetworkArgs(
                allowed_request_types=["ClientConnection"],
            ),
            private_endpoints=[azure.signalr.ServiceNetworkAclPrivateEndpointArgs(
                id=example_endpoint.id,
                allowed_request_types=["ServerConnection"],
            )])
        ```

        ## Import

        Network ACLs for a SignalR service can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:signalr/serviceNetworkAcl:ServiceNetworkAcl example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.SignalRService/signalR/signalr1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_action: The default action to control the network access when no other rule matches. Possible values are `Allow` and `Deny`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceNetworkAclPrivateEndpointArgs']]]] private_endpoints: A `private_endpoint` block as defined below.
        :param pulumi.Input[pulumi.InputType['ServiceNetworkAclPublicNetworkArgs']] public_network: A `public_network` block as defined below.
        :param pulumi.Input[str] signalr_service_id: The ID of the SignalR service. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceNetworkAclArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the Network ACL for a SignalR service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.signalr.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku=azure.signalr.ServiceSkuArgs(
                name="Standard_S1",
                capacity=1,
            ))
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            address_spaces=["10.5.0.0/16"])
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.5.2.0/24"],
            enforce_private_link_endpoint_network_policies=True)
        example_endpoint = azure.privatelink.Endpoint("exampleEndpoint",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            subnet_id=example_subnet.id,
            private_service_connection=azure.privatelink.EndpointPrivateServiceConnectionArgs(
                name="psc-sig-test",
                is_manual_connection=False,
                private_connection_resource_id=example_service.id,
                subresource_names=["signalr"],
            ))
        example_service_network_acl = azure.signalr.ServiceNetworkAcl("exampleServiceNetworkAcl",
            signalr_service_id=example_service.id,
            default_action="Deny",
            public_network=azure.signalr.ServiceNetworkAclPublicNetworkArgs(
                allowed_request_types=["ClientConnection"],
            ),
            private_endpoints=[azure.signalr.ServiceNetworkAclPrivateEndpointArgs(
                id=example_endpoint.id,
                allowed_request_types=["ServerConnection"],
            )])
        ```

        ## Import

        Network ACLs for a SignalR service can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:signalr/serviceNetworkAcl:ServiceNetworkAcl example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.SignalRService/signalR/signalr1
        ```

        :param str resource_name: The name of the resource.
        :param ServiceNetworkAclArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceNetworkAclArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 default_action: Optional[pulumi.Input[str]] = None,
                 private_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceNetworkAclPrivateEndpointArgs']]]]] = None,
                 public_network: Optional[pulumi.Input[pulumi.InputType['ServiceNetworkAclPublicNetworkArgs']]] = None,
                 signalr_service_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceNetworkAclArgs.__new__(ServiceNetworkAclArgs)

            if default_action is None and not opts.urn:
                raise TypeError("Missing required property 'default_action'")
            __props__.__dict__["default_action"] = default_action
            __props__.__dict__["private_endpoints"] = private_endpoints
            if public_network is None and not opts.urn:
                raise TypeError("Missing required property 'public_network'")
            __props__.__dict__["public_network"] = public_network
            if signalr_service_id is None and not opts.urn:
                raise TypeError("Missing required property 'signalr_service_id'")
            __props__.__dict__["signalr_service_id"] = signalr_service_id
        super(ServiceNetworkAcl, __self__).__init__(
            'azure:signalr/serviceNetworkAcl:ServiceNetworkAcl',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            default_action: Optional[pulumi.Input[str]] = None,
            private_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceNetworkAclPrivateEndpointArgs']]]]] = None,
            public_network: Optional[pulumi.Input[pulumi.InputType['ServiceNetworkAclPublicNetworkArgs']]] = None,
            signalr_service_id: Optional[pulumi.Input[str]] = None) -> 'ServiceNetworkAcl':
        """
        Get an existing ServiceNetworkAcl resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_action: The default action to control the network access when no other rule matches. Possible values are `Allow` and `Deny`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceNetworkAclPrivateEndpointArgs']]]] private_endpoints: A `private_endpoint` block as defined below.
        :param pulumi.Input[pulumi.InputType['ServiceNetworkAclPublicNetworkArgs']] public_network: A `public_network` block as defined below.
        :param pulumi.Input[str] signalr_service_id: The ID of the SignalR service. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceNetworkAclState.__new__(_ServiceNetworkAclState)

        __props__.__dict__["default_action"] = default_action
        __props__.__dict__["private_endpoints"] = private_endpoints
        __props__.__dict__["public_network"] = public_network
        __props__.__dict__["signalr_service_id"] = signalr_service_id
        return ServiceNetworkAcl(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> pulumi.Output[str]:
        """
        The default action to control the network access when no other rule matches. Possible values are `Allow` and `Deny`.
        """
        return pulumi.get(self, "default_action")

    @property
    @pulumi.getter(name="privateEndpoints")
    def private_endpoints(self) -> pulumi.Output[Optional[Sequence['outputs.ServiceNetworkAclPrivateEndpoint']]]:
        """
        A `private_endpoint` block as defined below.
        """
        return pulumi.get(self, "private_endpoints")

    @property
    @pulumi.getter(name="publicNetwork")
    def public_network(self) -> pulumi.Output['outputs.ServiceNetworkAclPublicNetwork']:
        """
        A `public_network` block as defined below.
        """
        return pulumi.get(self, "public_network")

    @property
    @pulumi.getter(name="signalrServiceId")
    def signalr_service_id(self) -> pulumi.Output[str]:
        """
        The ID of the SignalR service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "signalr_service_id")

