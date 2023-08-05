# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SpringCloudAppMysqlAssociationArgs', 'SpringCloudAppMysqlAssociation']

@pulumi.input_type
class SpringCloudAppMysqlAssociationArgs:
    def __init__(__self__, *,
                 database_name: pulumi.Input[str],
                 mysql_server_id: pulumi.Input[str],
                 password: pulumi.Input[str],
                 spring_cloud_app_id: pulumi.Input[str],
                 username: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SpringCloudAppMysqlAssociation resource.
        :param pulumi.Input[str] database_name: Specifies the name of the MySQL Database which the Spring Cloud App should be associated with.
        :param pulumi.Input[str] mysql_server_id: Specifies the ID of the MySQL Server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: Specifies the password which should be used when connecting to the MySQL Database from the Spring Cloud App.
        :param pulumi.Input[str] spring_cloud_app_id: Specifies the ID of the Spring Cloud Application where this Association is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] username: Specifies the username which should be used when connecting to the MySQL Database from the Spring Cloud App.
        :param pulumi.Input[str] name: Specifies the name of the Spring Cloud Application Association. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "database_name", database_name)
        pulumi.set(__self__, "mysql_server_id", mysql_server_id)
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "spring_cloud_app_id", spring_cloud_app_id)
        pulumi.set(__self__, "username", username)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the MySQL Database which the Spring Cloud App should be associated with.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="mysqlServerId")
    def mysql_server_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the MySQL Server. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "mysql_server_id")

    @mysql_server_id.setter
    def mysql_server_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "mysql_server_id", value)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        """
        Specifies the password which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="springCloudAppId")
    def spring_cloud_app_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the Spring Cloud Application where this Association is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "spring_cloud_app_id")

    @spring_cloud_app_id.setter
    def spring_cloud_app_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "spring_cloud_app_id", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        Specifies the username which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Spring Cloud Application Association. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _SpringCloudAppMysqlAssociationState:
    def __init__(__self__, *,
                 database_name: Optional[pulumi.Input[str]] = None,
                 mysql_server_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 spring_cloud_app_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SpringCloudAppMysqlAssociation resources.
        :param pulumi.Input[str] database_name: Specifies the name of the MySQL Database which the Spring Cloud App should be associated with.
        :param pulumi.Input[str] mysql_server_id: Specifies the ID of the MySQL Server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Spring Cloud Application Association. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: Specifies the password which should be used when connecting to the MySQL Database from the Spring Cloud App.
        :param pulumi.Input[str] spring_cloud_app_id: Specifies the ID of the Spring Cloud Application where this Association is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] username: Specifies the username which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        if database_name is not None:
            pulumi.set(__self__, "database_name", database_name)
        if mysql_server_id is not None:
            pulumi.set(__self__, "mysql_server_id", mysql_server_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if spring_cloud_app_id is not None:
            pulumi.set(__self__, "spring_cloud_app_id", spring_cloud_app_id)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the MySQL Database which the Spring Cloud App should be associated with.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="mysqlServerId")
    def mysql_server_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the MySQL Server. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "mysql_server_id")

    @mysql_server_id.setter
    def mysql_server_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mysql_server_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Spring Cloud Application Association. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the password which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="springCloudAppId")
    def spring_cloud_app_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the Spring Cloud Application where this Association is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "spring_cloud_app_id")

    @spring_cloud_app_id.setter
    def spring_cloud_app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spring_cloud_app_id", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the username which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class SpringCloudAppMysqlAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 mysql_server_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 spring_cloud_app_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Associates a Spring Cloud Application with a MySQL Database.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_spring_cloud_service = azure.appplatform.SpringCloudService("exampleSpringCloudService",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location)
        example_spring_cloud_app = azure.appplatform.SpringCloudApp("exampleSpringCloudApp",
            resource_group_name=example_resource_group.name,
            service_name=example_spring_cloud_service.name)
        example_server = azure.mysql.Server("exampleServer",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            administrator_login="mysqladminun",
            administrator_login_password="H@Sh1CoR3!",
            sku_name="B_Gen5_2",
            storage_mb=5120,
            version="5.7",
            ssl_enforcement_enabled=True,
            ssl_minimal_tls_version_enforced="TLS1_2")
        example_database = azure.mysql.Database("exampleDatabase",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            charset="utf8",
            collation="utf8_unicode_ci")
        example_spring_cloud_app_mysql_association = azure.appplatform.SpringCloudAppMysqlAssociation("exampleSpringCloudAppMysqlAssociation",
            spring_cloud_app_id=example_spring_cloud_app.id,
            mysql_server_id=example_server.id,
            database_name=example_database.name,
            username=example_server.administrator_login,
            password=example_server.administrator_login_password)
        ```

        ## Import

        Spring Cloud Application MySQL Association can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appplatform/springCloudAppMysqlAssociation:SpringCloudAppMysqlAssociation example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourcegroup1/providers/Microsoft.AppPlatform/Spring/service1/apps/app1/bindings/bind1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_name: Specifies the name of the MySQL Database which the Spring Cloud App should be associated with.
        :param pulumi.Input[str] mysql_server_id: Specifies the ID of the MySQL Server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Spring Cloud Application Association. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: Specifies the password which should be used when connecting to the MySQL Database from the Spring Cloud App.
        :param pulumi.Input[str] spring_cloud_app_id: Specifies the ID of the Spring Cloud Application where this Association is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] username: Specifies the username which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SpringCloudAppMysqlAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Associates a Spring Cloud Application with a MySQL Database.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_spring_cloud_service = azure.appplatform.SpringCloudService("exampleSpringCloudService",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location)
        example_spring_cloud_app = azure.appplatform.SpringCloudApp("exampleSpringCloudApp",
            resource_group_name=example_resource_group.name,
            service_name=example_spring_cloud_service.name)
        example_server = azure.mysql.Server("exampleServer",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            administrator_login="mysqladminun",
            administrator_login_password="H@Sh1CoR3!",
            sku_name="B_Gen5_2",
            storage_mb=5120,
            version="5.7",
            ssl_enforcement_enabled=True,
            ssl_minimal_tls_version_enforced="TLS1_2")
        example_database = azure.mysql.Database("exampleDatabase",
            resource_group_name=example_resource_group.name,
            server_name=example_server.name,
            charset="utf8",
            collation="utf8_unicode_ci")
        example_spring_cloud_app_mysql_association = azure.appplatform.SpringCloudAppMysqlAssociation("exampleSpringCloudAppMysqlAssociation",
            spring_cloud_app_id=example_spring_cloud_app.id,
            mysql_server_id=example_server.id,
            database_name=example_database.name,
            username=example_server.administrator_login,
            password=example_server.administrator_login_password)
        ```

        ## Import

        Spring Cloud Application MySQL Association can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appplatform/springCloudAppMysqlAssociation:SpringCloudAppMysqlAssociation example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourcegroup1/providers/Microsoft.AppPlatform/Spring/service1/apps/app1/bindings/bind1
        ```

        :param str resource_name: The name of the resource.
        :param SpringCloudAppMysqlAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SpringCloudAppMysqlAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 mysql_server_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 spring_cloud_app_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SpringCloudAppMysqlAssociationArgs.__new__(SpringCloudAppMysqlAssociationArgs)

            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__.__dict__["database_name"] = database_name
            if mysql_server_id is None and not opts.urn:
                raise TypeError("Missing required property 'mysql_server_id'")
            __props__.__dict__["mysql_server_id"] = mysql_server_id
            __props__.__dict__["name"] = name
            if password is None and not opts.urn:
                raise TypeError("Missing required property 'password'")
            __props__.__dict__["password"] = password
            if spring_cloud_app_id is None and not opts.urn:
                raise TypeError("Missing required property 'spring_cloud_app_id'")
            __props__.__dict__["spring_cloud_app_id"] = spring_cloud_app_id
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
        super(SpringCloudAppMysqlAssociation, __self__).__init__(
            'azure:appplatform/springCloudAppMysqlAssociation:SpringCloudAppMysqlAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            database_name: Optional[pulumi.Input[str]] = None,
            mysql_server_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            spring_cloud_app_id: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'SpringCloudAppMysqlAssociation':
        """
        Get an existing SpringCloudAppMysqlAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_name: Specifies the name of the MySQL Database which the Spring Cloud App should be associated with.
        :param pulumi.Input[str] mysql_server_id: Specifies the ID of the MySQL Server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Spring Cloud Application Association. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: Specifies the password which should be used when connecting to the MySQL Database from the Spring Cloud App.
        :param pulumi.Input[str] spring_cloud_app_id: Specifies the ID of the Spring Cloud Application where this Association is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] username: Specifies the username which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SpringCloudAppMysqlAssociationState.__new__(_SpringCloudAppMysqlAssociationState)

        __props__.__dict__["database_name"] = database_name
        __props__.__dict__["mysql_server_id"] = mysql_server_id
        __props__.__dict__["name"] = name
        __props__.__dict__["password"] = password
        __props__.__dict__["spring_cloud_app_id"] = spring_cloud_app_id
        __props__.__dict__["username"] = username
        return SpringCloudAppMysqlAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the MySQL Database which the Spring Cloud App should be associated with.
        """
        return pulumi.get(self, "database_name")

    @property
    @pulumi.getter(name="mysqlServerId")
    def mysql_server_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the MySQL Server. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "mysql_server_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Spring Cloud Application Association. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        Specifies the password which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="springCloudAppId")
    def spring_cloud_app_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the Spring Cloud Application where this Association is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "spring_cloud_app_id")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        Specifies the username which should be used when connecting to the MySQL Database from the Spring Cloud App.
        """
        return pulumi.get(self, "username")

