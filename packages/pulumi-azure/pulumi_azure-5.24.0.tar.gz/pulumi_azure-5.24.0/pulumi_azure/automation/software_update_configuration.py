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

__all__ = ['SoftwareUpdateConfigurationArgs', 'SoftwareUpdateConfiguration']

@pulumi.input_type
class SoftwareUpdateConfigurationArgs:
    def __init__(__self__, *,
                 automation_account_id: pulumi.Input[str],
                 operating_system: pulumi.Input[str],
                 duration: Optional[pulumi.Input[str]] = None,
                 linuxes: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationLinuxArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 non_azure_computer_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 post_tasks: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPostTaskArgs']]]] = None,
                 pre_tasks: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPreTaskArgs']]]] = None,
                 schedules: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationScheduleArgs']]]] = None,
                 target: Optional[pulumi.Input['SoftwareUpdateConfigurationTargetArgs']] = None,
                 virtual_machine_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 windows: Optional[pulumi.Input['SoftwareUpdateConfigurationWindowsArgs']] = None):
        """
        The set of arguments for constructing a SoftwareUpdateConfiguration resource.
        :param pulumi.Input[str] automation_account_id: The ID of Automation Account to manage this Source Control. Changing this forces a new Automation Source Control to be created.
        :param pulumi.Input[str] operating_system: The Operating system of target machines. Possible values are `Windows` and `Linux`.
        :param pulumi.Input[str] duration: Maximum time allowed for the software update configuration run. using format `PT[n]H[n]M[n]S` as per ISO8601.
        :param pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationLinuxArgs']]] linuxes: One or more `linux` blocks as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Automation. Changing this forces a new Automation to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] non_azure_computer_names: Specifies a list of names of non-azure machines for the software update configuration.
        :param pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPostTaskArgs']]] post_tasks: One or more `post_task` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPreTaskArgs']]] pre_tasks: One or more `pre_task` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationScheduleArgs']]] schedules: One or more `schedule` blocks as defined below.
        :param pulumi.Input['SoftwareUpdateConfigurationTargetArgs'] target: One or more `target` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] virtual_machine_ids: Specifies a list of azure resource Ids of azure virtual machines.
        :param pulumi.Input['SoftwareUpdateConfigurationWindowsArgs'] windows: One or more `windows` blocks as defined below.
        """
        pulumi.set(__self__, "automation_account_id", automation_account_id)
        pulumi.set(__self__, "operating_system", operating_system)
        if duration is not None:
            pulumi.set(__self__, "duration", duration)
        if linuxes is not None:
            pulumi.set(__self__, "linuxes", linuxes)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if non_azure_computer_names is not None:
            pulumi.set(__self__, "non_azure_computer_names", non_azure_computer_names)
        if post_tasks is not None:
            pulumi.set(__self__, "post_tasks", post_tasks)
        if pre_tasks is not None:
            pulumi.set(__self__, "pre_tasks", pre_tasks)
        if schedules is not None:
            pulumi.set(__self__, "schedules", schedules)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if virtual_machine_ids is not None:
            pulumi.set(__self__, "virtual_machine_ids", virtual_machine_ids)
        if windows is not None:
            pulumi.set(__self__, "windows", windows)

    @property
    @pulumi.getter(name="automationAccountId")
    def automation_account_id(self) -> pulumi.Input[str]:
        """
        The ID of Automation Account to manage this Source Control. Changing this forces a new Automation Source Control to be created.
        """
        return pulumi.get(self, "automation_account_id")

    @automation_account_id.setter
    def automation_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "automation_account_id", value)

    @property
    @pulumi.getter(name="operatingSystem")
    def operating_system(self) -> pulumi.Input[str]:
        """
        The Operating system of target machines. Possible values are `Windows` and `Linux`.
        """
        return pulumi.get(self, "operating_system")

    @operating_system.setter
    def operating_system(self, value: pulumi.Input[str]):
        pulumi.set(self, "operating_system", value)

    @property
    @pulumi.getter
    def duration(self) -> Optional[pulumi.Input[str]]:
        """
        Maximum time allowed for the software update configuration run. using format `PT[n]H[n]M[n]S` as per ISO8601.
        """
        return pulumi.get(self, "duration")

    @duration.setter
    def duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "duration", value)

    @property
    @pulumi.getter
    def linuxes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationLinuxArgs']]]]:
        """
        One or more `linux` blocks as defined below.
        """
        return pulumi.get(self, "linuxes")

    @linuxes.setter
    def linuxes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationLinuxArgs']]]]):
        pulumi.set(self, "linuxes", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Automation. Changing this forces a new Automation to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="nonAzureComputerNames")
    def non_azure_computer_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of names of non-azure machines for the software update configuration.
        """
        return pulumi.get(self, "non_azure_computer_names")

    @non_azure_computer_names.setter
    def non_azure_computer_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "non_azure_computer_names", value)

    @property
    @pulumi.getter(name="postTasks")
    def post_tasks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPostTaskArgs']]]]:
        """
        One or more `post_task` blocks as defined below.
        """
        return pulumi.get(self, "post_tasks")

    @post_tasks.setter
    def post_tasks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPostTaskArgs']]]]):
        pulumi.set(self, "post_tasks", value)

    @property
    @pulumi.getter(name="preTasks")
    def pre_tasks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPreTaskArgs']]]]:
        """
        One or more `pre_task` blocks as defined below.
        """
        return pulumi.get(self, "pre_tasks")

    @pre_tasks.setter
    def pre_tasks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPreTaskArgs']]]]):
        pulumi.set(self, "pre_tasks", value)

    @property
    @pulumi.getter
    def schedules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationScheduleArgs']]]]:
        """
        One or more `schedule` blocks as defined below.
        """
        return pulumi.get(self, "schedules")

    @schedules.setter
    def schedules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationScheduleArgs']]]]):
        pulumi.set(self, "schedules", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input['SoftwareUpdateConfigurationTargetArgs']]:
        """
        One or more `target` blocks as defined below.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input['SoftwareUpdateConfigurationTargetArgs']]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="virtualMachineIds")
    def virtual_machine_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of azure resource Ids of azure virtual machines.
        """
        return pulumi.get(self, "virtual_machine_ids")

    @virtual_machine_ids.setter
    def virtual_machine_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "virtual_machine_ids", value)

    @property
    @pulumi.getter
    def windows(self) -> Optional[pulumi.Input['SoftwareUpdateConfigurationWindowsArgs']]:
        """
        One or more `windows` blocks as defined below.
        """
        return pulumi.get(self, "windows")

    @windows.setter
    def windows(self, value: Optional[pulumi.Input['SoftwareUpdateConfigurationWindowsArgs']]):
        pulumi.set(self, "windows", value)


@pulumi.input_type
class _SoftwareUpdateConfigurationState:
    def __init__(__self__, *,
                 automation_account_id: Optional[pulumi.Input[str]] = None,
                 duration: Optional[pulumi.Input[str]] = None,
                 error_code: Optional[pulumi.Input[str]] = None,
                 error_meesage: Optional[pulumi.Input[str]] = None,
                 linuxes: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationLinuxArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 non_azure_computer_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 operating_system: Optional[pulumi.Input[str]] = None,
                 post_tasks: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPostTaskArgs']]]] = None,
                 pre_tasks: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPreTaskArgs']]]] = None,
                 schedules: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationScheduleArgs']]]] = None,
                 target: Optional[pulumi.Input['SoftwareUpdateConfigurationTargetArgs']] = None,
                 virtual_machine_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 windows: Optional[pulumi.Input['SoftwareUpdateConfigurationWindowsArgs']] = None):
        """
        Input properties used for looking up and filtering SoftwareUpdateConfiguration resources.
        :param pulumi.Input[str] automation_account_id: The ID of Automation Account to manage this Source Control. Changing this forces a new Automation Source Control to be created.
        :param pulumi.Input[str] duration: Maximum time allowed for the software update configuration run. using format `PT[n]H[n]M[n]S` as per ISO8601.
        :param pulumi.Input[str] error_code: The Error code when failed.
        :param pulumi.Input[str] error_meesage: The Error message indicating why the operation failed.
        :param pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationLinuxArgs']]] linuxes: One or more `linux` blocks as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Automation. Changing this forces a new Automation to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] non_azure_computer_names: Specifies a list of names of non-azure machines for the software update configuration.
        :param pulumi.Input[str] operating_system: The Operating system of target machines. Possible values are `Windows` and `Linux`.
        :param pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPostTaskArgs']]] post_tasks: One or more `post_task` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPreTaskArgs']]] pre_tasks: One or more `pre_task` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationScheduleArgs']]] schedules: One or more `schedule` blocks as defined below.
        :param pulumi.Input['SoftwareUpdateConfigurationTargetArgs'] target: One or more `target` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] virtual_machine_ids: Specifies a list of azure resource Ids of azure virtual machines.
        :param pulumi.Input['SoftwareUpdateConfigurationWindowsArgs'] windows: One or more `windows` blocks as defined below.
        """
        if automation_account_id is not None:
            pulumi.set(__self__, "automation_account_id", automation_account_id)
        if duration is not None:
            pulumi.set(__self__, "duration", duration)
        if error_code is not None:
            pulumi.set(__self__, "error_code", error_code)
        if error_meesage is not None:
            pulumi.set(__self__, "error_meesage", error_meesage)
        if linuxes is not None:
            pulumi.set(__self__, "linuxes", linuxes)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if non_azure_computer_names is not None:
            pulumi.set(__self__, "non_azure_computer_names", non_azure_computer_names)
        if operating_system is not None:
            pulumi.set(__self__, "operating_system", operating_system)
        if post_tasks is not None:
            pulumi.set(__self__, "post_tasks", post_tasks)
        if pre_tasks is not None:
            pulumi.set(__self__, "pre_tasks", pre_tasks)
        if schedules is not None:
            pulumi.set(__self__, "schedules", schedules)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if virtual_machine_ids is not None:
            pulumi.set(__self__, "virtual_machine_ids", virtual_machine_ids)
        if windows is not None:
            pulumi.set(__self__, "windows", windows)

    @property
    @pulumi.getter(name="automationAccountId")
    def automation_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of Automation Account to manage this Source Control. Changing this forces a new Automation Source Control to be created.
        """
        return pulumi.get(self, "automation_account_id")

    @automation_account_id.setter
    def automation_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "automation_account_id", value)

    @property
    @pulumi.getter
    def duration(self) -> Optional[pulumi.Input[str]]:
        """
        Maximum time allowed for the software update configuration run. using format `PT[n]H[n]M[n]S` as per ISO8601.
        """
        return pulumi.get(self, "duration")

    @duration.setter
    def duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "duration", value)

    @property
    @pulumi.getter(name="errorCode")
    def error_code(self) -> Optional[pulumi.Input[str]]:
        """
        The Error code when failed.
        """
        return pulumi.get(self, "error_code")

    @error_code.setter
    def error_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "error_code", value)

    @property
    @pulumi.getter(name="errorMeesage")
    def error_meesage(self) -> Optional[pulumi.Input[str]]:
        """
        The Error message indicating why the operation failed.
        """
        return pulumi.get(self, "error_meesage")

    @error_meesage.setter
    def error_meesage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "error_meesage", value)

    @property
    @pulumi.getter
    def linuxes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationLinuxArgs']]]]:
        """
        One or more `linux` blocks as defined below.
        """
        return pulumi.get(self, "linuxes")

    @linuxes.setter
    def linuxes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationLinuxArgs']]]]):
        pulumi.set(self, "linuxes", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Automation. Changing this forces a new Automation to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="nonAzureComputerNames")
    def non_azure_computer_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of names of non-azure machines for the software update configuration.
        """
        return pulumi.get(self, "non_azure_computer_names")

    @non_azure_computer_names.setter
    def non_azure_computer_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "non_azure_computer_names", value)

    @property
    @pulumi.getter(name="operatingSystem")
    def operating_system(self) -> Optional[pulumi.Input[str]]:
        """
        The Operating system of target machines. Possible values are `Windows` and `Linux`.
        """
        return pulumi.get(self, "operating_system")

    @operating_system.setter
    def operating_system(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "operating_system", value)

    @property
    @pulumi.getter(name="postTasks")
    def post_tasks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPostTaskArgs']]]]:
        """
        One or more `post_task` blocks as defined below.
        """
        return pulumi.get(self, "post_tasks")

    @post_tasks.setter
    def post_tasks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPostTaskArgs']]]]):
        pulumi.set(self, "post_tasks", value)

    @property
    @pulumi.getter(name="preTasks")
    def pre_tasks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPreTaskArgs']]]]:
        """
        One or more `pre_task` blocks as defined below.
        """
        return pulumi.get(self, "pre_tasks")

    @pre_tasks.setter
    def pre_tasks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationPreTaskArgs']]]]):
        pulumi.set(self, "pre_tasks", value)

    @property
    @pulumi.getter
    def schedules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationScheduleArgs']]]]:
        """
        One or more `schedule` blocks as defined below.
        """
        return pulumi.get(self, "schedules")

    @schedules.setter
    def schedules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SoftwareUpdateConfigurationScheduleArgs']]]]):
        pulumi.set(self, "schedules", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input['SoftwareUpdateConfigurationTargetArgs']]:
        """
        One or more `target` blocks as defined below.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input['SoftwareUpdateConfigurationTargetArgs']]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="virtualMachineIds")
    def virtual_machine_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of azure resource Ids of azure virtual machines.
        """
        return pulumi.get(self, "virtual_machine_ids")

    @virtual_machine_ids.setter
    def virtual_machine_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "virtual_machine_ids", value)

    @property
    @pulumi.getter
    def windows(self) -> Optional[pulumi.Input['SoftwareUpdateConfigurationWindowsArgs']]:
        """
        One or more `windows` blocks as defined below.
        """
        return pulumi.get(self, "windows")

    @windows.setter
    def windows(self, value: Optional[pulumi.Input['SoftwareUpdateConfigurationWindowsArgs']]):
        pulumi.set(self, "windows", value)


class SoftwareUpdateConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_id: Optional[pulumi.Input[str]] = None,
                 duration: Optional[pulumi.Input[str]] = None,
                 linuxes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationLinuxArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 non_azure_computer_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 operating_system: Optional[pulumi.Input[str]] = None,
                 post_tasks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPostTaskArgs']]]]] = None,
                 pre_tasks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPreTaskArgs']]]]] = None,
                 schedules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationScheduleArgs']]]]] = None,
                 target: Optional[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationTargetArgs']]] = None,
                 virtual_machine_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 windows: Optional[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationWindowsArgs']]] = None,
                 __props__=None):
        """
        Manages an Automation Software Update Configuraion.

        ## Import

        Automations Software Update Configuration can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:automation/softwareUpdateConfiguration:SoftwareUpdateConfiguration example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/group1/providers/Microsoft.Automation/automationAccounts/account1/softwareUpdateConfigurations/suc1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_id: The ID of Automation Account to manage this Source Control. Changing this forces a new Automation Source Control to be created.
        :param pulumi.Input[str] duration: Maximum time allowed for the software update configuration run. using format `PT[n]H[n]M[n]S` as per ISO8601.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationLinuxArgs']]]] linuxes: One or more `linux` blocks as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Automation. Changing this forces a new Automation to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] non_azure_computer_names: Specifies a list of names of non-azure machines for the software update configuration.
        :param pulumi.Input[str] operating_system: The Operating system of target machines. Possible values are `Windows` and `Linux`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPostTaskArgs']]]] post_tasks: One or more `post_task` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPreTaskArgs']]]] pre_tasks: One or more `pre_task` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationScheduleArgs']]]] schedules: One or more `schedule` blocks as defined below.
        :param pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationTargetArgs']] target: One or more `target` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] virtual_machine_ids: Specifies a list of azure resource Ids of azure virtual machines.
        :param pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationWindowsArgs']] windows: One or more `windows` blocks as defined below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SoftwareUpdateConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Automation Software Update Configuraion.

        ## Import

        Automations Software Update Configuration can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:automation/softwareUpdateConfiguration:SoftwareUpdateConfiguration example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/group1/providers/Microsoft.Automation/automationAccounts/account1/softwareUpdateConfigurations/suc1
        ```

        :param str resource_name: The name of the resource.
        :param SoftwareUpdateConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SoftwareUpdateConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_id: Optional[pulumi.Input[str]] = None,
                 duration: Optional[pulumi.Input[str]] = None,
                 linuxes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationLinuxArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 non_azure_computer_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 operating_system: Optional[pulumi.Input[str]] = None,
                 post_tasks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPostTaskArgs']]]]] = None,
                 pre_tasks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPreTaskArgs']]]]] = None,
                 schedules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationScheduleArgs']]]]] = None,
                 target: Optional[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationTargetArgs']]] = None,
                 virtual_machine_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 windows: Optional[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationWindowsArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SoftwareUpdateConfigurationArgs.__new__(SoftwareUpdateConfigurationArgs)

            if automation_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'automation_account_id'")
            __props__.__dict__["automation_account_id"] = automation_account_id
            __props__.__dict__["duration"] = duration
            __props__.__dict__["linuxes"] = linuxes
            __props__.__dict__["name"] = name
            __props__.__dict__["non_azure_computer_names"] = non_azure_computer_names
            if operating_system is None and not opts.urn:
                raise TypeError("Missing required property 'operating_system'")
            __props__.__dict__["operating_system"] = operating_system
            __props__.__dict__["post_tasks"] = post_tasks
            __props__.__dict__["pre_tasks"] = pre_tasks
            __props__.__dict__["schedules"] = schedules
            __props__.__dict__["target"] = target
            __props__.__dict__["virtual_machine_ids"] = virtual_machine_ids
            __props__.__dict__["windows"] = windows
            __props__.__dict__["error_code"] = None
            __props__.__dict__["error_meesage"] = None
        super(SoftwareUpdateConfiguration, __self__).__init__(
            'azure:automation/softwareUpdateConfiguration:SoftwareUpdateConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            automation_account_id: Optional[pulumi.Input[str]] = None,
            duration: Optional[pulumi.Input[str]] = None,
            error_code: Optional[pulumi.Input[str]] = None,
            error_meesage: Optional[pulumi.Input[str]] = None,
            linuxes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationLinuxArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            non_azure_computer_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            operating_system: Optional[pulumi.Input[str]] = None,
            post_tasks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPostTaskArgs']]]]] = None,
            pre_tasks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPreTaskArgs']]]]] = None,
            schedules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationScheduleArgs']]]]] = None,
            target: Optional[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationTargetArgs']]] = None,
            virtual_machine_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            windows: Optional[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationWindowsArgs']]] = None) -> 'SoftwareUpdateConfiguration':
        """
        Get an existing SoftwareUpdateConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_id: The ID of Automation Account to manage this Source Control. Changing this forces a new Automation Source Control to be created.
        :param pulumi.Input[str] duration: Maximum time allowed for the software update configuration run. using format `PT[n]H[n]M[n]S` as per ISO8601.
        :param pulumi.Input[str] error_code: The Error code when failed.
        :param pulumi.Input[str] error_meesage: The Error message indicating why the operation failed.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationLinuxArgs']]]] linuxes: One or more `linux` blocks as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Automation. Changing this forces a new Automation to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] non_azure_computer_names: Specifies a list of names of non-azure machines for the software update configuration.
        :param pulumi.Input[str] operating_system: The Operating system of target machines. Possible values are `Windows` and `Linux`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPostTaskArgs']]]] post_tasks: One or more `post_task` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationPreTaskArgs']]]] pre_tasks: One or more `pre_task` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationScheduleArgs']]]] schedules: One or more `schedule` blocks as defined below.
        :param pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationTargetArgs']] target: One or more `target` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] virtual_machine_ids: Specifies a list of azure resource Ids of azure virtual machines.
        :param pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationWindowsArgs']] windows: One or more `windows` blocks as defined below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SoftwareUpdateConfigurationState.__new__(_SoftwareUpdateConfigurationState)

        __props__.__dict__["automation_account_id"] = automation_account_id
        __props__.__dict__["duration"] = duration
        __props__.__dict__["error_code"] = error_code
        __props__.__dict__["error_meesage"] = error_meesage
        __props__.__dict__["linuxes"] = linuxes
        __props__.__dict__["name"] = name
        __props__.__dict__["non_azure_computer_names"] = non_azure_computer_names
        __props__.__dict__["operating_system"] = operating_system
        __props__.__dict__["post_tasks"] = post_tasks
        __props__.__dict__["pre_tasks"] = pre_tasks
        __props__.__dict__["schedules"] = schedules
        __props__.__dict__["target"] = target
        __props__.__dict__["virtual_machine_ids"] = virtual_machine_ids
        __props__.__dict__["windows"] = windows
        return SoftwareUpdateConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="automationAccountId")
    def automation_account_id(self) -> pulumi.Output[str]:
        """
        The ID of Automation Account to manage this Source Control. Changing this forces a new Automation Source Control to be created.
        """
        return pulumi.get(self, "automation_account_id")

    @property
    @pulumi.getter
    def duration(self) -> pulumi.Output[Optional[str]]:
        """
        Maximum time allowed for the software update configuration run. using format `PT[n]H[n]M[n]S` as per ISO8601.
        """
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="errorCode")
    def error_code(self) -> pulumi.Output[str]:
        """
        The Error code when failed.
        """
        return pulumi.get(self, "error_code")

    @property
    @pulumi.getter(name="errorMeesage")
    def error_meesage(self) -> pulumi.Output[str]:
        """
        The Error message indicating why the operation failed.
        """
        return pulumi.get(self, "error_meesage")

    @property
    @pulumi.getter
    def linuxes(self) -> pulumi.Output[Optional[Sequence['outputs.SoftwareUpdateConfigurationLinux']]]:
        """
        One or more `linux` blocks as defined below.
        """
        return pulumi.get(self, "linuxes")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Automation. Changing this forces a new Automation to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nonAzureComputerNames")
    def non_azure_computer_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies a list of names of non-azure machines for the software update configuration.
        """
        return pulumi.get(self, "non_azure_computer_names")

    @property
    @pulumi.getter(name="operatingSystem")
    def operating_system(self) -> pulumi.Output[str]:
        """
        The Operating system of target machines. Possible values are `Windows` and `Linux`.
        """
        return pulumi.get(self, "operating_system")

    @property
    @pulumi.getter(name="postTasks")
    def post_tasks(self) -> pulumi.Output[Optional[Sequence['outputs.SoftwareUpdateConfigurationPostTask']]]:
        """
        One or more `post_task` blocks as defined below.
        """
        return pulumi.get(self, "post_tasks")

    @property
    @pulumi.getter(name="preTasks")
    def pre_tasks(self) -> pulumi.Output[Optional[Sequence['outputs.SoftwareUpdateConfigurationPreTask']]]:
        """
        One or more `pre_task` blocks as defined below.
        """
        return pulumi.get(self, "pre_tasks")

    @property
    @pulumi.getter
    def schedules(self) -> pulumi.Output[Optional[Sequence['outputs.SoftwareUpdateConfigurationSchedule']]]:
        """
        One or more `schedule` blocks as defined below.
        """
        return pulumi.get(self, "schedules")

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output[Optional['outputs.SoftwareUpdateConfigurationTarget']]:
        """
        One or more `target` blocks as defined below.
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter(name="virtualMachineIds")
    def virtual_machine_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies a list of azure resource Ids of azure virtual machines.
        """
        return pulumi.get(self, "virtual_machine_ids")

    @property
    @pulumi.getter
    def windows(self) -> pulumi.Output[Optional['outputs.SoftwareUpdateConfigurationWindows']]:
        """
        One or more `windows` blocks as defined below.
        """
        return pulumi.get(self, "windows")

