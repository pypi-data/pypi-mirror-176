# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SubscriptionTemplateDeploymentArgs', 'SubscriptionTemplateDeployment']

@pulumi.input_type
class SubscriptionTemplateDeploymentArgs:
    def __init__(__self__, *,
                 debug_level: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters_content: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_content: Optional[pulumi.Input[str]] = None,
                 template_spec_version_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SubscriptionTemplateDeployment resource.
        :param pulumi.Input[str] debug_level: The Debug Level which should be used for this Subscription Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        :param pulumi.Input[str] location: The Azure Region where the Subscription Template Deployment should exist. Changing this forces a new Subscription Template Deployment to be created.
        :param pulumi.Input[str] name: The name which should be used for this Subscription Template Deployment. Changing this forces a new Subscription Template Deployment to be created.
        :param pulumi.Input[str] parameters_content: The contents of the ARM Template parameters file - containing a JSON list of parameters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Subscription Template Deployment.
        :param pulumi.Input[str] template_content: The contents of the ARM Template which should be deployed into this Subscription.
        :param pulumi.Input[str] template_spec_version_id: The ID of the Template Spec Version to deploy into the Subscription. Cannot be specified with `template_content`.
        """
        if debug_level is not None:
            pulumi.set(__self__, "debug_level", debug_level)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parameters_content is not None:
            pulumi.set(__self__, "parameters_content", parameters_content)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if template_content is not None:
            pulumi.set(__self__, "template_content", template_content)
        if template_spec_version_id is not None:
            pulumi.set(__self__, "template_spec_version_id", template_spec_version_id)

    @property
    @pulumi.getter(name="debugLevel")
    def debug_level(self) -> Optional[pulumi.Input[str]]:
        """
        The Debug Level which should be used for this Subscription Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        """
        return pulumi.get(self, "debug_level")

    @debug_level.setter
    def debug_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "debug_level", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Subscription Template Deployment should exist. Changing this forces a new Subscription Template Deployment to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Subscription Template Deployment. Changing this forces a new Subscription Template Deployment to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="parametersContent")
    def parameters_content(self) -> Optional[pulumi.Input[str]]:
        """
        The contents of the ARM Template parameters file - containing a JSON list of parameters.
        """
        return pulumi.get(self, "parameters_content")

    @parameters_content.setter
    def parameters_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parameters_content", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Subscription Template Deployment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="templateContent")
    def template_content(self) -> Optional[pulumi.Input[str]]:
        """
        The contents of the ARM Template which should be deployed into this Subscription.
        """
        return pulumi.get(self, "template_content")

    @template_content.setter
    def template_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_content", value)

    @property
    @pulumi.getter(name="templateSpecVersionId")
    def template_spec_version_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Template Spec Version to deploy into the Subscription. Cannot be specified with `template_content`.
        """
        return pulumi.get(self, "template_spec_version_id")

    @template_spec_version_id.setter
    def template_spec_version_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_spec_version_id", value)


@pulumi.input_type
class _SubscriptionTemplateDeploymentState:
    def __init__(__self__, *,
                 debug_level: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_content: Optional[pulumi.Input[str]] = None,
                 parameters_content: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_content: Optional[pulumi.Input[str]] = None,
                 template_spec_version_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SubscriptionTemplateDeployment resources.
        :param pulumi.Input[str] debug_level: The Debug Level which should be used for this Subscription Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        :param pulumi.Input[str] location: The Azure Region where the Subscription Template Deployment should exist. Changing this forces a new Subscription Template Deployment to be created.
        :param pulumi.Input[str] name: The name which should be used for this Subscription Template Deployment. Changing this forces a new Subscription Template Deployment to be created.
        :param pulumi.Input[str] output_content: The JSON Content of the Outputs of the ARM Template Deployment.
        :param pulumi.Input[str] parameters_content: The contents of the ARM Template parameters file - containing a JSON list of parameters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Subscription Template Deployment.
        :param pulumi.Input[str] template_content: The contents of the ARM Template which should be deployed into this Subscription.
        :param pulumi.Input[str] template_spec_version_id: The ID of the Template Spec Version to deploy into the Subscription. Cannot be specified with `template_content`.
        """
        if debug_level is not None:
            pulumi.set(__self__, "debug_level", debug_level)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if output_content is not None:
            pulumi.set(__self__, "output_content", output_content)
        if parameters_content is not None:
            pulumi.set(__self__, "parameters_content", parameters_content)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if template_content is not None:
            pulumi.set(__self__, "template_content", template_content)
        if template_spec_version_id is not None:
            pulumi.set(__self__, "template_spec_version_id", template_spec_version_id)

    @property
    @pulumi.getter(name="debugLevel")
    def debug_level(self) -> Optional[pulumi.Input[str]]:
        """
        The Debug Level which should be used for this Subscription Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        """
        return pulumi.get(self, "debug_level")

    @debug_level.setter
    def debug_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "debug_level", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Subscription Template Deployment should exist. Changing this forces a new Subscription Template Deployment to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Subscription Template Deployment. Changing this forces a new Subscription Template Deployment to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="outputContent")
    def output_content(self) -> Optional[pulumi.Input[str]]:
        """
        The JSON Content of the Outputs of the ARM Template Deployment.
        """
        return pulumi.get(self, "output_content")

    @output_content.setter
    def output_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "output_content", value)

    @property
    @pulumi.getter(name="parametersContent")
    def parameters_content(self) -> Optional[pulumi.Input[str]]:
        """
        The contents of the ARM Template parameters file - containing a JSON list of parameters.
        """
        return pulumi.get(self, "parameters_content")

    @parameters_content.setter
    def parameters_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parameters_content", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Subscription Template Deployment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="templateContent")
    def template_content(self) -> Optional[pulumi.Input[str]]:
        """
        The contents of the ARM Template which should be deployed into this Subscription.
        """
        return pulumi.get(self, "template_content")

    @template_content.setter
    def template_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_content", value)

    @property
    @pulumi.getter(name="templateSpecVersionId")
    def template_spec_version_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Template Spec Version to deploy into the Subscription. Cannot be specified with `template_content`.
        """
        return pulumi.get(self, "template_spec_version_id")

    @template_spec_version_id.setter
    def template_spec_version_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_spec_version_id", value)


class SubscriptionTemplateDeployment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 debug_level: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters_content: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_content: Optional[pulumi.Input[str]] = None,
                 template_spec_version_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Subscription Template Deployment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.SubscriptionTemplateDeployment("example",
            location="West Europe",
            template_content=\"\"\" {
           "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
           "contentVersion": "1.0.0.0",
           "parameters": {},
           "variables": {},
           "resources": [
             {
               "type": "Microsoft.Resources/resourceGroups",
               "apiVersion": "2018-05-01",
               "location": "West Europe",
               "name": "some-resource-group",
               "properties": {}
             }
           ]
         }
         
        \"\"\")
        ```

        ## Import

        Subscription Template Deployments can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:core/subscriptionTemplateDeployment:SubscriptionTemplateDeployment example /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Resources/deployments/template1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] debug_level: The Debug Level which should be used for this Subscription Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        :param pulumi.Input[str] location: The Azure Region where the Subscription Template Deployment should exist. Changing this forces a new Subscription Template Deployment to be created.
        :param pulumi.Input[str] name: The name which should be used for this Subscription Template Deployment. Changing this forces a new Subscription Template Deployment to be created.
        :param pulumi.Input[str] parameters_content: The contents of the ARM Template parameters file - containing a JSON list of parameters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Subscription Template Deployment.
        :param pulumi.Input[str] template_content: The contents of the ARM Template which should be deployed into this Subscription.
        :param pulumi.Input[str] template_spec_version_id: The ID of the Template Spec Version to deploy into the Subscription. Cannot be specified with `template_content`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[SubscriptionTemplateDeploymentArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Subscription Template Deployment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.SubscriptionTemplateDeployment("example",
            location="West Europe",
            template_content=\"\"\" {
           "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
           "contentVersion": "1.0.0.0",
           "parameters": {},
           "variables": {},
           "resources": [
             {
               "type": "Microsoft.Resources/resourceGroups",
               "apiVersion": "2018-05-01",
               "location": "West Europe",
               "name": "some-resource-group",
               "properties": {}
             }
           ]
         }
         
        \"\"\")
        ```

        ## Import

        Subscription Template Deployments can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:core/subscriptionTemplateDeployment:SubscriptionTemplateDeployment example /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Resources/deployments/template1
        ```

        :param str resource_name: The name of the resource.
        :param SubscriptionTemplateDeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SubscriptionTemplateDeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 debug_level: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters_content: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_content: Optional[pulumi.Input[str]] = None,
                 template_spec_version_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SubscriptionTemplateDeploymentArgs.__new__(SubscriptionTemplateDeploymentArgs)

            __props__.__dict__["debug_level"] = debug_level
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["parameters_content"] = parameters_content
            __props__.__dict__["tags"] = tags
            __props__.__dict__["template_content"] = template_content
            __props__.__dict__["template_spec_version_id"] = template_spec_version_id
            __props__.__dict__["output_content"] = None
        super(SubscriptionTemplateDeployment, __self__).__init__(
            'azure:core/subscriptionTemplateDeployment:SubscriptionTemplateDeployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            debug_level: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            output_content: Optional[pulumi.Input[str]] = None,
            parameters_content: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            template_content: Optional[pulumi.Input[str]] = None,
            template_spec_version_id: Optional[pulumi.Input[str]] = None) -> 'SubscriptionTemplateDeployment':
        """
        Get an existing SubscriptionTemplateDeployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] debug_level: The Debug Level which should be used for this Subscription Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        :param pulumi.Input[str] location: The Azure Region where the Subscription Template Deployment should exist. Changing this forces a new Subscription Template Deployment to be created.
        :param pulumi.Input[str] name: The name which should be used for this Subscription Template Deployment. Changing this forces a new Subscription Template Deployment to be created.
        :param pulumi.Input[str] output_content: The JSON Content of the Outputs of the ARM Template Deployment.
        :param pulumi.Input[str] parameters_content: The contents of the ARM Template parameters file - containing a JSON list of parameters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Subscription Template Deployment.
        :param pulumi.Input[str] template_content: The contents of the ARM Template which should be deployed into this Subscription.
        :param pulumi.Input[str] template_spec_version_id: The ID of the Template Spec Version to deploy into the Subscription. Cannot be specified with `template_content`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SubscriptionTemplateDeploymentState.__new__(_SubscriptionTemplateDeploymentState)

        __props__.__dict__["debug_level"] = debug_level
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["output_content"] = output_content
        __props__.__dict__["parameters_content"] = parameters_content
        __props__.__dict__["tags"] = tags
        __props__.__dict__["template_content"] = template_content
        __props__.__dict__["template_spec_version_id"] = template_spec_version_id
        return SubscriptionTemplateDeployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="debugLevel")
    def debug_level(self) -> pulumi.Output[Optional[str]]:
        """
        The Debug Level which should be used for this Subscription Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        """
        return pulumi.get(self, "debug_level")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Subscription Template Deployment should exist. Changing this forces a new Subscription Template Deployment to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Subscription Template Deployment. Changing this forces a new Subscription Template Deployment to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outputContent")
    def output_content(self) -> pulumi.Output[str]:
        """
        The JSON Content of the Outputs of the ARM Template Deployment.
        """
        return pulumi.get(self, "output_content")

    @property
    @pulumi.getter(name="parametersContent")
    def parameters_content(self) -> pulumi.Output[str]:
        """
        The contents of the ARM Template parameters file - containing a JSON list of parameters.
        """
        return pulumi.get(self, "parameters_content")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Subscription Template Deployment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="templateContent")
    def template_content(self) -> pulumi.Output[str]:
        """
        The contents of the ARM Template which should be deployed into this Subscription.
        """
        return pulumi.get(self, "template_content")

    @property
    @pulumi.getter(name="templateSpecVersionId")
    def template_spec_version_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Template Spec Version to deploy into the Subscription. Cannot be specified with `template_content`.
        """
        return pulumi.get(self, "template_spec_version_id")

