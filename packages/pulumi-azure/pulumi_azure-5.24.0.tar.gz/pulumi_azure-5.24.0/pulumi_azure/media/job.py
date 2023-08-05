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

__all__ = ['JobArgs', 'Job']

@pulumi.input_type
class JobArgs:
    def __init__(__self__, *,
                 input_asset: pulumi.Input['JobInputAssetArgs'],
                 media_services_account_name: pulumi.Input[str],
                 output_assets: pulumi.Input[Sequence[pulumi.Input['JobOutputAssetArgs']]],
                 resource_group_name: pulumi.Input[str],
                 transform_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Job resource.
        :param pulumi.Input['JobInputAssetArgs'] input_asset: A `input_asset` block as defined below. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Transform to be created.
        :param pulumi.Input[Sequence[pulumi.Input['JobOutputAssetArgs']]] output_assets: One or more `output_asset` blocks as defined below. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Media Job should exist. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] transform_name: The Transform name. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] description: Optional customer supplied description of the Job.
        :param pulumi.Input[str] name: The name which should be used for this Media Job. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] priority: Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal. Changing this forces a new Media Job to be created.
        """
        pulumi.set(__self__, "input_asset", input_asset)
        pulumi.set(__self__, "media_services_account_name", media_services_account_name)
        pulumi.set(__self__, "output_assets", output_assets)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "transform_name", transform_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)

    @property
    @pulumi.getter(name="inputAsset")
    def input_asset(self) -> pulumi.Input['JobInputAssetArgs']:
        """
        A `input_asset` block as defined below. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "input_asset")

    @input_asset.setter
    def input_asset(self, value: pulumi.Input['JobInputAssetArgs']):
        pulumi.set(self, "input_asset", value)

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> pulumi.Input[str]:
        """
        The Media Services account name. Changing this forces a new Transform to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @media_services_account_name.setter
    def media_services_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "media_services_account_name", value)

    @property
    @pulumi.getter(name="outputAssets")
    def output_assets(self) -> pulumi.Input[Sequence[pulumi.Input['JobOutputAssetArgs']]]:
        """
        One or more `output_asset` blocks as defined below. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "output_assets")

    @output_assets.setter
    def output_assets(self, value: pulumi.Input[Sequence[pulumi.Input['JobOutputAssetArgs']]]):
        pulumi.set(self, "output_assets", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Media Job should exist. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="transformName")
    def transform_name(self) -> pulumi.Input[str]:
        """
        The Transform name. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "transform_name")

    @transform_name.setter
    def transform_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "transform_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional customer supplied description of the Job.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Media Job. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[str]]:
        """
        Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "priority", value)


