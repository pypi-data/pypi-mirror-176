# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RedisCacheArgs', 'RedisCache']

@pulumi.input_type
class RedisCacheArgs:
    def __init__(__self__, *,
                 api_management_id: pulumi.Input[str],
                 connection_string: pulumi.Input[str],
                 cache_location: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 redis_cache_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RedisCache resource.
        :param pulumi.Input[str] api_management_id: The resource ID of the API Management Service from which to create this external cache. Changing this forces a new API Management Redis Cache to be created.
        :param pulumi.Input[str] connection_string: The connection string to the Cache for Redis.
        :param pulumi.Input[str] cache_location: The location where to use cache from. Possible values are `default` and valid Azure regions. Defaults to `default`.
        :param pulumi.Input[str] description: The description of the API Management Redis Cache.
        :param pulumi.Input[str] name: The name which should be used for this API Management Redis Cache. Changing this forces a new API Management Redis Cache to be created.
        :param pulumi.Input[str] redis_cache_id: The resource ID of the Cache for Redis.
        """
        pulumi.set(__self__, "api_management_id", api_management_id)
        pulumi.set(__self__, "connection_string", connection_string)
        if cache_location is not None:
            pulumi.set(__self__, "cache_location", cache_location)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if redis_cache_id is not None:
            pulumi.set(__self__, "redis_cache_id", redis_cache_id)

    @property
    @pulumi.getter(name="apiManagementId")
    def api_management_id(self) -> pulumi.Input[str]:
        """
        The resource ID of the API Management Service from which to create this external cache. Changing this forces a new API Management Redis Cache to be created.
        """
        return pulumi.get(self, "api_management_id")

    @api_management_id.setter
    def api_management_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_management_id", value)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> pulumi.Input[str]:
        """
        The connection string to the Cache for Redis.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: pulumi.Input[str]):
        pulumi.set(self, "connection_string", value)

    @property
    @pulumi.getter(name="cacheLocation")
    def cache_location(self) -> Optional[pulumi.Input[str]]:
        """
        The location where to use cache from. Possible values are `default` and valid Azure regions. Defaults to `default`.
        """
        return pulumi.get(self, "cache_location")

    @cache_location.setter
    def cache_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cache_location", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the API Management Redis Cache.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this API Management Redis Cache. Changing this forces a new API Management Redis Cache to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="redisCacheId")
    def redis_cache_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource ID of the Cache for Redis.
        """
        return pulumi.get(self, "redis_cache_id")

    @redis_cache_id.setter
    def redis_cache_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "redis_cache_id", value)


@pulumi.input_type
class _RedisCacheState:
    def __init__(__self__, *,
                 api_management_id: Optional[pulumi.Input[str]] = None,
                 cache_location: Optional[pulumi.Input[str]] = None,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 redis_cache_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RedisCache resources.
        :param pulumi.Input[str] api_management_id: The resource ID of the API Management Service from which to create this external cache. Changing this forces a new API Management Redis Cache to be created.
        :param pulumi.Input[str] cache_location: The location where to use cache from. Possible values are `default` and valid Azure regions. Defaults to `default`.
        :param pulumi.Input[str] connection_string: The connection string to the Cache for Redis.
        :param pulumi.Input[str] description: The description of the API Management Redis Cache.
        :param pulumi.Input[str] name: The name which should be used for this API Management Redis Cache. Changing this forces a new API Management Redis Cache to be created.
        :param pulumi.Input[str] redis_cache_id: The resource ID of the Cache for Redis.
        """
        if api_management_id is not None:
            pulumi.set(__self__, "api_management_id", api_management_id)
        if cache_location is not None:
            pulumi.set(__self__, "cache_location", cache_location)
        if connection_string is not None:
            pulumi.set(__self__, "connection_string", connection_string)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if redis_cache_id is not None:
            pulumi.set(__self__, "redis_cache_id", redis_cache_id)

    @property
    @pulumi.getter(name="apiManagementId")
    def api_management_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource ID of the API Management Service from which to create this external cache. Changing this forces a new API Management Redis Cache to be created.
        """
        return pulumi.get(self, "api_management_id")

    @api_management_id.setter
    def api_management_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_management_id", value)

    @property
    @pulumi.getter(name="cacheLocation")
    def cache_location(self) -> Optional[pulumi.Input[str]]:
        """
        The location where to use cache from. Possible values are `default` and valid Azure regions. Defaults to `default`.
        """
        return pulumi.get(self, "cache_location")

    @cache_location.setter
    def cache_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cache_location", value)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        The connection string to the Cache for Redis.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_string", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the API Management Redis Cache.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this API Management Redis Cache. Changing this forces a new API Management Redis Cache to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="redisCacheId")
    def redis_cache_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource ID of the Cache for Redis.
        """
        return pulumi.get(self, "redis_cache_id")

    @redis_cache_id.setter
    def redis_cache_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "redis_cache_id", value)


