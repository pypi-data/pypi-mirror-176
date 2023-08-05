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

__all__ = ['ContentKeyPolicyArgs', 'ContentKeyPolicy']

@pulumi.input_type
class ContentKeyPolicyArgs:
    def __init__(__self__, *,
                 media_services_account_name: pulumi.Input[str],
                 policy_options: pulumi.Input[Sequence[pulumi.Input['ContentKeyPolicyPolicyOptionArgs']]],
                 resource_group_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ContentKeyPolicy resource.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Content Key Policy to be created.
        :param pulumi.Input[Sequence[pulumi.Input['ContentKeyPolicyPolicyOptionArgs']]] policy_options: One or more `policy_option` blocks as defined below.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Content Key Policy should exist. Changing this forces a new Content Key Policy to be created.
        :param pulumi.Input[str] description: A description for the Policy.
        :param pulumi.Input[str] name: The name which should be used for this Content Key Policy. Changing this forces a new Content Key Policy to be created.
        """
        pulumi.set(__self__, "media_services_account_name", media_services_account_name)
        pulumi.set(__self__, "policy_options", policy_options)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> pulumi.Input[str]:
        """
        The Media Services account name. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @media_services_account_name.setter
    def media_services_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "media_services_account_name", value)

    @property
    @pulumi.getter(name="policyOptions")
    def policy_options(self) -> pulumi.Input[Sequence[pulumi.Input['ContentKeyPolicyPolicyOptionArgs']]]:
        """
        One or more `policy_option` blocks as defined below.
        """
        return pulumi.get(self, "policy_options")

    @policy_options.setter
    def policy_options(self, value: pulumi.Input[Sequence[pulumi.Input['ContentKeyPolicyPolicyOptionArgs']]]):
        pulumi.set(self, "policy_options", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Content Key Policy should exist. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the Policy.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Content Key Policy. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ContentKeyPolicyState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_options: Optional[pulumi.Input[Sequence[pulumi.Input['ContentKeyPolicyPolicyOptionArgs']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ContentKeyPolicy resources.
        :param pulumi.Input[str] description: A description for the Policy.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Content Key Policy to be created.
        :param pulumi.Input[str] name: The name which should be used for this Content Key Policy. Changing this forces a new Content Key Policy to be created.
        :param pulumi.Input[Sequence[pulumi.Input['ContentKeyPolicyPolicyOptionArgs']]] policy_options: One or more `policy_option` blocks as defined below.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Content Key Policy should exist. Changing this forces a new Content Key Policy to be created.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if media_services_account_name is not None:
            pulumi.set(__self__, "media_services_account_name", media_services_account_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy_options is not None:
            pulumi.set(__self__, "policy_options", policy_options)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the Policy.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Media Services account name. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @media_services_account_name.setter
    def media_services_account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "media_services_account_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Content Key Policy. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="policyOptions")
    def policy_options(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ContentKeyPolicyPolicyOptionArgs']]]]:
        """
        One or more `policy_option` blocks as defined below.
        """
        return pulumi.get(self, "policy_options")

    @policy_options.setter
    def policy_options(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ContentKeyPolicyPolicyOptionArgs']]]]):
        pulumi.set(self, "policy_options", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Content Key Policy should exist. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)


class ContentKeyPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_options: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContentKeyPolicyPolicyOptionArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Content Key Policy.

        ## Example Usage

        ```python
        import pulumi
        import json
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
        example_content_key_policy = azure.media.ContentKeyPolicy("exampleContentKeyPolicy",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            policy_options=[
                azure.media.ContentKeyPolicyPolicyOptionArgs(
                    name="fairPlay",
                    fairplay_configuration=azure.media.ContentKeyPolicyPolicyOptionFairplayConfigurationArgs(
                        ask="bb566284cc124a21c435a92cd3c108c4",
                        pfx="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",
                        pfx_password="password",
                        rental_duration_seconds=2249,
                        rental_and_lease_key_type="PersistentUnlimited",
                    ),
                    open_restriction_enabled=True,
                ),
                azure.media.ContentKeyPolicyPolicyOptionArgs(
                    name="playReady",
                    playready_configuration_licenses=[azure.media.ContentKeyPolicyPolicyOptionPlayreadyConfigurationLicenseArgs(
                        allow_test_devices=True,
                        begin_date="2017-10-16T18:22:53Z",
                        play_right=azure.media.ContentKeyPolicyPolicyOptionPlayreadyConfigurationLicensePlayRightArgs(
                            scms_restriction=2,
                            digital_video_only_content_restriction=False,
                            image_constraint_for_analog_component_video_restriction=False,
                            image_constraint_for_analog_computer_monitor_restriction=False,
                            allow_passing_video_content_to_unknown_output="NotAllowed",
                            uncompressed_digital_video_opl=100,
                            uncompressed_digital_audio_opl=100,
                            analog_video_opl=150,
                            compressed_digital_audio_opl=150,
                        ),
                        license_type="Persistent",
                        content_type="UltraVioletDownload",
                        content_key_location_from_header_enabled=True,
                    )],
                    open_restriction_enabled=True,
                ),
                azure.media.ContentKeyPolicyPolicyOptionArgs(
                    name="clearKey",
                    clear_key_configuration_enabled=True,
                    token_restriction=azure.media.ContentKeyPolicyPolicyOptionTokenRestrictionArgs(
                        issuer="urn:issuer",
                        audience="urn:audience",
                        token_type="Swt",
                        primary_symmetric_token_key="AAAAAAAAAAAAAAAAAAAAAA==",
                    ),
                ),
                azure.media.ContentKeyPolicyPolicyOptionArgs(
                    name="widevine",
                    widevine_configuration_template=json.dumps({
                        "allowed_track_types": "SD_HD",
                        "content_key_specs": [{
                            "track_type": "SD",
                            "security_level": 1,
                            "required_output_protection": {
                                "hdcp": "HDCP_V2",
                            },
                        }],
                        "policy_overrides": {
                            "can_play": True,
                            "can_persist": True,
                            "can_renew": False,
                        },
                    }),
                    open_restriction_enabled=True,
                ),
            ])
        ```

        ## Import

        Resource Groups can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:media/contentKeyPolicy:ContentKeyPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Media/mediaservices/account1/contentkeypolicies/policy1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description for the Policy.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Content Key Policy to be created.
        :param pulumi.Input[str] name: The name which should be used for this Content Key Policy. Changing this forces a new Content Key Policy to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContentKeyPolicyPolicyOptionArgs']]]] policy_options: One or more `policy_option` blocks as defined below.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Content Key Policy should exist. Changing this forces a new Content Key Policy to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContentKeyPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Content Key Policy.

        ## Example Usage

        ```python
        import pulumi
        import json
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
        example_content_key_policy = azure.media.ContentKeyPolicy("exampleContentKeyPolicy",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            policy_options=[
                azure.media.ContentKeyPolicyPolicyOptionArgs(
                    name="fairPlay",
                    fairplay_configuration=azure.media.ContentKeyPolicyPolicyOptionFairplayConfigurationArgs(
                        ask="bb566284cc124a21c435a92cd3c108c4",
                        pfx="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",
                        pfx_password="password",
                        rental_duration_seconds=2249,
                        rental_and_lease_key_type="PersistentUnlimited",
                    ),
                    open_restriction_enabled=True,
                ),
                azure.media.ContentKeyPolicyPolicyOptionArgs(
                    name="playReady",
                    playready_configuration_licenses=[azure.media.ContentKeyPolicyPolicyOptionPlayreadyConfigurationLicenseArgs(
                        allow_test_devices=True,
                        begin_date="2017-10-16T18:22:53Z",
                        play_right=azure.media.ContentKeyPolicyPolicyOptionPlayreadyConfigurationLicensePlayRightArgs(
                            scms_restriction=2,
                            digital_video_only_content_restriction=False,
                            image_constraint_for_analog_component_video_restriction=False,
                            image_constraint_for_analog_computer_monitor_restriction=False,
                            allow_passing_video_content_to_unknown_output="NotAllowed",
                            uncompressed_digital_video_opl=100,
                            uncompressed_digital_audio_opl=100,
                            analog_video_opl=150,
                            compressed_digital_audio_opl=150,
                        ),
                        license_type="Persistent",
                        content_type="UltraVioletDownload",
                        content_key_location_from_header_enabled=True,
                    )],
                    open_restriction_enabled=True,
                ),
                azure.media.ContentKeyPolicyPolicyOptionArgs(
                    name="clearKey",
                    clear_key_configuration_enabled=True,
                    token_restriction=azure.media.ContentKeyPolicyPolicyOptionTokenRestrictionArgs(
                        issuer="urn:issuer",
                        audience="urn:audience",
                        token_type="Swt",
                        primary_symmetric_token_key="AAAAAAAAAAAAAAAAAAAAAA==",
                    ),
                ),
                azure.media.ContentKeyPolicyPolicyOptionArgs(
                    name="widevine",
                    widevine_configuration_template=json.dumps({
                        "allowed_track_types": "SD_HD",
                        "content_key_specs": [{
                            "track_type": "SD",
                            "security_level": 1,
                            "required_output_protection": {
                                "hdcp": "HDCP_V2",
                            },
                        }],
                        "policy_overrides": {
                            "can_play": True,
                            "can_persist": True,
                            "can_renew": False,
                        },
                    }),
                    open_restriction_enabled=True,
                ),
            ])
        ```

        ## Import

        Resource Groups can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:media/contentKeyPolicy:ContentKeyPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Media/mediaservices/account1/contentkeypolicies/policy1
        ```

        :param str resource_name: The name of the resource.
        :param ContentKeyPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContentKeyPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_options: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContentKeyPolicyPolicyOptionArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContentKeyPolicyArgs.__new__(ContentKeyPolicyArgs)

            __props__.__dict__["description"] = description
            if media_services_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'media_services_account_name'")
            __props__.__dict__["media_services_account_name"] = media_services_account_name
            __props__.__dict__["name"] = name
            if policy_options is None and not opts.urn:
                raise TypeError("Missing required property 'policy_options'")
            __props__.__dict__["policy_options"] = policy_options
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
        super(ContentKeyPolicy, __self__).__init__(
            'azure:media/contentKeyPolicy:ContentKeyPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            media_services_account_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            policy_options: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContentKeyPolicyPolicyOptionArgs']]]]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None) -> 'ContentKeyPolicy':
        """
        Get an existing ContentKeyPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description for the Policy.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Content Key Policy to be created.
        :param pulumi.Input[str] name: The name which should be used for this Content Key Policy. Changing this forces a new Content Key Policy to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContentKeyPolicyPolicyOptionArgs']]]] policy_options: One or more `policy_option` blocks as defined below.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Content Key Policy should exist. Changing this forces a new Content Key Policy to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ContentKeyPolicyState.__new__(_ContentKeyPolicyState)

        __props__.__dict__["description"] = description
        __props__.__dict__["media_services_account_name"] = media_services_account_name
        __props__.__dict__["name"] = name
        __props__.__dict__["policy_options"] = policy_options
        __props__.__dict__["resource_group_name"] = resource_group_name
        return ContentKeyPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description for the Policy.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> pulumi.Output[str]:
        """
        The Media Services account name. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Content Key Policy. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyOptions")
    def policy_options(self) -> pulumi.Output[Sequence['outputs.ContentKeyPolicyPolicyOption']]:
        """
        One or more `policy_option` blocks as defined below.
        """
        return pulumi.get(self, "policy_options")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Content Key Policy should exist. Changing this forces a new Content Key Policy to be created.
        """
        return pulumi.get(self, "resource_group_name")