@pulumi.input_type
class _JobState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 input_asset: Optional[pulumi.Input['JobInputAssetArgs']] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_assets: Optional[pulumi.Input[Sequence[pulumi.Input['JobOutputAssetArgs']]]] = None,
                 priority: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 transform_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Job resources.
        :param pulumi.Input[str] description: Optional customer supplied description of the Job.
        :param pulumi.Input['JobInputAssetArgs'] input_asset: A `input_asset` block as defined below. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Transform to be created.
        :param pulumi.Input[str] name: The name which should be used for this Media Job. Changing this forces a new Media Job to be created.
        :param pulumi.Input[Sequence[pulumi.Input['JobOutputAssetArgs']]] output_assets: One or more `output_asset` blocks as defined below. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] priority: Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Media Job should exist. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] transform_name: The Transform name. Changing this forces a new Media Job to be created.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if input_asset is not None:
            pulumi.set(__self__, "input_asset", input_asset)
        if media_services_account_name is not None:
            pulumi.set(__self__, "media_services_account_name", media_services_account_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if output_assets is not None:
            pulumi.set(__self__, "output_assets", output_assets)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if transform_name is not None:
            pulumi.set(__self__, "transform_name", transform_name)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional customer supplied description of the Job.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="inputAsset")
    def input_asset(self) -> Optional[pulumi.Input['JobInputAssetArgs']]:
        """
        A `input_asset` block as defined below. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "input_asset")

    @input_asset.setter
    def input_asset(self, value: Optional[pulumi.Input['JobInputAssetArgs']]):
        pulumi.set(self, "input_asset", value)

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Media Services account name. Changing this forces a new Transform to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @media_services_account_name.setter
    def media_services_account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "media_services_account_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Media Job. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="outputAssets")
    def output_assets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['JobOutputAssetArgs']]]]:
        """
        One or more `output_asset` blocks as defined below. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "output_assets")

    @output_assets.setter
    def output_assets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['JobOutputAssetArgs']]]]):
        pulumi.set(self, "output_assets", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[str]]:
        """
        Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Media Job should exist. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="transformName")
    def transform_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Transform name. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "transform_name")

    @transform_name.setter
    def transform_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transform_name", value)


class Job(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 input_asset: Optional[pulumi.Input[pulumi.InputType['JobInputAssetArgs']]] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_assets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobOutputAssetArgs']]]]] = None,
                 priority: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 transform_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Media Job.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="GRS")
        example_service_account = azure.media.ServiceAccount("exampleServiceAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            storage_accounts=[azure.media.ServiceAccountStorageAccountArgs(
                id=example_account.id,
                is_primary=True,
            )])
        example_transform = azure.media.Transform("exampleTransform",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            description="My transform description",
            outputs=[azure.media.TransformOutputArgs(
                relative_priority="Normal",
                on_error_action="ContinueJob",
                builtin_preset=azure.media.TransformOutputBuiltinPresetArgs(
                    preset_name="AACGoodQualityAudio",
                ),
            )])
        input = azure.media.Asset("input",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            description="Input Asset description")
        output = azure.media.Asset("output",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            description="Output Asset description")
        example_job = azure.media.Job("exampleJob",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            transform_name=example_transform.name,
            description="My Job description",
            priority="Normal",
            input_asset=azure.media.JobInputAssetArgs(
                name=input.name,
            ),
            output_assets=[azure.media.JobOutputAssetArgs(
                name=output.name,
            )])
        ```

        ## Import

        Media Jobs can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:media/job:Job example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resGroup1/providers/Microsoft.Media/mediaservices/account1/transforms/transform1/jobs/job1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Optional customer supplied description of the Job.
        :param pulumi.Input[pulumi.InputType['JobInputAssetArgs']] input_asset: A `input_asset` block as defined below. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Transform to be created.
        :param pulumi.Input[str] name: The name which should be used for this Media Job. Changing this forces a new Media Job to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobOutputAssetArgs']]]] output_assets: One or more `output_asset` blocks as defined below. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] priority: Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Media Job should exist. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] transform_name: The Transform name. Changing this forces a new Media Job to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Media Job.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="GRS")
        example_service_account = azure.media.ServiceAccount("exampleServiceAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            storage_accounts=[azure.media.ServiceAccountStorageAccountArgs(
                id=example_account.id,
                is_primary=True,
            )])
        example_transform = azure.media.Transform("exampleTransform",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            description="My transform description",
            outputs=[azure.media.TransformOutputArgs(
                relative_priority="Normal",
                on_error_action="ContinueJob",
                builtin_preset=azure.media.TransformOutputBuiltinPresetArgs(
                    preset_name="AACGoodQualityAudio",
                ),
            )])
        input = azure.media.Asset("input",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            description="Input Asset description")
        output = azure.media.Asset("output",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            description="Output Asset description")
        example_job = azure.media.Job("exampleJob",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            transform_name=example_transform.name,
            description="My Job description",
            priority="Normal",
            input_asset=azure.media.JobInputAssetArgs(
                name=input.name,
            ),
            output_assets=[azure.media.JobOutputAssetArgs(
                name=output.name,
            )])
        ```

        ## Import

        Media Jobs can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:media/job:Job example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resGroup1/providers/Microsoft.Media/mediaservices/account1/transforms/transform1/jobs/job1
        ```

        :param str resource_name: The name of the resource.
        :param JobArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 input_asset: Optional[pulumi.Input[pulumi.InputType['JobInputAssetArgs']]] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_assets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobOutputAssetArgs']]]]] = None,
                 priority: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 transform_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = JobArgs.__new__(JobArgs)

            __props__.__dict__["description"] = description
            if input_asset is None and not opts.urn:
                raise TypeError("Missing required property 'input_asset'")
            __props__.__dict__["input_asset"] = input_asset
            if media_services_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'media_services_account_name'")
            __props__.__dict__["media_services_account_name"] = media_services_account_name
            __props__.__dict__["name"] = name
            if output_assets is None and not opts.urn:
                raise TypeError("Missing required property 'output_assets'")
            __props__.__dict__["output_assets"] = output_assets
            __props__.__dict__["priority"] = priority
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if transform_name is None and not opts.urn:
                raise TypeError("Missing required property 'transform_name'")
            __props__.__dict__["transform_name"] = transform_name
        super(Job, __self__).__init__(
            'azure:media/job:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            input_asset: Optional[pulumi.Input[pulumi.InputType['JobInputAssetArgs']]] = None,
            media_services_account_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            output_assets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobOutputAssetArgs']]]]] = None,
            priority: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            transform_name: Optional[pulumi.Input[str]] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Optional customer supplied description of the Job.
        :param pulumi.Input[pulumi.InputType['JobInputAssetArgs']] input_asset: A `input_asset` block as defined below. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Transform to be created.
        :param pulumi.Input[str] name: The name which should be used for this Media Job. Changing this forces a new Media Job to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobOutputAssetArgs']]]] output_assets: One or more `output_asset` blocks as defined below. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] priority: Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Media Job should exist. Changing this forces a new Media Job to be created.
        :param pulumi.Input[str] transform_name: The Transform name. Changing this forces a new Media Job to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _JobState.__new__(_JobState)

        __props__.__dict__["description"] = description
        __props__.__dict__["input_asset"] = input_asset
        __props__.__dict__["media_services_account_name"] = media_services_account_name
        __props__.__dict__["name"] = name
        __props__.__dict__["output_assets"] = output_assets
        __props__.__dict__["priority"] = priority
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["transform_name"] = transform_name
        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Optional customer supplied description of the Job.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="inputAsset")
    def input_asset(self) -> pulumi.Output['outputs.JobInputAsset']:
        """
        A `input_asset` block as defined below. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "input_asset")

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> pulumi.Output[str]:
        """
        The Media Services account name. Changing this forces a new Transform to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Media Job. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outputAssets")
    def output_assets(self) -> pulumi.Output[Sequence['outputs.JobOutputAsset']]:
        """
        One or more `output_asset` blocks as defined below. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "output_assets")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[Optional[str]]:
        """
        Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Media Job should exist. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="transformName")
    def transform_name(self) -> pulumi.Output[str]:
        """
        The Transform name. Changing this forces a new Media Job to be created.
        """
        return pulumi.get(self, "transform_name")