class RedisCache(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_id: Optional[pulumi.Input[str]] = None,
                 cache_location: Optional[pulumi.Input[str]] = None,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 redis_cache_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a API Management Redis Cache.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="pub1",
            publisher_email="pub1@email.com",
            sku_name="Consumption_0")
        example_cache = azure.redis.Cache("exampleCache",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            capacity=1,
            family="C",
            sku_name="Basic",
            enable_non_ssl_port=False,
            minimum_tls_version="1.2",
            redis_configuration=azure.redis.CacheRedisConfigurationArgs())
        example_redis_cache = azure.apimanagement.RedisCache("exampleRedisCache",
            api_management_id=example_service.id,
            connection_string=example_cache.primary_connection_string,
            description="Redis cache instances",
            redis_cache_id=example_cache.id,
            cache_location="East Us")
        ```

        ## Import

        API Management Redis Caches can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/redisCache:RedisCache example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ApiManagement/service/service1/caches/cache1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_id: The resource ID of the API Management Service from which to create this external cache. Changing this forces a new API Management Redis Cache to be created.
        :param pulumi.Input[str] cache_location: The location where to use cache from. Possible values are `default` and valid Azure regions. Defaults to `default`.
        :param pulumi.Input[str] connection_string: The connection string to the Cache for Redis.
        :param pulumi.Input[str] description: The description of the API Management Redis Cache.
        :param pulumi.Input[str] name: The name which should be used for this API Management Redis Cache. Changing this forces a new API Management Redis Cache to be created.
        :param pulumi.Input[str] redis_cache_id: The resource ID of the Cache for Redis.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RedisCacheArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a API Management Redis Cache.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="pub1",
            publisher_email="pub1@email.com",
            sku_name="Consumption_0")
        example_cache = azure.redis.Cache("exampleCache",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            capacity=1,
            family="C",
            sku_name="Basic",
            enable_non_ssl_port=False,
            minimum_tls_version="1.2",
            redis_configuration=azure.redis.CacheRedisConfigurationArgs())
        example_redis_cache = azure.apimanagement.RedisCache("exampleRedisCache",
            api_management_id=example_service.id,
            connection_string=example_cache.primary_connection_string,
            description="Redis cache instances",
            redis_cache_id=example_cache.id,
            cache_location="East Us")
        ```

        ## Import

        API Management Redis Caches can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/redisCache:RedisCache example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ApiManagement/service/service1/caches/cache1
        ```

        :param str resource_name: The name of the resource.
        :param RedisCacheArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RedisCacheArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_id: Optional[pulumi.Input[str]] = None,
                 cache_location: Optional[pulumi.Input[str]] = None,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 redis_cache_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RedisCacheArgs.__new__(RedisCacheArgs)

            if api_management_id is None and not opts.urn:
                raise TypeError("Missing required property 'api_management_id'")
            __props__.__dict__["api_management_id"] = api_management_id
            __props__.__dict__["cache_location"] = cache_location
            if connection_string is None and not opts.urn:
                raise TypeError("Missing required property 'connection_string'")
            __props__.__dict__["connection_string"] = connection_string
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["redis_cache_id"] = redis_cache_id
        super(RedisCache, __self__).__init__(
            'azure:apimanagement/redisCache:RedisCache',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_management_id: Optional[pulumi.Input[str]] = None,
            cache_location: Optional[pulumi.Input[str]] = None,
            connection_string: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            redis_cache_id: Optional[pulumi.Input[str]] = None) -> 'RedisCache':
        """
        Get an existing RedisCache resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_id: The resource ID of the API Management Service from which to create this external cache. Changing this forces a new API Management Redis Cache to be created.
        :param pulumi.Input[str] cache_location: The location where to use cache from. Possible values are `default` and valid Azure regions. Defaults to `default`.
        :param pulumi.Input[str] connection_string: The connection string to the Cache for Redis.
        :param pulumi.Input[str] description: The description of the API Management Redis Cache.
        :param pulumi.Input[str] name: The name which should be used for this API Management Redis Cache. Changing this forces a new API Management Redis Cache to be created.
        :param pulumi.Input[str] redis_cache_id: The resource ID of the Cache for Redis.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RedisCacheState.__new__(_RedisCacheState)

        __props__.__dict__["api_management_id"] = api_management_id
        __props__.__dict__["cache_location"] = cache_location
        __props__.__dict__["connection_string"] = connection_string
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["redis_cache_id"] = redis_cache_id
        return RedisCache(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiManagementId")
    def api_management_id(self) -> pulumi.Output[str]:
        """
        The resource ID of the API Management Service from which to create this external cache. Changing this forces a new API Management Redis Cache to be created.
        """
        return pulumi.get(self, "api_management_id")

    @property
    @pulumi.getter(name="cacheLocation")
    def cache_location(self) -> pulumi.Output[Optional[str]]:
        """
        The location where to use cache from. Possible values are `default` and valid Azure regions. Defaults to `default`.
        """
        return pulumi.get(self, "cache_location")

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> pulumi.Output[str]:
        """
        The connection string to the Cache for Redis.
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the API Management Redis Cache.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this API Management Redis Cache. Changing this forces a new API Management Redis Cache to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="redisCacheId")
    def redis_cache_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource ID of the Cache for Redis.
        """
        return pulumi.get(self, "redis_cache_id")

