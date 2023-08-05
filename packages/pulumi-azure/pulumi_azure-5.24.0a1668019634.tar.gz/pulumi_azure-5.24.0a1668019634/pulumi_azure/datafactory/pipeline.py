# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PipelineArgs', 'Pipeline']

@pulumi.input_type
class PipelineArgs:
    def __init__(__self__, *,
                 data_factory_id: pulumi.Input[str],
                 activities_json: Optional[pulumi.Input[str]] = None,
                 annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 concurrency: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 folder: Optional[pulumi.Input[str]] = None,
                 moniter_metrics_after_duration: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Pipeline resource.
        :param pulumi.Input[str] data_factory_id: The Data Factory ID in which to associate the Linked Service with. Changing this forces a new resource.
        :param pulumi.Input[str] activities_json: A JSON object that contains the activities that will be associated with the Data Factory Pipeline.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] annotations: List of tags that can be used for describing the Data Factory Pipeline.
        :param pulumi.Input[int] concurrency: The max number of concurrent runs for the Data Factory Pipeline. Must be between `1` and `50`.
        :param pulumi.Input[str] description: The description for the Data Factory Pipeline.
        :param pulumi.Input[str] folder: The folder that this Pipeline is in. If not specified, the Pipeline will appear at the root level.
        :param pulumi.Input[str] moniter_metrics_after_duration: The TimeSpan value after which an Azure Monitoring Metric is fired.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Pipeline. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/azure/data-factory/naming-rules) for all restrictions.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: A map of parameters to associate with the Data Factory Pipeline.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: A map of variables to associate with the Data Factory Pipeline.
        """
        pulumi.set(__self__, "data_factory_id", data_factory_id)
        if activities_json is not None:
            pulumi.set(__self__, "activities_json", activities_json)
        if annotations is not None:
            pulumi.set(__self__, "annotations", annotations)
        if concurrency is not None:
            pulumi.set(__self__, "concurrency", concurrency)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if folder is not None:
            pulumi.set(__self__, "folder", folder)
        if moniter_metrics_after_duration is not None:
            pulumi.set(__self__, "moniter_metrics_after_duration", moniter_metrics_after_duration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if variables is not None:
            pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter(name="dataFactoryId")
    def data_factory_id(self) -> pulumi.Input[str]:
        """
        The Data Factory ID in which to associate the Linked Service with. Changing this forces a new resource.
        """
        return pulumi.get(self, "data_factory_id")

    @data_factory_id.setter
    def data_factory_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_factory_id", value)

    @property
    @pulumi.getter(name="activitiesJson")
    def activities_json(self) -> Optional[pulumi.Input[str]]:
        """
        A JSON object that contains the activities that will be associated with the Data Factory Pipeline.
        """
        return pulumi.get(self, "activities_json")

    @activities_json.setter
    def activities_json(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "activities_json", value)

    @property
    @pulumi.getter
    def annotations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of tags that can be used for describing the Data Factory Pipeline.
        """
        return pulumi.get(self, "annotations")

    @annotations.setter
    def annotations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "annotations", value)

    @property
    @pulumi.getter
    def concurrency(self) -> Optional[pulumi.Input[int]]:
        """
        The max number of concurrent runs for the Data Factory Pipeline. Must be between `1` and `50`.
        """
        return pulumi.get(self, "concurrency")

    @concurrency.setter
    def concurrency(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "concurrency", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for the Data Factory Pipeline.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def folder(self) -> Optional[pulumi.Input[str]]:
        """
        The folder that this Pipeline is in. If not specified, the Pipeline will appear at the root level.
        """
        return pulumi.get(self, "folder")

    @folder.setter
    def folder(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "folder", value)

    @property
    @pulumi.getter(name="moniterMetricsAfterDuration")
    def moniter_metrics_after_duration(self) -> Optional[pulumi.Input[str]]:
        """
        The TimeSpan value after which an Azure Monitoring Metric is fired.
        """
        return pulumi.get(self, "moniter_metrics_after_duration")

    @moniter_metrics_after_duration.setter
    def moniter_metrics_after_duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "moniter_metrics_after_duration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Data Factory Pipeline. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/azure/data-factory/naming-rules) for all restrictions.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of parameters to associate with the Data Factory Pipeline.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter
    def variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of variables to associate with the Data Factory Pipeline.
        """
        return pulumi.get(self, "variables")

    @variables.setter
    def variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "variables", value)


@pulumi.input_type
class _PipelineState:
    def __init__(__self__, *,
                 activities_json: Optional[pulumi.Input[str]] = None,
                 annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 concurrency: Optional[pulumi.Input[int]] = None,
                 data_factory_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 folder: Optional[pulumi.Input[str]] = None,
                 moniter_metrics_after_duration: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Pipeline resources.
        :param pulumi.Input[str] activities_json: A JSON object that contains the activities that will be associated with the Data Factory Pipeline.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] annotations: List of tags that can be used for describing the Data Factory Pipeline.
        :param pulumi.Input[int] concurrency: The max number of concurrent runs for the Data Factory Pipeline. Must be between `1` and `50`.
        :param pulumi.Input[str] data_factory_id: The Data Factory ID in which to associate the Linked Service with. Changing this forces a new resource.
        :param pulumi.Input[str] description: The description for the Data Factory Pipeline.
        :param pulumi.Input[str] folder: The folder that this Pipeline is in. If not specified, the Pipeline will appear at the root level.
        :param pulumi.Input[str] moniter_metrics_after_duration: The TimeSpan value after which an Azure Monitoring Metric is fired.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Pipeline. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/azure/data-factory/naming-rules) for all restrictions.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: A map of parameters to associate with the Data Factory Pipeline.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: A map of variables to associate with the Data Factory Pipeline.
        """
        if activities_json is not None:
            pulumi.set(__self__, "activities_json", activities_json)
        if annotations is not None:
            pulumi.set(__self__, "annotations", annotations)
        if concurrency is not None:
            pulumi.set(__self__, "concurrency", concurrency)
        if data_factory_id is not None:
            pulumi.set(__self__, "data_factory_id", data_factory_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if folder is not None:
            pulumi.set(__self__, "folder", folder)
        if moniter_metrics_after_duration is not None:
            pulumi.set(__self__, "moniter_metrics_after_duration", moniter_metrics_after_duration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if variables is not None:
            pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter(name="activitiesJson")
    def activities_json(self) -> Optional[pulumi.Input[str]]:
        """
        A JSON object that contains the activities that will be associated with the Data Factory Pipeline.
        """
        return pulumi.get(self, "activities_json")

    @activities_json.setter
    def activities_json(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "activities_json", value)

    @property
    @pulumi.getter
    def annotations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of tags that can be used for describing the Data Factory Pipeline.
        """
        return pulumi.get(self, "annotations")

    @annotations.setter
    def annotations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "annotations", value)

    @property
    @pulumi.getter
    def concurrency(self) -> Optional[pulumi.Input[int]]:
        """
        The max number of concurrent runs for the Data Factory Pipeline. Must be between `1` and `50`.
        """
        return pulumi.get(self, "concurrency")

    @concurrency.setter
    def concurrency(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "concurrency", value)

    @property
    @pulumi.getter(name="dataFactoryId")
    def data_factory_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Data Factory ID in which to associate the Linked Service with. Changing this forces a new resource.
        """
        return pulumi.get(self, "data_factory_id")

    @data_factory_id.setter
    def data_factory_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_factory_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for the Data Factory Pipeline.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def folder(self) -> Optional[pulumi.Input[str]]:
        """
        The folder that this Pipeline is in. If not specified, the Pipeline will appear at the root level.
        """
        return pulumi.get(self, "folder")

    @folder.setter
    def folder(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "folder", value)

    @property
    @pulumi.getter(name="moniterMetricsAfterDuration")
    def moniter_metrics_after_duration(self) -> Optional[pulumi.Input[str]]:
        """
        The TimeSpan value after which an Azure Monitoring Metric is fired.
        """
        return pulumi.get(self, "moniter_metrics_after_duration")

    @moniter_metrics_after_duration.setter
    def moniter_metrics_after_duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "moniter_metrics_after_duration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Data Factory Pipeline. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/azure/data-factory/naming-rules) for all restrictions.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of parameters to associate with the Data Factory Pipeline.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter
    def variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of variables to associate with the Data Factory Pipeline.
        """
        return pulumi.get(self, "variables")

    @variables.setter
    def variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "variables", value)


class Pipeline(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 activities_json: Optional[pulumi.Input[str]] = None,
                 annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 concurrency: Optional[pulumi.Input[int]] = None,
                 data_factory_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 folder: Optional[pulumi.Input[str]] = None,
                 moniter_metrics_after_duration: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Pipeline inside a Azure Data Factory.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_factory = azure.datafactory.Factory("exampleFactory",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_pipeline = azure.datafactory.Pipeline("examplePipeline", data_factory_id=example_factory.id)
        ```
        ### With Activities

        ```python
        import pulumi
        import pulumi_azure as azure

        test = azure.datafactory.Pipeline("test",
            data_factory_id=azurerm_data_factory["test"]["id"],
            variables={
                "bob": "item1",
            },
            activities_json=\"\"\"[
            {
                "name": "Append variable1",
                "type": "AppendVariable",
                "dependsOn": [],
                "userProperties": [],
                "typeProperties": {
                  "variableName": "bob",
                  "value": "something"
                }
            }
        ]
        \"\"\")
        ```

        ## Import

        Data Factory Pipeline's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:datafactory/pipeline:Pipeline example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example/providers/Microsoft.DataFactory/factories/example/pipelines/example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] activities_json: A JSON object that contains the activities that will be associated with the Data Factory Pipeline.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] annotations: List of tags that can be used for describing the Data Factory Pipeline.
        :param pulumi.Input[int] concurrency: The max number of concurrent runs for the Data Factory Pipeline. Must be between `1` and `50`.
        :param pulumi.Input[str] data_factory_id: The Data Factory ID in which to associate the Linked Service with. Changing this forces a new resource.
        :param pulumi.Input[str] description: The description for the Data Factory Pipeline.
        :param pulumi.Input[str] folder: The folder that this Pipeline is in. If not specified, the Pipeline will appear at the root level.
        :param pulumi.Input[str] moniter_metrics_after_duration: The TimeSpan value after which an Azure Monitoring Metric is fired.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Pipeline. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/azure/data-factory/naming-rules) for all restrictions.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: A map of parameters to associate with the Data Factory Pipeline.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: A map of variables to associate with the Data Factory Pipeline.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PipelineArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Pipeline inside a Azure Data Factory.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_factory = azure.datafactory.Factory("exampleFactory",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_pipeline = azure.datafactory.Pipeline("examplePipeline", data_factory_id=example_factory.id)
        ```
        ### With Activities

        ```python
        import pulumi
        import pulumi_azure as azure

        test = azure.datafactory.Pipeline("test",
            data_factory_id=azurerm_data_factory["test"]["id"],
            variables={
                "bob": "item1",
            },
            activities_json=\"\"\"[
            {
                "name": "Append variable1",
                "type": "AppendVariable",
                "dependsOn": [],
                "userProperties": [],
                "typeProperties": {
                  "variableName": "bob",
                  "value": "something"
                }
            }
        ]
        \"\"\")
        ```

        ## Import

        Data Factory Pipeline's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:datafactory/pipeline:Pipeline example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example/providers/Microsoft.DataFactory/factories/example/pipelines/example
        ```

        :param str resource_name: The name of the resource.
        :param PipelineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PipelineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 activities_json: Optional[pulumi.Input[str]] = None,
                 annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 concurrency: Optional[pulumi.Input[int]] = None,
                 data_factory_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 folder: Optional[pulumi.Input[str]] = None,
                 moniter_metrics_after_duration: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PipelineArgs.__new__(PipelineArgs)

            __props__.__dict__["activities_json"] = activities_json
            __props__.__dict__["annotations"] = annotations
            __props__.__dict__["concurrency"] = concurrency
            if data_factory_id is None and not opts.urn:
                raise TypeError("Missing required property 'data_factory_id'")
            __props__.__dict__["data_factory_id"] = data_factory_id
            __props__.__dict__["description"] = description
            __props__.__dict__["folder"] = folder
            __props__.__dict__["moniter_metrics_after_duration"] = moniter_metrics_after_duration
            __props__.__dict__["name"] = name
            __props__.__dict__["parameters"] = parameters
            __props__.__dict__["variables"] = variables
        super(Pipeline, __self__).__init__(
            'azure:datafactory/pipeline:Pipeline',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            activities_json: Optional[pulumi.Input[str]] = None,
            annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            concurrency: Optional[pulumi.Input[int]] = None,
            data_factory_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            folder: Optional[pulumi.Input[str]] = None,
            moniter_metrics_after_duration: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Pipeline':
        """
        Get an existing Pipeline resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] activities_json: A JSON object that contains the activities that will be associated with the Data Factory Pipeline.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] annotations: List of tags that can be used for describing the Data Factory Pipeline.
        :param pulumi.Input[int] concurrency: The max number of concurrent runs for the Data Factory Pipeline. Must be between `1` and `50`.
        :param pulumi.Input[str] data_factory_id: The Data Factory ID in which to associate the Linked Service with. Changing this forces a new resource.
        :param pulumi.Input[str] description: The description for the Data Factory Pipeline.
        :param pulumi.Input[str] folder: The folder that this Pipeline is in. If not specified, the Pipeline will appear at the root level.
        :param pulumi.Input[str] moniter_metrics_after_duration: The TimeSpan value after which an Azure Monitoring Metric is fired.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Pipeline. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/azure/data-factory/naming-rules) for all restrictions.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: A map of parameters to associate with the Data Factory Pipeline.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: A map of variables to associate with the Data Factory Pipeline.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PipelineState.__new__(_PipelineState)

        __props__.__dict__["activities_json"] = activities_json
        __props__.__dict__["annotations"] = annotations
        __props__.__dict__["concurrency"] = concurrency
        __props__.__dict__["data_factory_id"] = data_factory_id
        __props__.__dict__["description"] = description
        __props__.__dict__["folder"] = folder
        __props__.__dict__["moniter_metrics_after_duration"] = moniter_metrics_after_duration
        __props__.__dict__["name"] = name
        __props__.__dict__["parameters"] = parameters
        __props__.__dict__["variables"] = variables
        return Pipeline(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="activitiesJson")
    def activities_json(self) -> pulumi.Output[Optional[str]]:
        """
        A JSON object that contains the activities that will be associated with the Data Factory Pipeline.
        """
        return pulumi.get(self, "activities_json")

    @property
    @pulumi.getter
    def annotations(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of tags that can be used for describing the Data Factory Pipeline.
        """
        return pulumi.get(self, "annotations")

    @property
    @pulumi.getter
    def concurrency(self) -> pulumi.Output[Optional[int]]:
        """
        The max number of concurrent runs for the Data Factory Pipeline. Must be between `1` and `50`.
        """
        return pulumi.get(self, "concurrency")

    @property
    @pulumi.getter(name="dataFactoryId")
    def data_factory_id(self) -> pulumi.Output[str]:
        """
        The Data Factory ID in which to associate the Linked Service with. Changing this forces a new resource.
        """
        return pulumi.get(self, "data_factory_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description for the Data Factory Pipeline.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def folder(self) -> pulumi.Output[Optional[str]]:
        """
        The folder that this Pipeline is in. If not specified, the Pipeline will appear at the root level.
        """
        return pulumi.get(self, "folder")

    @property
    @pulumi.getter(name="moniterMetricsAfterDuration")
    def moniter_metrics_after_duration(self) -> pulumi.Output[Optional[str]]:
        """
        The TimeSpan value after which an Azure Monitoring Metric is fired.
        """
        return pulumi.get(self, "moniter_metrics_after_duration")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Data Factory Pipeline. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/azure/data-factory/naming-rules) for all restrictions.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of parameters to associate with the Data Factory Pipeline.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def variables(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of variables to associate with the Data Factory Pipeline.
        """
        return pulumi.get(self, "variables")

