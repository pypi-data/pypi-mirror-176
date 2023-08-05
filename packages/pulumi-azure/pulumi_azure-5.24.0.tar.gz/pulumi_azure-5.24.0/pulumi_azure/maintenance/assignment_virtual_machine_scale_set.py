# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AssignmentVirtualMachineScaleSetArgs', 'AssignmentVirtualMachineScaleSet']

@pulumi.input_type
class AssignmentVirtualMachineScaleSetArgs:
    def __init__(__self__, *,
                 maintenance_configuration_id: pulumi.Input[str],
                 virtual_machine_scale_set_id: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AssignmentVirtualMachineScaleSet resource.
        :param pulumi.Input[str] maintenance_configuration_id: Specifies the ID of the Maintenance Configuration Resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_machine_scale_set_id: Specifies the Virtual Machine Scale Set ID to which the Maintenance Configuration will be assigned. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "maintenance_configuration_id", maintenance_configuration_id)
        pulumi.set(__self__, "virtual_machine_scale_set_id", virtual_machine_scale_set_id)
        if location is not None:
            pulumi.set(__self__, "location", location)

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the Maintenance Configuration Resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @maintenance_configuration_id.setter
    def maintenance_configuration_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "maintenance_configuration_id", value)

    @property
    @pulumi.getter(name="virtualMachineScaleSetId")
    def virtual_machine_scale_set_id(self) -> pulumi.Input[str]:
        """
        Specifies the Virtual Machine Scale Set ID to which the Maintenance Configuration will be assigned. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_machine_scale_set_id")

    @virtual_machine_scale_set_id.setter
    def virtual_machine_scale_set_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_machine_scale_set_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)


@pulumi.input_type
class _AssignmentVirtualMachineScaleSetState:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 virtual_machine_scale_set_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AssignmentVirtualMachineScaleSet resources.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] maintenance_configuration_id: Specifies the ID of the Maintenance Configuration Resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_machine_scale_set_id: Specifies the Virtual Machine Scale Set ID to which the Maintenance Configuration will be assigned. Changing this forces a new resource to be created.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maintenance_configuration_id is not None:
            pulumi.set(__self__, "maintenance_configuration_id", maintenance_configuration_id)
        if virtual_machine_scale_set_id is not None:
            pulumi.set(__self__, "virtual_machine_scale_set_id", virtual_machine_scale_set_id)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the Maintenance Configuration Resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @maintenance_configuration_id.setter
    def maintenance_configuration_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "maintenance_configuration_id", value)

    @property
    @pulumi.getter(name="virtualMachineScaleSetId")
    def virtual_machine_scale_set_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Virtual Machine Scale Set ID to which the Maintenance Configuration will be assigned. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_machine_scale_set_id")

    @virtual_machine_scale_set_id.setter
    def virtual_machine_scale_set_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_machine_scale_set_id", value)


class AssignmentVirtualMachineScaleSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 virtual_machine_scale_set_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a maintenance assignment to a virtual machine scale set.

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
            address_prefixes=["10.0.2.0/24"])
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            allocation_method="Static")
        example_load_balancer = azure.lb.LoadBalancer("exampleLoadBalancer",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            frontend_ip_configurations=[azure.lb.LoadBalancerFrontendIpConfigurationArgs(
                name="internal",
                public_ip_address_id=example_public_ip.id,
            )])
        example_backend_address_pool = azure.lb.BackendAddressPool("exampleBackendAddressPool", loadbalancer_id=example_load_balancer.id)
        example_probe = azure.lb.Probe("exampleProbe",
            loadbalancer_id=example_load_balancer.id,
            port=22,
            protocol="Tcp")
        example_rule = azure.lb.Rule("exampleRule",
            loadbalancer_id=example_load_balancer.id,
            probe_id=example_probe.id,
            frontend_ip_configuration_name="internal",
            protocol="Tcp",
            frontend_port=22,
            backend_port=22)
        example_configuration = azure.maintenance.Configuration("exampleConfiguration",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            scope="OSImage",
            visibility="Custom",
            window=azure.maintenance.ConfigurationWindowArgs(
                start_date_time="2021-12-31 00:00",
                expiration_date_time="9999-12-31 00:00",
                duration="06:00",
                time_zone="Pacific Standard Time",
                recur_every="1Days",
            ))
        example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
                name="testconfiguration1",
                private_ip_address_allocation="Dynamic",
            )])
        example_linux_virtual_machine = azure.compute.LinuxVirtualMachine("exampleLinuxVirtualMachine",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            size="Standard_F2",
            admin_username="adminuser",
            network_interface_ids=[example_network_interface.id],
            os_disk=azure.compute.LinuxVirtualMachineOsDiskArgs(
                caching="ReadWrite",
                storage_account_type="Standard_LRS",
            ))
        example_linux_virtual_machine_scale_set = azure.compute.LinuxVirtualMachineScaleSet("exampleLinuxVirtualMachineScaleSet",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            sku="Standard_F2",
            instances=1,
            admin_username="adminuser",
            admin_password="P@ssword1234!",
            upgrade_mode="Automatic",
            health_probe_id=example_probe.id,
            disable_password_authentication=False,
            source_image_reference=azure.compute.LinuxVirtualMachineScaleSetSourceImageReferenceArgs(
                publisher="Canonical",
                offer="UbuntuServer",
                sku="16.04-LTS",
                version="latest",
            ),
            os_disk=azure.compute.LinuxVirtualMachineScaleSetOsDiskArgs(
                storage_account_type="Standard_LRS",
                caching="ReadWrite",
            ),
            network_interfaces=[azure.compute.LinuxVirtualMachineScaleSetNetworkInterfaceArgs(
                name="example",
                primary=True,
                ip_configurations=[azure.compute.LinuxVirtualMachineScaleSetNetworkInterfaceIpConfigurationArgs(
                    name="internal",
                    primary=True,
                    subnet_id=example_subnet.id,
                    load_balancer_backend_address_pool_ids=[example_backend_address_pool.id],
                )],
            )],
            automatic_os_upgrade_policy=azure.compute.LinuxVirtualMachineScaleSetAutomaticOsUpgradePolicyArgs(
                disable_automatic_rollback=True,
                enable_automatic_os_upgrade=True,
            ),
            rolling_upgrade_policy=azure.compute.LinuxVirtualMachineScaleSetRollingUpgradePolicyArgs(
                max_batch_instance_percent=20,
                max_unhealthy_instance_percent=20,
                max_unhealthy_upgraded_instance_percent=20,
                pause_time_between_batches="PT0S",
            ),
            opts=pulumi.ResourceOptions(depends_on=["azurerm_lb_rule.example"]))
        example_assignment_virtual_machine_scale_set = azure.maintenance.AssignmentVirtualMachineScaleSet("exampleAssignmentVirtualMachineScaleSet",
            location=example_resource_group.location,
            maintenance_configuration_id=example_configuration.id,
            virtual_machine_scale_set_id=example_linux_virtual_machine.id)
        ```

        ## Import

        Maintenance Assignment can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:maintenance/assignmentVirtualMachineScaleSet:AssignmentVirtualMachineScaleSet example /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/resGroup1/providers/microsoft.compute/virtualMachineScaleSets/vmss1/providers/Microsoft.Maintenance/configurationAssignments/assign1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] maintenance_configuration_id: Specifies the ID of the Maintenance Configuration Resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_machine_scale_set_id: Specifies the Virtual Machine Scale Set ID to which the Maintenance Configuration will be assigned. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AssignmentVirtualMachineScaleSetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a maintenance assignment to a virtual machine scale set.

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
            address_prefixes=["10.0.2.0/24"])
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            allocation_method="Static")
        example_load_balancer = azure.lb.LoadBalancer("exampleLoadBalancer",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            frontend_ip_configurations=[azure.lb.LoadBalancerFrontendIpConfigurationArgs(
                name="internal",
                public_ip_address_id=example_public_ip.id,
            )])
        example_backend_address_pool = azure.lb.BackendAddressPool("exampleBackendAddressPool", loadbalancer_id=example_load_balancer.id)
        example_probe = azure.lb.Probe("exampleProbe",
            loadbalancer_id=example_load_balancer.id,
            port=22,
            protocol="Tcp")
        example_rule = azure.lb.Rule("exampleRule",
            loadbalancer_id=example_load_balancer.id,
            probe_id=example_probe.id,
            frontend_ip_configuration_name="internal",
            protocol="Tcp",
            frontend_port=22,
            backend_port=22)
        example_configuration = azure.maintenance.Configuration("exampleConfiguration",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            scope="OSImage",
            visibility="Custom",
            window=azure.maintenance.ConfigurationWindowArgs(
                start_date_time="2021-12-31 00:00",
                expiration_date_time="9999-12-31 00:00",
                duration="06:00",
                time_zone="Pacific Standard Time",
                recur_every="1Days",
            ))
        example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
                name="testconfiguration1",
                private_ip_address_allocation="Dynamic",
            )])
        example_linux_virtual_machine = azure.compute.LinuxVirtualMachine("exampleLinuxVirtualMachine",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            size="Standard_F2",
            admin_username="adminuser",
            network_interface_ids=[example_network_interface.id],
            os_disk=azure.compute.LinuxVirtualMachineOsDiskArgs(
                caching="ReadWrite",
                storage_account_type="Standard_LRS",
            ))
        example_linux_virtual_machine_scale_set = azure.compute.LinuxVirtualMachineScaleSet("exampleLinuxVirtualMachineScaleSet",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            sku="Standard_F2",
            instances=1,
            admin_username="adminuser",
            admin_password="P@ssword1234!",
            upgrade_mode="Automatic",
            health_probe_id=example_probe.id,
            disable_password_authentication=False,
            source_image_reference=azure.compute.LinuxVirtualMachineScaleSetSourceImageReferenceArgs(
                publisher="Canonical",
                offer="UbuntuServer",
                sku="16.04-LTS",
                version="latest",
            ),
            os_disk=azure.compute.LinuxVirtualMachineScaleSetOsDiskArgs(
                storage_account_type="Standard_LRS",
                caching="ReadWrite",
            ),
            network_interfaces=[azure.compute.LinuxVirtualMachineScaleSetNetworkInterfaceArgs(
                name="example",
                primary=True,
                ip_configurations=[azure.compute.LinuxVirtualMachineScaleSetNetworkInterfaceIpConfigurationArgs(
                    name="internal",
                    primary=True,
                    subnet_id=example_subnet.id,
                    load_balancer_backend_address_pool_ids=[example_backend_address_pool.id],
                )],
            )],
            automatic_os_upgrade_policy=azure.compute.LinuxVirtualMachineScaleSetAutomaticOsUpgradePolicyArgs(
                disable_automatic_rollback=True,
                enable_automatic_os_upgrade=True,
            ),
            rolling_upgrade_policy=azure.compute.LinuxVirtualMachineScaleSetRollingUpgradePolicyArgs(
                max_batch_instance_percent=20,
                max_unhealthy_instance_percent=20,
                max_unhealthy_upgraded_instance_percent=20,
                pause_time_between_batches="PT0S",
            ),
            opts=pulumi.ResourceOptions(depends_on=["azurerm_lb_rule.example"]))
        example_assignment_virtual_machine_scale_set = azure.maintenance.AssignmentVirtualMachineScaleSet("exampleAssignmentVirtualMachineScaleSet",
            location=example_resource_group.location,
            maintenance_configuration_id=example_configuration.id,
            virtual_machine_scale_set_id=example_linux_virtual_machine.id)
        ```

        ## Import

        Maintenance Assignment can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:maintenance/assignmentVirtualMachineScaleSet:AssignmentVirtualMachineScaleSet example /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/resGroup1/providers/microsoft.compute/virtualMachineScaleSets/vmss1/providers/Microsoft.Maintenance/configurationAssignments/assign1
        ```

        :param str resource_name: The name of the resource.
        :param AssignmentVirtualMachineScaleSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AssignmentVirtualMachineScaleSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 virtual_machine_scale_set_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AssignmentVirtualMachineScaleSetArgs.__new__(AssignmentVirtualMachineScaleSetArgs)

            __props__.__dict__["location"] = location
            if maintenance_configuration_id is None and not opts.urn:
                raise TypeError("Missing required property 'maintenance_configuration_id'")
            __props__.__dict__["maintenance_configuration_id"] = maintenance_configuration_id
            if virtual_machine_scale_set_id is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_machine_scale_set_id'")
            __props__.__dict__["virtual_machine_scale_set_id"] = virtual_machine_scale_set_id
        super(AssignmentVirtualMachineScaleSet, __self__).__init__(
            'azure:maintenance/assignmentVirtualMachineScaleSet:AssignmentVirtualMachineScaleSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            location: Optional[pulumi.Input[str]] = None,
            maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
            virtual_machine_scale_set_id: Optional[pulumi.Input[str]] = None) -> 'AssignmentVirtualMachineScaleSet':
        """
        Get an existing AssignmentVirtualMachineScaleSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] maintenance_configuration_id: Specifies the ID of the Maintenance Configuration Resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_machine_scale_set_id: Specifies the Virtual Machine Scale Set ID to which the Maintenance Configuration will be assigned. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AssignmentVirtualMachineScaleSetState.__new__(_AssignmentVirtualMachineScaleSetState)

        __props__.__dict__["location"] = location
        __props__.__dict__["maintenance_configuration_id"] = maintenance_configuration_id
        __props__.__dict__["virtual_machine_scale_set_id"] = virtual_machine_scale_set_id
        return AssignmentVirtualMachineScaleSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the Maintenance Configuration Resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @property
    @pulumi.getter(name="virtualMachineScaleSetId")
    def virtual_machine_scale_set_id(self) -> pulumi.Output[str]:
        """
        Specifies the Virtual Machine Scale Set ID to which the Maintenance Configuration will be assigned. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_machine_scale_set_id")

