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

__all__ = ['NetworkConnectionMonitorArgs', 'NetworkConnectionMonitor']

@pulumi.input_type
class NetworkConnectionMonitorArgs:
    def __init__(__self__, *,
                 endpoints: pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorEndpointArgs']]],
                 network_watcher_id: pulumi.Input[str],
                 test_configurations: pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestConfigurationArgs']]],
                 test_groups: pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestGroupArgs']]],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 output_workspace_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NetworkConnectionMonitor resource.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorEndpointArgs']]] endpoints: A `endpoint` block as defined below.
        :param pulumi.Input[str] network_watcher_id: The ID of the Network Watcher. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestConfigurationArgs']]] test_configurations: A `test_configuration` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestGroupArgs']]] test_groups: A `test_group` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the Network Connection Monitor should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for this Network Connection Monitor. Changing this forces a new resource to be created.
        :param pulumi.Input[str] notes: The description of the Network Connection Monitor.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] output_workspace_resource_ids: A list of IDs of the Log Analytics Workspace which will accept the output from the Network Connection Monitor.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Network Connection Monitor.
        """
        pulumi.set(__self__, "endpoints", endpoints)
        pulumi.set(__self__, "network_watcher_id", network_watcher_id)
        pulumi.set(__self__, "test_configurations", test_configurations)
        pulumi.set(__self__, "test_groups", test_groups)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if notes is not None:
            pulumi.set(__self__, "notes", notes)
        if output_workspace_resource_ids is not None:
            pulumi.set(__self__, "output_workspace_resource_ids", output_workspace_resource_ids)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def endpoints(self) -> pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorEndpointArgs']]]:
        """
        A `endpoint` block as defined below.
        """
        return pulumi.get(self, "endpoints")

    @endpoints.setter
    def endpoints(self, value: pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorEndpointArgs']]]):
        pulumi.set(self, "endpoints", value)

    @property
    @pulumi.getter(name="networkWatcherId")
    def network_watcher_id(self) -> pulumi.Input[str]:
        """
        The ID of the Network Watcher. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "network_watcher_id")

    @network_watcher_id.setter
    def network_watcher_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_watcher_id", value)

    @property
    @pulumi.getter(name="testConfigurations")
    def test_configurations(self) -> pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestConfigurationArgs']]]:
        """
        A `test_configuration` block as defined below.
        """
        return pulumi.get(self, "test_configurations")

    @test_configurations.setter
    def test_configurations(self, value: pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestConfigurationArgs']]]):
        pulumi.set(self, "test_configurations", value)

    @property
    @pulumi.getter(name="testGroups")
    def test_groups(self) -> pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestGroupArgs']]]:
        """
        A `test_group` block as defined below.
        """
        return pulumi.get(self, "test_groups")

    @test_groups.setter
    def test_groups(self, value: pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestGroupArgs']]]):
        pulumi.set(self, "test_groups", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Network Connection Monitor should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Network Connection Monitor. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def notes(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Network Connection Monitor.
        """
        return pulumi.get(self, "notes")

    @notes.setter
    def notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notes", value)

    @property
    @pulumi.getter(name="outputWorkspaceResourceIds")
    def output_workspace_resource_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IDs of the Log Analytics Workspace which will accept the output from the Network Connection Monitor.
        """
        return pulumi.get(self, "output_workspace_resource_ids")

    @output_workspace_resource_ids.setter
    def output_workspace_resource_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "output_workspace_resource_ids", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Network Connection Monitor.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _NetworkConnectionMonitorState:
    def __init__(__self__, *,
                 endpoints: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorEndpointArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_watcher_id: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 output_workspace_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 test_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestConfigurationArgs']]]] = None,
                 test_groups: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestGroupArgs']]]] = None):
        """
        Input properties used for looking up and filtering NetworkConnectionMonitor resources.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorEndpointArgs']]] endpoints: A `endpoint` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the Network Connection Monitor should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for this Network Connection Monitor. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_watcher_id: The ID of the Network Watcher. Changing this forces a new resource to be created.
        :param pulumi.Input[str] notes: The description of the Network Connection Monitor.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] output_workspace_resource_ids: A list of IDs of the Log Analytics Workspace which will accept the output from the Network Connection Monitor.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Network Connection Monitor.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestConfigurationArgs']]] test_configurations: A `test_configuration` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestGroupArgs']]] test_groups: A `test_group` block as defined below.
        """
        if endpoints is not None:
            pulumi.set(__self__, "endpoints", endpoints)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network_watcher_id is not None:
            pulumi.set(__self__, "network_watcher_id", network_watcher_id)
        if notes is not None:
            pulumi.set(__self__, "notes", notes)
        if output_workspace_resource_ids is not None:
            pulumi.set(__self__, "output_workspace_resource_ids", output_workspace_resource_ids)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if test_configurations is not None:
            pulumi.set(__self__, "test_configurations", test_configurations)
        if test_groups is not None:
            pulumi.set(__self__, "test_groups", test_groups)

    @property
    @pulumi.getter
    def endpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorEndpointArgs']]]]:
        """
        A `endpoint` block as defined below.
        """
        return pulumi.get(self, "endpoints")

    @endpoints.setter
    def endpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorEndpointArgs']]]]):
        pulumi.set(self, "endpoints", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Network Connection Monitor should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Network Connection Monitor. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="networkWatcherId")
    def network_watcher_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Network Watcher. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "network_watcher_id")

    @network_watcher_id.setter
    def network_watcher_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_watcher_id", value)

    @property
    @pulumi.getter
    def notes(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Network Connection Monitor.
        """
        return pulumi.get(self, "notes")

    @notes.setter
    def notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notes", value)

    @property
    @pulumi.getter(name="outputWorkspaceResourceIds")
    def output_workspace_resource_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IDs of the Log Analytics Workspace which will accept the output from the Network Connection Monitor.
        """
        return pulumi.get(self, "output_workspace_resource_ids")

    @output_workspace_resource_ids.setter
    def output_workspace_resource_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "output_workspace_resource_ids", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Network Connection Monitor.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="testConfigurations")
    def test_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestConfigurationArgs']]]]:
        """
        A `test_configuration` block as defined below.
        """
        return pulumi.get(self, "test_configurations")

    @test_configurations.setter
    def test_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestConfigurationArgs']]]]):
        pulumi.set(self, "test_configurations", value)

    @property
    @pulumi.getter(name="testGroups")
    def test_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestGroupArgs']]]]:
        """
        A `test_group` block as defined below.
        """
        return pulumi.get(self, "test_groups")

    @test_groups.setter
    def test_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkConnectionMonitorTestGroupArgs']]]]):
        pulumi.set(self, "test_groups", value)


class NetworkConnectionMonitor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorEndpointArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_watcher_id: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 output_workspace_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 test_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestConfigurationArgs']]]]] = None,
                 test_groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestGroupArgs']]]]] = None,
                 __props__=None):
        """
        Manages a Network Connection Monitor.

        > **NOTE:** Any Network Connection Monitor resource created with API versions 2019-06-01 or earlier (v1) are now incompatible with this provider, which now only supports v2.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_network_watcher = azure.network.NetworkWatcher("exampleNetworkWatcher",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.0.2.0/24"])
        example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
                name="testconfiguration1",
                subnet_id=example_subnet.id,
                private_ip_address_allocation="Dynamic",
            )])
        example_virtual_machine = azure.compute.VirtualMachine("exampleVirtualMachine",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            network_interface_ids=[example_network_interface.id],
            vm_size="Standard_D2s_v3",
            storage_image_reference=azure.compute.VirtualMachineStorageImageReferenceArgs(
                publisher="Canonical",
                offer="UbuntuServer",
                sku="16.04-LTS",
                version="latest",
            ),
            storage_os_disk=azure.compute.VirtualMachineStorageOsDiskArgs(
                name="osdisk-example01",
                caching="ReadWrite",
                create_option="FromImage",
                managed_disk_type="Standard_LRS",
            ),
            os_profile=azure.compute.VirtualMachineOsProfileArgs(
                computer_name="hostnametest01",
                admin_username="testadmin",
                admin_password="Password1234!",
            ),
            os_profile_linux_config=azure.compute.VirtualMachineOsProfileLinuxConfigArgs(
                disable_password_authentication=False,
            ))
        example_extension = azure.compute.Extension("exampleExtension",
            virtual_machine_id=example_virtual_machine.id,
            publisher="Microsoft.Azure.NetworkWatcher",
            type="NetworkWatcherAgentLinux",
            type_handler_version="1.4",
            auto_upgrade_minor_version=True)
        example_analytics_workspace = azure.operationalinsights.AnalyticsWorkspace("exampleAnalyticsWorkspace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="PerGB2018")
        example_network_connection_monitor = azure.network.NetworkConnectionMonitor("exampleNetworkConnectionMonitor",
            network_watcher_id=example_network_watcher.id,
            location=example_network_watcher.location,
            endpoints=[
                azure.network.NetworkConnectionMonitorEndpointArgs(
                    name="source",
                    target_resource_id=example_virtual_machine.id,
                    filter=azure.network.NetworkConnectionMonitorEndpointFilterArgs(
                        items=[azure.network.NetworkConnectionMonitorEndpointFilterItemArgs(
                            address=example_virtual_machine.id,
                            type="AgentAddress",
                        )],
                        type="Include",
                    ),
                ),
                azure.network.NetworkConnectionMonitorEndpointArgs(
                    name="destination",
                    address="mycompany.io",
                ),
            ],
            test_configurations=[azure.network.NetworkConnectionMonitorTestConfigurationArgs(
                name="tcpName",
                protocol="Tcp",
                test_frequency_in_seconds=60,
                tcp_configuration=azure.network.NetworkConnectionMonitorTestConfigurationTcpConfigurationArgs(
                    port=80,
                ),
            )],
            test_groups=[azure.network.NetworkConnectionMonitorTestGroupArgs(
                name="exampletg",
                destination_endpoints=["destination"],
                source_endpoints=["source"],
                test_configuration_names=["tcpName"],
            )],
            notes="examplenote",
            output_workspace_resource_ids=[example_analytics_workspace.id],
            opts=pulumi.ResourceOptions(depends_on=[example_extension]))
        ```

        ## Import

        Network Connection Monitors can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/networkConnectionMonitor:NetworkConnectionMonitor example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/networkWatchers/watcher1/connectionMonitors/connectionMonitor1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorEndpointArgs']]]] endpoints: A `endpoint` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the Network Connection Monitor should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for this Network Connection Monitor. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_watcher_id: The ID of the Network Watcher. Changing this forces a new resource to be created.
        :param pulumi.Input[str] notes: The description of the Network Connection Monitor.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] output_workspace_resource_ids: A list of IDs of the Log Analytics Workspace which will accept the output from the Network Connection Monitor.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Network Connection Monitor.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestConfigurationArgs']]]] test_configurations: A `test_configuration` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestGroupArgs']]]] test_groups: A `test_group` block as defined below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkConnectionMonitorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Network Connection Monitor.

        > **NOTE:** Any Network Connection Monitor resource created with API versions 2019-06-01 or earlier (v1) are now incompatible with this provider, which now only supports v2.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_network_watcher = azure.network.NetworkWatcher("exampleNetworkWatcher",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.0.2.0/24"])
        example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
                name="testconfiguration1",
                subnet_id=example_subnet.id,
                private_ip_address_allocation="Dynamic",
            )])
        example_virtual_machine = azure.compute.VirtualMachine("exampleVirtualMachine",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            network_interface_ids=[example_network_interface.id],
            vm_size="Standard_D2s_v3",
            storage_image_reference=azure.compute.VirtualMachineStorageImageReferenceArgs(
                publisher="Canonical",
                offer="UbuntuServer",
                sku="16.04-LTS",
                version="latest",
            ),
            storage_os_disk=azure.compute.VirtualMachineStorageOsDiskArgs(
                name="osdisk-example01",
                caching="ReadWrite",
                create_option="FromImage",
                managed_disk_type="Standard_LRS",
            ),
            os_profile=azure.compute.VirtualMachineOsProfileArgs(
                computer_name="hostnametest01",
                admin_username="testadmin",
                admin_password="Password1234!",
            ),
            os_profile_linux_config=azure.compute.VirtualMachineOsProfileLinuxConfigArgs(
                disable_password_authentication=False,
            ))
        example_extension = azure.compute.Extension("exampleExtension",
            virtual_machine_id=example_virtual_machine.id,
            publisher="Microsoft.Azure.NetworkWatcher",
            type="NetworkWatcherAgentLinux",
            type_handler_version="1.4",
            auto_upgrade_minor_version=True)
        example_analytics_workspace = azure.operationalinsights.AnalyticsWorkspace("exampleAnalyticsWorkspace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="PerGB2018")
        example_network_connection_monitor = azure.network.NetworkConnectionMonitor("exampleNetworkConnectionMonitor",
            network_watcher_id=example_network_watcher.id,
            location=example_network_watcher.location,
            endpoints=[
                azure.network.NetworkConnectionMonitorEndpointArgs(
                    name="source",
                    target_resource_id=example_virtual_machine.id,
                    filter=azure.network.NetworkConnectionMonitorEndpointFilterArgs(
                        items=[azure.network.NetworkConnectionMonitorEndpointFilterItemArgs(
                            address=example_virtual_machine.id,
                            type="AgentAddress",
                        )],
                        type="Include",
                    ),
                ),
                azure.network.NetworkConnectionMonitorEndpointArgs(
                    name="destination",
                    address="mycompany.io",
                ),
            ],
            test_configurations=[azure.network.NetworkConnectionMonitorTestConfigurationArgs(
                name="tcpName",
                protocol="Tcp",
                test_frequency_in_seconds=60,
                tcp_configuration=azure.network.NetworkConnectionMonitorTestConfigurationTcpConfigurationArgs(
                    port=80,
                ),
            )],
            test_groups=[azure.network.NetworkConnectionMonitorTestGroupArgs(
                name="exampletg",
                destination_endpoints=["destination"],
                source_endpoints=["source"],
                test_configuration_names=["tcpName"],
            )],
            notes="examplenote",
            output_workspace_resource_ids=[example_analytics_workspace.id],
            opts=pulumi.ResourceOptions(depends_on=[example_extension]))
        ```

        ## Import

        Network Connection Monitors can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/networkConnectionMonitor:NetworkConnectionMonitor example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/networkWatchers/watcher1/connectionMonitors/connectionMonitor1
        ```

        :param str resource_name: The name of the resource.
        :param NetworkConnectionMonitorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkConnectionMonitorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorEndpointArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_watcher_id: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 output_workspace_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 test_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestConfigurationArgs']]]]] = None,
                 test_groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestGroupArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkConnectionMonitorArgs.__new__(NetworkConnectionMonitorArgs)

            if endpoints is None and not opts.urn:
                raise TypeError("Missing required property 'endpoints'")
            __props__.__dict__["endpoints"] = endpoints
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if network_watcher_id is None and not opts.urn:
                raise TypeError("Missing required property 'network_watcher_id'")
            __props__.__dict__["network_watcher_id"] = network_watcher_id
            __props__.__dict__["notes"] = notes
            __props__.__dict__["output_workspace_resource_ids"] = output_workspace_resource_ids
            __props__.__dict__["tags"] = tags
            if test_configurations is None and not opts.urn:
                raise TypeError("Missing required property 'test_configurations'")
            __props__.__dict__["test_configurations"] = test_configurations
            if test_groups is None and not opts.urn:
                raise TypeError("Missing required property 'test_groups'")
            __props__.__dict__["test_groups"] = test_groups
        super(NetworkConnectionMonitor, __self__).__init__(
            'azure:network/networkConnectionMonitor:NetworkConnectionMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorEndpointArgs']]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network_watcher_id: Optional[pulumi.Input[str]] = None,
            notes: Optional[pulumi.Input[str]] = None,
            output_workspace_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            test_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestConfigurationArgs']]]]] = None,
            test_groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestGroupArgs']]]]] = None) -> 'NetworkConnectionMonitor':
        """
        Get an existing NetworkConnectionMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorEndpointArgs']]]] endpoints: A `endpoint` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the Network Connection Monitor should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for this Network Connection Monitor. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_watcher_id: The ID of the Network Watcher. Changing this forces a new resource to be created.
        :param pulumi.Input[str] notes: The description of the Network Connection Monitor.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] output_workspace_resource_ids: A list of IDs of the Log Analytics Workspace which will accept the output from the Network Connection Monitor.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Network Connection Monitor.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestConfigurationArgs']]]] test_configurations: A `test_configuration` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkConnectionMonitorTestGroupArgs']]]] test_groups: A `test_group` block as defined below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkConnectionMonitorState.__new__(_NetworkConnectionMonitorState)

        __props__.__dict__["endpoints"] = endpoints
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["network_watcher_id"] = network_watcher_id
        __props__.__dict__["notes"] = notes
        __props__.__dict__["output_workspace_resource_ids"] = output_workspace_resource_ids
        __props__.__dict__["tags"] = tags
        __props__.__dict__["test_configurations"] = test_configurations
        __props__.__dict__["test_groups"] = test_groups
        return NetworkConnectionMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def endpoints(self) -> pulumi.Output[Sequence['outputs.NetworkConnectionMonitorEndpoint']]:
        """
        A `endpoint` block as defined below.
        """
        return pulumi.get(self, "endpoints")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Network Connection Monitor should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Network Connection Monitor. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkWatcherId")
    def network_watcher_id(self) -> pulumi.Output[str]:
        """
        The ID of the Network Watcher. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "network_watcher_id")

    @property
    @pulumi.getter
    def notes(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the Network Connection Monitor.
        """
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter(name="outputWorkspaceResourceIds")
    def output_workspace_resource_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of IDs of the Log Analytics Workspace which will accept the output from the Network Connection Monitor.
        """
        return pulumi.get(self, "output_workspace_resource_ids")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Network Connection Monitor.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="testConfigurations")
    def test_configurations(self) -> pulumi.Output[Sequence['outputs.NetworkConnectionMonitorTestConfiguration']]:
        """
        A `test_configuration` block as defined below.
        """
        return pulumi.get(self, "test_configurations")

    @property
    @pulumi.getter(name="testGroups")
    def test_groups(self) -> pulumi.Output[Sequence['outputs.NetworkConnectionMonitorTestGroup']]:
        """
        A `test_group` block as defined below.
        """
        return pulumi.get(self, "test_groups")

