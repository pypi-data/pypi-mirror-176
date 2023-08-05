# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LinkedServiceArgs', 'LinkedService']

@pulumi.input_type
class LinkedServiceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 workspace_id: pulumi.Input[str],
                 read_access_id: Optional[pulumi.Input[str]] = None,
                 write_access_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a LinkedService resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Log Analytics Linked Service is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] workspace_id: The ID of the Log Analytics Workspace that will contain the Log Analytics Linked Service resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] read_access_id: The ID of the readable Resource that will be linked to the workspace. This should be used for linking to an Automation Account resource.
        :param pulumi.Input[str] write_access_id: The ID of the writable Resource that will be linked to the workspace. This should be used for linking to a Log Analytics Cluster resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_id", workspace_id)
        if read_access_id is not None:
            pulumi.set(__self__, "read_access_id", read_access_id)
        if write_access_id is not None:
            pulumi.set(__self__, "write_access_id", write_access_id)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which the Log Analytics Linked Service is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Input[str]:
        """
        The ID of the Log Analytics Workspace that will contain the Log Analytics Linked Service resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_id", value)

    @property
    @pulumi.getter(name="readAccessId")
    def read_access_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the readable Resource that will be linked to the workspace. This should be used for linking to an Automation Account resource.
        """
        return pulumi.get(self, "read_access_id")

    @read_access_id.setter
    def read_access_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "read_access_id", value)

    @property
    @pulumi.getter(name="writeAccessId")
    def write_access_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the writable Resource that will be linked to the workspace. This should be used for linking to a Log Analytics Cluster resource.
        """
        return pulumi.get(self, "write_access_id")

    @write_access_id.setter
    def write_access_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "write_access_id", value)


@pulumi.input_type
class _LinkedServiceState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 read_access_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 write_access_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LinkedService resources.
        :param pulumi.Input[str] name: The generated name of the Linked Service. The format for this attribute is always `<workspace name>/<linked service type>`(e.g. `workspace1/Automation` or `workspace1/Cluster`)
        :param pulumi.Input[str] read_access_id: The ID of the readable Resource that will be linked to the workspace. This should be used for linking to an Automation Account resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Log Analytics Linked Service is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] workspace_id: The ID of the Log Analytics Workspace that will contain the Log Analytics Linked Service resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] write_access_id: The ID of the writable Resource that will be linked to the workspace. This should be used for linking to a Log Analytics Cluster resource.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if read_access_id is not None:
            pulumi.set(__self__, "read_access_id", read_access_id)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if workspace_id is not None:
            pulumi.set(__self__, "workspace_id", workspace_id)
        if write_access_id is not None:
            pulumi.set(__self__, "write_access_id", write_access_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The generated name of the Linked Service. The format for this attribute is always `<workspace name>/<linked service type>`(e.g. `workspace1/Automation` or `workspace1/Cluster`)
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="readAccessId")
    def read_access_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the readable Resource that will be linked to the workspace. This should be used for linking to an Automation Account resource.
        """
        return pulumi.get(self, "read_access_id")

    @read_access_id.setter
    def read_access_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "read_access_id", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which the Log Analytics Linked Service is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Log Analytics Workspace that will contain the Log Analytics Linked Service resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_id", value)

    @property
    @pulumi.getter(name="writeAccessId")
    def write_access_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the writable Resource that will be linked to the workspace. This should be used for linking to a Log Analytics Cluster resource.
        """
        return pulumi.get(self, "write_access_id")

    @write_access_id.setter
    def write_access_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "write_access_id", value)


class LinkedService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 read_access_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 write_access_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Log Analytics Linked Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.automation.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Basic",
            tags={
                "environment": "development",
            })
        example_analytics_workspace = azure.operationalinsights.AnalyticsWorkspace("exampleAnalyticsWorkspace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="PerGB2018",
            retention_in_days=30)
        example_linked_service = azure.loganalytics.LinkedService("exampleLinkedService",
            resource_group_name=example_resource_group.name,
            workspace_id=example_analytics_workspace.id,
            read_access_id=example_account.id)
        ```

        ## Import

        Log Analytics Workspaces can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:loganalytics/linkedService:LinkedService example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.OperationalInsights/workspaces/workspace1/linkedServices/Automation
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] read_access_id: The ID of the readable Resource that will be linked to the workspace. This should be used for linking to an Automation Account resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Log Analytics Linked Service is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] workspace_id: The ID of the Log Analytics Workspace that will contain the Log Analytics Linked Service resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] write_access_id: The ID of the writable Resource that will be linked to the workspace. This should be used for linking to a Log Analytics Cluster resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LinkedServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Log Analytics Linked Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.automation.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Basic",
            tags={
                "environment": "development",
            })
        example_analytics_workspace = azure.operationalinsights.AnalyticsWorkspace("exampleAnalyticsWorkspace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="PerGB2018",
            retention_in_days=30)
        example_linked_service = azure.loganalytics.LinkedService("exampleLinkedService",
            resource_group_name=example_resource_group.name,
            workspace_id=example_analytics_workspace.id,
            read_access_id=example_account.id)
        ```

        ## Import

        Log Analytics Workspaces can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:loganalytics/linkedService:LinkedService example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.OperationalInsights/workspaces/workspace1/linkedServices/Automation
        ```

        :param str resource_name: The name of the resource.
        :param LinkedServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LinkedServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 read_access_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 write_access_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LinkedServiceArgs.__new__(LinkedServiceArgs)

            __props__.__dict__["read_access_id"] = read_access_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if workspace_id is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_id'")
            __props__.__dict__["workspace_id"] = workspace_id
            __props__.__dict__["write_access_id"] = write_access_id
            __props__.__dict__["name"] = None
        super(LinkedService, __self__).__init__(
            'azure:loganalytics/linkedService:LinkedService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            read_access_id: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            workspace_id: Optional[pulumi.Input[str]] = None,
            write_access_id: Optional[pulumi.Input[str]] = None) -> 'LinkedService':
        """
        Get an existing LinkedService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The generated name of the Linked Service. The format for this attribute is always `<workspace name>/<linked service type>`(e.g. `workspace1/Automation` or `workspace1/Cluster`)
        :param pulumi.Input[str] read_access_id: The ID of the readable Resource that will be linked to the workspace. This should be used for linking to an Automation Account resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Log Analytics Linked Service is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] workspace_id: The ID of the Log Analytics Workspace that will contain the Log Analytics Linked Service resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] write_access_id: The ID of the writable Resource that will be linked to the workspace. This should be used for linking to a Log Analytics Cluster resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LinkedServiceState.__new__(_LinkedServiceState)

        __props__.__dict__["name"] = name
        __props__.__dict__["read_access_id"] = read_access_id
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["workspace_id"] = workspace_id
        __props__.__dict__["write_access_id"] = write_access_id
        return LinkedService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The generated name of the Linked Service. The format for this attribute is always `<workspace name>/<linked service type>`(e.g. `workspace1/Automation` or `workspace1/Cluster`)
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="readAccessId")
    def read_access_id(self) -> pulumi.Output[str]:
        """
        The ID of the readable Resource that will be linked to the workspace. This should be used for linking to an Automation Account resource.
        """
        return pulumi.get(self, "read_access_id")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which the Log Analytics Linked Service is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[str]:
        """
        The ID of the Log Analytics Workspace that will contain the Log Analytics Linked Service resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "workspace_id")

    @property
    @pulumi.getter(name="writeAccessId")
    def write_access_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the writable Resource that will be linked to the workspace. This should be used for linking to a Log Analytics Cluster resource.
        """
        return pulumi.get(self, "write_access_id")

