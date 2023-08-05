# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NetworkInterfaceApplicationSecurityGroupAssociationArgs', 'NetworkInterfaceApplicationSecurityGroupAssociation']

@pulumi.input_type
class NetworkInterfaceApplicationSecurityGroupAssociationArgs:
    def __init__(__self__, *,
                 application_security_group_id: pulumi.Input[str],
                 network_interface_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a NetworkInterfaceApplicationSecurityGroupAssociation resource.
        :param pulumi.Input[str] application_security_group_id: The ID of the Application Security Group which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_interface_id: The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "application_security_group_id", application_security_group_id)
        pulumi.set(__self__, "network_interface_id", network_interface_id)

    @property
    @pulumi.getter(name="applicationSecurityGroupId")
    def application_security_group_id(self) -> pulumi.Input[str]:
        """
        The ID of the Application Security Group which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "application_security_group_id")

    @application_security_group_id.setter
    def application_security_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_security_group_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Input[str]:
        """
        The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_interface_id", value)


@pulumi.input_type
class _NetworkInterfaceApplicationSecurityGroupAssociationState:
    def __init__(__self__, *,
                 application_security_group_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NetworkInterfaceApplicationSecurityGroupAssociation resources.
        :param pulumi.Input[str] application_security_group_id: The ID of the Application Security Group which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_interface_id: The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        if application_security_group_id is not None:
            pulumi.set(__self__, "application_security_group_id", application_security_group_id)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)

    @property
    @pulumi.getter(name="applicationSecurityGroupId")
    def application_security_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Application Security Group which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "application_security_group_id")

    @application_security_group_id.setter
    def application_security_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_security_group_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_interface_id", value)


class NetworkInterfaceApplicationSecurityGroupAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_security_group_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages the association between a Network Interface and a Application Security Group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.0.1.0/24"])
        example_application_security_group = azure.network.ApplicationSecurityGroup("exampleApplicationSecurityGroup",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
                name="testconfiguration1",
                subnet_id=example_subnet.id,
                private_ip_address_allocation="Dynamic",
            )])
        example_network_interface_application_security_group_association = azure.network.NetworkInterfaceApplicationSecurityGroupAssociation("exampleNetworkInterfaceApplicationSecurityGroupAssociation",
            network_interface_id=example_network_interface.id,
            application_security_group_id=example_application_security_group.id)
        ```

        ## Import

        Associations between Network Interfaces and Application Security Groups can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/networkInterfaceApplicationSecurityGroupAssociation:NetworkInterfaceApplicationSecurityGroupAssociation association1 "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/microsoft.network/networkInterfaces/nic1|/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/applicationSecurityGroups/securityGroup1"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_security_group_id: The ID of the Application Security Group which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_interface_id: The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkInterfaceApplicationSecurityGroupAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the association between a Network Interface and a Application Security Group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.0.1.0/24"])
        example_application_security_group = azure.network.ApplicationSecurityGroup("exampleApplicationSecurityGroup",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
                name="testconfiguration1",
                subnet_id=example_subnet.id,
                private_ip_address_allocation="Dynamic",
            )])
        example_network_interface_application_security_group_association = azure.network.NetworkInterfaceApplicationSecurityGroupAssociation("exampleNetworkInterfaceApplicationSecurityGroupAssociation",
            network_interface_id=example_network_interface.id,
            application_security_group_id=example_application_security_group.id)
        ```

        ## Import

        Associations between Network Interfaces and Application Security Groups can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/networkInterfaceApplicationSecurityGroupAssociation:NetworkInterfaceApplicationSecurityGroupAssociation association1 "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/microsoft.network/networkInterfaces/nic1|/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/applicationSecurityGroups/securityGroup1"
        ```

        :param str resource_name: The name of the resource.
        :param NetworkInterfaceApplicationSecurityGroupAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkInterfaceApplicationSecurityGroupAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_security_group_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkInterfaceApplicationSecurityGroupAssociationArgs.__new__(NetworkInterfaceApplicationSecurityGroupAssociationArgs)

            if application_security_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'application_security_group_id'")
            __props__.__dict__["application_security_group_id"] = application_security_group_id
            if network_interface_id is None and not opts.urn:
                raise TypeError("Missing required property 'network_interface_id'")
            __props__.__dict__["network_interface_id"] = network_interface_id
        super(NetworkInterfaceApplicationSecurityGroupAssociation, __self__).__init__(
            'azure:network/networkInterfaceApplicationSecurityGroupAssociation:NetworkInterfaceApplicationSecurityGroupAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            application_security_group_id: Optional[pulumi.Input[str]] = None,
            network_interface_id: Optional[pulumi.Input[str]] = None) -> 'NetworkInterfaceApplicationSecurityGroupAssociation':
        """
        Get an existing NetworkInterfaceApplicationSecurityGroupAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_security_group_id: The ID of the Application Security Group which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_interface_id: The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkInterfaceApplicationSecurityGroupAssociationState.__new__(_NetworkInterfaceApplicationSecurityGroupAssociationState)

        __props__.__dict__["application_security_group_id"] = application_security_group_id
        __props__.__dict__["network_interface_id"] = network_interface_id
        return NetworkInterfaceApplicationSecurityGroupAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationSecurityGroupId")
    def application_security_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the Application Security Group which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "application_security_group_id")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Output[str]:
        """
        The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "network_interface_id")

