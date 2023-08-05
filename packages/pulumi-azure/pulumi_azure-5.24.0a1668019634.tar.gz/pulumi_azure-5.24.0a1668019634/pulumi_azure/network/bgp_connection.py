# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BgpConnectionArgs', 'BgpConnection']

@pulumi.input_type
class BgpConnectionArgs:
    def __init__(__self__, *,
                 peer_asn: pulumi.Input[int],
                 peer_ip: pulumi.Input[str],
                 virtual_hub_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 virtual_network_connection_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BgpConnection resource.
        :param pulumi.Input[int] peer_asn: The peer autonomous system number for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] peer_ip: The peer IP address for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub within which this Bgp connection should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for this Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_network_connection_id: The ID of virtual network connection.
        """
        pulumi.set(__self__, "peer_asn", peer_asn)
        pulumi.set(__self__, "peer_ip", peer_ip)
        pulumi.set(__self__, "virtual_hub_id", virtual_hub_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if virtual_network_connection_id is not None:
            pulumi.set(__self__, "virtual_network_connection_id", virtual_network_connection_id)

    @property
    @pulumi.getter(name="peerAsn")
    def peer_asn(self) -> pulumi.Input[int]:
        """
        The peer autonomous system number for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "peer_asn")

    @peer_asn.setter
    def peer_asn(self, value: pulumi.Input[int]):
        pulumi.set(self, "peer_asn", value)

    @property
    @pulumi.getter(name="peerIp")
    def peer_ip(self) -> pulumi.Input[str]:
        """
        The peer IP address for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "peer_ip")

    @peer_ip.setter
    def peer_ip(self, value: pulumi.Input[str]):
        pulumi.set(self, "peer_ip", value)

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> pulumi.Input[str]:
        """
        The ID of the Virtual Hub within which this Bgp connection should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_hub_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="virtualNetworkConnectionId")
    def virtual_network_connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of virtual network connection.
        """
        return pulumi.get(self, "virtual_network_connection_id")

    @virtual_network_connection_id.setter
    def virtual_network_connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_network_connection_id", value)


@pulumi.input_type
class _BgpConnectionState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 peer_asn: Optional[pulumi.Input[int]] = None,
                 peer_ip: Optional[pulumi.Input[str]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 virtual_network_connection_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BgpConnection resources.
        :param pulumi.Input[str] name: The name which should be used for this Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[int] peer_asn: The peer autonomous system number for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] peer_ip: The peer IP address for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub within which this Bgp connection should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_network_connection_id: The ID of virtual network connection.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if peer_asn is not None:
            pulumi.set(__self__, "peer_asn", peer_asn)
        if peer_ip is not None:
            pulumi.set(__self__, "peer_ip", peer_ip)
        if virtual_hub_id is not None:
            pulumi.set(__self__, "virtual_hub_id", virtual_hub_id)
        if virtual_network_connection_id is not None:
            pulumi.set(__self__, "virtual_network_connection_id", virtual_network_connection_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="peerAsn")
    def peer_asn(self) -> Optional[pulumi.Input[int]]:
        """
        The peer autonomous system number for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "peer_asn")

    @peer_asn.setter
    def peer_asn(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "peer_asn", value)

    @property
    @pulumi.getter(name="peerIp")
    def peer_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The peer IP address for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "peer_ip")

    @peer_ip.setter
    def peer_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peer_ip", value)

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Virtual Hub within which this Bgp connection should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_hub_id", value)

    @property
    @pulumi.getter(name="virtualNetworkConnectionId")
    def virtual_network_connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of virtual network connection.
        """
        return pulumi.get(self, "virtual_network_connection_id")

    @virtual_network_connection_id.setter
    def virtual_network_connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_network_connection_id", value)


class BgpConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 peer_asn: Optional[pulumi.Input[int]] = None,
                 peer_ip: Optional[pulumi.Input[str]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 virtual_network_connection_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Bgp Connection for a Virtual Hub.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_hub = azure.network.VirtualHub("exampleVirtualHub",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            sku="Standard")
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            allocation_method="Static",
            sku="Standard")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.5.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.5.1.0/24"])
        example_virtual_hub_ip = azure.network.VirtualHubIp("exampleVirtualHubIp",
            virtual_hub_id=example_virtual_hub.id,
            private_ip_address="10.5.1.18",
            private_ip_allocation_method="Static",
            public_ip_address_id=example_public_ip.id,
            subnet_id=example_subnet.id)
        example_bgp_connection = azure.network.BgpConnection("exampleBgpConnection",
            virtual_hub_id=example_virtual_hub.id,
            peer_asn=65514,
            peer_ip="169.254.21.5",
            opts=pulumi.ResourceOptions(depends_on=[example_virtual_hub_ip]))
        ```

        ## Import

        Virtual Hub Bgp Connections can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/bgpConnection:BgpConnection example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/virtualHubs/virtualHub1/bgpConnections/connection1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name which should be used for this Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[int] peer_asn: The peer autonomous system number for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] peer_ip: The peer IP address for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub within which this Bgp connection should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_network_connection_id: The ID of virtual network connection.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BgpConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Bgp Connection for a Virtual Hub.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_hub = azure.network.VirtualHub("exampleVirtualHub",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            sku="Standard")
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            allocation_method="Static",
            sku="Standard")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.5.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.5.1.0/24"])
        example_virtual_hub_ip = azure.network.VirtualHubIp("exampleVirtualHubIp",
            virtual_hub_id=example_virtual_hub.id,
            private_ip_address="10.5.1.18",
            private_ip_allocation_method="Static",
            public_ip_address_id=example_public_ip.id,
            subnet_id=example_subnet.id)
        example_bgp_connection = azure.network.BgpConnection("exampleBgpConnection",
            virtual_hub_id=example_virtual_hub.id,
            peer_asn=65514,
            peer_ip="169.254.21.5",
            opts=pulumi.ResourceOptions(depends_on=[example_virtual_hub_ip]))
        ```

        ## Import

        Virtual Hub Bgp Connections can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/bgpConnection:BgpConnection example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/virtualHubs/virtualHub1/bgpConnections/connection1
        ```

        :param str resource_name: The name of the resource.
        :param BgpConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BgpConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 peer_asn: Optional[pulumi.Input[int]] = None,
                 peer_ip: Optional[pulumi.Input[str]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 virtual_network_connection_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BgpConnectionArgs.__new__(BgpConnectionArgs)

            __props__.__dict__["name"] = name
            if peer_asn is None and not opts.urn:
                raise TypeError("Missing required property 'peer_asn'")
            __props__.__dict__["peer_asn"] = peer_asn
            if peer_ip is None and not opts.urn:
                raise TypeError("Missing required property 'peer_ip'")
            __props__.__dict__["peer_ip"] = peer_ip
            if virtual_hub_id is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_id'")
            __props__.__dict__["virtual_hub_id"] = virtual_hub_id
            __props__.__dict__["virtual_network_connection_id"] = virtual_network_connection_id
        super(BgpConnection, __self__).__init__(
            'azure:network/bgpConnection:BgpConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            peer_asn: Optional[pulumi.Input[int]] = None,
            peer_ip: Optional[pulumi.Input[str]] = None,
            virtual_hub_id: Optional[pulumi.Input[str]] = None,
            virtual_network_connection_id: Optional[pulumi.Input[str]] = None) -> 'BgpConnection':
        """
        Get an existing BgpConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name which should be used for this Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[int] peer_asn: The peer autonomous system number for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] peer_ip: The peer IP address for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub within which this Bgp connection should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_network_connection_id: The ID of virtual network connection.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BgpConnectionState.__new__(_BgpConnectionState)

        __props__.__dict__["name"] = name
        __props__.__dict__["peer_asn"] = peer_asn
        __props__.__dict__["peer_ip"] = peer_ip
        __props__.__dict__["virtual_hub_id"] = virtual_hub_id
        __props__.__dict__["virtual_network_connection_id"] = virtual_network_connection_id
        return BgpConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="peerAsn")
    def peer_asn(self) -> pulumi.Output[int]:
        """
        The peer autonomous system number for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "peer_asn")

    @property
    @pulumi.getter(name="peerIp")
    def peer_ip(self) -> pulumi.Output[str]:
        """
        The peer IP address for the Virtual Hub Bgp Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "peer_ip")

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> pulumi.Output[str]:
        """
        The ID of the Virtual Hub within which this Bgp connection should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @property
    @pulumi.getter(name="virtualNetworkConnectionId")
    def virtual_network_connection_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of virtual network connection.
        """
        return pulumi.get(self, "virtual_network_connection_id")

