# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NatGatewayPublicIpPrefixAssociationArgs', 'NatGatewayPublicIpPrefixAssociation']

@pulumi.input_type
class NatGatewayPublicIpPrefixAssociationArgs:
    def __init__(__self__, *,
                 nat_gateway_id: pulumi.Input[str],
                 public_ip_prefix_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a NatGatewayPublicIpPrefixAssociation resource.
        :param pulumi.Input[str] nat_gateway_id: The ID of the NAT Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] public_ip_prefix_id: The ID of the Public IP Prefix which this NAT Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "nat_gateway_id", nat_gateway_id)
        pulumi.set(__self__, "public_ip_prefix_id", public_ip_prefix_id)

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> pulumi.Input[str]:
        """
        The ID of the NAT Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "nat_gateway_id")

    @nat_gateway_id.setter
    def nat_gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "nat_gateway_id", value)

    @property
    @pulumi.getter(name="publicIpPrefixId")
    def public_ip_prefix_id(self) -> pulumi.Input[str]:
        """
        The ID of the Public IP Prefix which this NAT Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "public_ip_prefix_id")

    @public_ip_prefix_id.setter
    def public_ip_prefix_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "public_ip_prefix_id", value)


@pulumi.input_type
class _NatGatewayPublicIpPrefixAssociationState:
    def __init__(__self__, *,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 public_ip_prefix_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NatGatewayPublicIpPrefixAssociation resources.
        :param pulumi.Input[str] nat_gateway_id: The ID of the NAT Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] public_ip_prefix_id: The ID of the Public IP Prefix which this NAT Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        if nat_gateway_id is not None:
            pulumi.set(__self__, "nat_gateway_id", nat_gateway_id)
        if public_ip_prefix_id is not None:
            pulumi.set(__self__, "public_ip_prefix_id", public_ip_prefix_id)

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the NAT Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "nat_gateway_id")

    @nat_gateway_id.setter
    def nat_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nat_gateway_id", value)

    @property
    @pulumi.getter(name="publicIpPrefixId")
    def public_ip_prefix_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Public IP Prefix which this NAT Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "public_ip_prefix_id")

    @public_ip_prefix_id.setter
    def public_ip_prefix_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_ip_prefix_id", value)


class NatGatewayPublicIpPrefixAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 public_ip_prefix_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages the association between a NAT Gateway and a Public IP Prefix.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_public_ip_prefix = azure.network.PublicIpPrefix("examplePublicIpPrefix",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            prefix_length=30,
            zones=["1"])
        example_nat_gateway = azure.network.NatGateway("exampleNatGateway",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Standard")
        example_nat_gateway_public_ip_prefix_association = azure.network.NatGatewayPublicIpPrefixAssociation("exampleNatGatewayPublicIpPrefixAssociation",
            nat_gateway_id=example_nat_gateway.id,
            public_ip_prefix_id=example_public_ip_prefix.id)
        ```

        ## Import

        Associations between NAT Gateway and Public IP Prefixes can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/natGatewayPublicIpPrefixAssociation:NatGatewayPublicIpPrefixAssociation example "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/natGateways/gateway1|/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Network/publicIPPrefixes/myPublicIpPrefix1"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] nat_gateway_id: The ID of the NAT Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] public_ip_prefix_id: The ID of the Public IP Prefix which this NAT Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NatGatewayPublicIpPrefixAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the association between a NAT Gateway and a Public IP Prefix.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_public_ip_prefix = azure.network.PublicIpPrefix("examplePublicIpPrefix",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            prefix_length=30,
            zones=["1"])
        example_nat_gateway = azure.network.NatGateway("exampleNatGateway",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Standard")
        example_nat_gateway_public_ip_prefix_association = azure.network.NatGatewayPublicIpPrefixAssociation("exampleNatGatewayPublicIpPrefixAssociation",
            nat_gateway_id=example_nat_gateway.id,
            public_ip_prefix_id=example_public_ip_prefix.id)
        ```

        ## Import

        Associations between NAT Gateway and Public IP Prefixes can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/natGatewayPublicIpPrefixAssociation:NatGatewayPublicIpPrefixAssociation example "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/natGateways/gateway1|/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Network/publicIPPrefixes/myPublicIpPrefix1"
        ```

        :param str resource_name: The name of the resource.
        :param NatGatewayPublicIpPrefixAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NatGatewayPublicIpPrefixAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 public_ip_prefix_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NatGatewayPublicIpPrefixAssociationArgs.__new__(NatGatewayPublicIpPrefixAssociationArgs)

            if nat_gateway_id is None and not opts.urn:
                raise TypeError("Missing required property 'nat_gateway_id'")
            __props__.__dict__["nat_gateway_id"] = nat_gateway_id
            if public_ip_prefix_id is None and not opts.urn:
                raise TypeError("Missing required property 'public_ip_prefix_id'")
            __props__.__dict__["public_ip_prefix_id"] = public_ip_prefix_id
        super(NatGatewayPublicIpPrefixAssociation, __self__).__init__(
            'azure:network/natGatewayPublicIpPrefixAssociation:NatGatewayPublicIpPrefixAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            nat_gateway_id: Optional[pulumi.Input[str]] = None,
            public_ip_prefix_id: Optional[pulumi.Input[str]] = None) -> 'NatGatewayPublicIpPrefixAssociation':
        """
        Get an existing NatGatewayPublicIpPrefixAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] nat_gateway_id: The ID of the NAT Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] public_ip_prefix_id: The ID of the Public IP Prefix which this NAT Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NatGatewayPublicIpPrefixAssociationState.__new__(_NatGatewayPublicIpPrefixAssociationState)

        __props__.__dict__["nat_gateway_id"] = nat_gateway_id
        __props__.__dict__["public_ip_prefix_id"] = public_ip_prefix_id
        return NatGatewayPublicIpPrefixAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> pulumi.Output[str]:
        """
        The ID of the NAT Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "nat_gateway_id")

    @property
    @pulumi.getter(name="publicIpPrefixId")
    def public_ip_prefix_id(self) -> pulumi.Output[str]:
        """
        The ID of the Public IP Prefix which this NAT Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "public_ip_prefix_id")

