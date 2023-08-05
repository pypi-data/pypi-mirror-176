# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ZipBlobArgs', 'ZipBlob']

@pulumi.input_type
class ZipBlobArgs:
    def __init__(__self__, *,
                 storage_account_name: pulumi.Input[str],
                 storage_container_name: pulumi.Input[str],
                 type: pulumi.Input[str],
                 access_tier: Optional[pulumi.Input[str]] = None,
                 cache_control: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[pulumi.Archive]] = None,
                 content_md5: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parallelism: Optional[pulumi.Input[int]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 source_content: Optional[pulumi.Input[str]] = None,
                 source_uri: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ZipBlob resource.
        """
        pulumi.set(__self__, "storage_account_name", storage_account_name)
        pulumi.set(__self__, "storage_container_name", storage_container_name)
        pulumi.set(__self__, "type", type)
        if access_tier is not None:
            pulumi.set(__self__, "access_tier", access_tier)
        if cache_control is not None:
            pulumi.set(__self__, "cache_control", cache_control)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if content_md5 is not None:
            pulumi.set(__self__, "content_md5", content_md5)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parallelism is not None:
            pulumi.set(__self__, "parallelism", parallelism)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if source_content is not None:
            pulumi.set(__self__, "source_content", source_content)
        if source_uri is not None:
            pulumi.set(__self__, "source_uri", source_uri)

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "storage_account_name")

    @storage_account_name.setter
    def storage_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_account_name", value)

    @property
    @pulumi.getter(name="storageContainerName")
    def storage_container_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "storage_container_name")

    @storage_container_name.setter
    def storage_container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_container_name", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="accessTier")
    def access_tier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "access_tier")

    @access_tier.setter
    def access_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_tier", value)

    @property
    @pulumi.getter(name="cacheControl")
    def cache_control(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cache_control")

    @cache_control.setter
    def cache_control(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cache_control", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[pulumi.Archive]]:
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[pulumi.Archive]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="contentMd5")
    def content_md5(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content_md5")

    @content_md5.setter
    def content_md5(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_md5", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parallelism(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "parallelism")

    @parallelism.setter
    def parallelism(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "parallelism", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter(name="sourceContent")
    def source_content(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source_content")

    @source_content.setter
    def source_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_content", value)

    @property
    @pulumi.getter(name="sourceUri")
    def source_uri(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source_uri")

    @source_uri.setter
    def source_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_uri", value)


@pulumi.input_type
class _ZipBlobState:
    def __init__(__self__, *,
                 access_tier: Optional[pulumi.Input[str]] = None,
                 cache_control: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[pulumi.Archive]] = None,
                 content_md5: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parallelism: Optional[pulumi.Input[int]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 source_content: Optional[pulumi.Input[str]] = None,
                 source_uri: Optional[pulumi.Input[str]] = None,
                 storage_account_name: Optional[pulumi.Input[str]] = None,
                 storage_container_name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ZipBlob resources.
        """
        if access_tier is not None:
            pulumi.set(__self__, "access_tier", access_tier)
        if cache_control is not None:
            pulumi.set(__self__, "cache_control", cache_control)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if content_md5 is not None:
            pulumi.set(__self__, "content_md5", content_md5)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parallelism is not None:
            pulumi.set(__self__, "parallelism", parallelism)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if source_content is not None:
            pulumi.set(__self__, "source_content", source_content)
        if source_uri is not None:
            pulumi.set(__self__, "source_uri", source_uri)
        if storage_account_name is not None:
            pulumi.set(__self__, "storage_account_name", storage_account_name)
        if storage_container_name is not None:
            pulumi.set(__self__, "storage_container_name", storage_container_name)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="accessTier")
    def access_tier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "access_tier")

    @access_tier.setter
    def access_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_tier", value)

    @property
    @pulumi.getter(name="cacheControl")
    def cache_control(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cache_control")

    @cache_control.setter
    def cache_control(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cache_control", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[pulumi.Archive]]:
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[pulumi.Archive]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="contentMd5")
    def content_md5(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content_md5")

    @content_md5.setter
    def content_md5(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_md5", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parallelism(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "parallelism")

    @parallelism.setter
    def parallelism(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "parallelism", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter(name="sourceContent")
    def source_content(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source_content")

    @source_content.setter
    def source_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_content", value)

    @property
    @pulumi.getter(name="sourceUri")
    def source_uri(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source_uri")

    @source_uri.setter
    def source_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_uri", value)

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "storage_account_name")

    @storage_account_name.setter
    def storage_account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_name", value)

    @property
    @pulumi.getter(name="storageContainerName")
    def storage_container_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "storage_container_name")

    @storage_container_name.setter
    def storage_container_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_container_name", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


warnings.warn("""ZipBlob resource is deprecated in the 2.0 version of the provider. Use Blob resource instead.""", DeprecationWarning)


class ZipBlob(pulumi.CustomResource):
    warnings.warn("""ZipBlob resource is deprecated in the 2.0 version of the provider. Use Blob resource instead.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_tier: Optional[pulumi.Input[str]] = None,
                 cache_control: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[pulumi.Archive]] = None,
                 content_md5: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parallelism: Optional[pulumi.Input[int]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 source_content: Optional[pulumi.Input[str]] = None,
                 source_uri: Optional[pulumi.Input[str]] = None,
                 storage_account_name: Optional[pulumi.Input[str]] = None,
                 storage_container_name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a ZipBlob resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ZipBlobArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a ZipBlob resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param ZipBlobArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ZipBlobArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_tier: Optional[pulumi.Input[str]] = None,
                 cache_control: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[pulumi.Archive]] = None,
                 content_md5: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parallelism: Optional[pulumi.Input[int]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 source_content: Optional[pulumi.Input[str]] = None,
                 source_uri: Optional[pulumi.Input[str]] = None,
                 storage_account_name: Optional[pulumi.Input[str]] = None,
                 storage_container_name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""ZipBlob is deprecated: ZipBlob resource is deprecated in the 2.0 version of the provider. Use Blob resource instead.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ZipBlobArgs.__new__(ZipBlobArgs)

            __props__.__dict__["access_tier"] = access_tier
            __props__.__dict__["cache_control"] = cache_control
            __props__.__dict__["content"] = content
            __props__.__dict__["content_md5"] = content_md5
            __props__.__dict__["content_type"] = content_type
            __props__.__dict__["metadata"] = metadata
            __props__.__dict__["name"] = name
            __props__.__dict__["parallelism"] = parallelism
            __props__.__dict__["size"] = size
            __props__.__dict__["source_content"] = source_content
            __props__.__dict__["source_uri"] = source_uri
            if storage_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_account_name'")
            __props__.__dict__["storage_account_name"] = storage_account_name
            if storage_container_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_container_name'")
            __props__.__dict__["storage_container_name"] = storage_container_name
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["url"] = None
        super(ZipBlob, __self__).__init__(
            'azure:storage/zipBlob:ZipBlob',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_tier: Optional[pulumi.Input[str]] = None,
            cache_control: Optional[pulumi.Input[str]] = None,
            content: Optional[pulumi.Input[pulumi.Archive]] = None,
            content_md5: Optional[pulumi.Input[str]] = None,
            content_type: Optional[pulumi.Input[str]] = None,
            metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            parallelism: Optional[pulumi.Input[int]] = None,
            size: Optional[pulumi.Input[int]] = None,
            source_content: Optional[pulumi.Input[str]] = None,
            source_uri: Optional[pulumi.Input[str]] = None,
            storage_account_name: Optional[pulumi.Input[str]] = None,
            storage_container_name: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            url: Optional[pulumi.Input[str]] = None) -> 'ZipBlob':
        """
        Get an existing ZipBlob resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ZipBlobState.__new__(_ZipBlobState)

        __props__.__dict__["access_tier"] = access_tier
        __props__.__dict__["cache_control"] = cache_control
        __props__.__dict__["content"] = content
        __props__.__dict__["content_md5"] = content_md5
        __props__.__dict__["content_type"] = content_type
        __props__.__dict__["metadata"] = metadata
        __props__.__dict__["name"] = name
        __props__.__dict__["parallelism"] = parallelism
        __props__.__dict__["size"] = size
        __props__.__dict__["source_content"] = source_content
        __props__.__dict__["source_uri"] = source_uri
        __props__.__dict__["storage_account_name"] = storage_account_name
        __props__.__dict__["storage_container_name"] = storage_container_name
        __props__.__dict__["type"] = type
        __props__.__dict__["url"] = url
        return ZipBlob(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessTier")
    def access_tier(self) -> pulumi.Output[str]:
        return pulumi.get(self, "access_tier")

    @property
    @pulumi.getter(name="cacheControl")
    def cache_control(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "cache_control")

    @property
    @pulumi.getter
    def content(self) -> pulumi.Output[Optional[pulumi.Archive]]:
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="contentMd5")
    def content_md5(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "content_md5")

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parallelism(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "parallelism")

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "size")

    @property
    @pulumi.getter(name="sourceContent")
    def source_content(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "source_content")

    @property
    @pulumi.getter(name="sourceUri")
    def source_uri(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "source_uri")

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "storage_account_name")

    @property
    @pulumi.getter(name="storageContainerName")
    def storage_container_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "storage_container_name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        return pulumi.get(self, "url")

