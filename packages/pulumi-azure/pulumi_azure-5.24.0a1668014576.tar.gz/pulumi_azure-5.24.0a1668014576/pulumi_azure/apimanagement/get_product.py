# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetProductResult',
    'AwaitableGetProductResult',
    'get_product',
    'get_product_output',
]

@pulumi.output_type
class GetProductResult:
    """
    A collection of values returned by getProduct.
    """
    def __init__(__self__, api_management_name=None, approval_required=None, description=None, display_name=None, id=None, product_id=None, published=None, resource_group_name=None, subscription_required=None, subscriptions_limit=None, terms=None):
        if api_management_name and not isinstance(api_management_name, str):
            raise TypeError("Expected argument 'api_management_name' to be a str")
        pulumi.set(__self__, "api_management_name", api_management_name)
        if approval_required and not isinstance(approval_required, bool):
            raise TypeError("Expected argument 'approval_required' to be a bool")
        pulumi.set(__self__, "approval_required", approval_required)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if product_id and not isinstance(product_id, str):
            raise TypeError("Expected argument 'product_id' to be a str")
        pulumi.set(__self__, "product_id", product_id)
        if published and not isinstance(published, bool):
            raise TypeError("Expected argument 'published' to be a bool")
        pulumi.set(__self__, "published", published)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if subscription_required and not isinstance(subscription_required, bool):
            raise TypeError("Expected argument 'subscription_required' to be a bool")
        pulumi.set(__self__, "subscription_required", subscription_required)
        if subscriptions_limit and not isinstance(subscriptions_limit, int):
            raise TypeError("Expected argument 'subscriptions_limit' to be a int")
        pulumi.set(__self__, "subscriptions_limit", subscriptions_limit)
        if terms and not isinstance(terms, str):
            raise TypeError("Expected argument 'terms' to be a str")
        pulumi.set(__self__, "terms", terms)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> str:
        return pulumi.get(self, "api_management_name")

    @property
    @pulumi.getter(name="approvalRequired")
    def approval_required(self) -> bool:
        """
        Do subscribers need to be approved prior to being able to use the Product?
        """
        return pulumi.get(self, "approval_required")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of this Product, which may include HTML formatting tags.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The Display Name for this API Management Product.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> str:
        return pulumi.get(self, "product_id")

    @property
    @pulumi.getter
    def published(self) -> bool:
        """
        Is this Product Published?
        """
        return pulumi.get(self, "published")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="subscriptionRequired")
    def subscription_required(self) -> bool:
        """
        Is a Subscription required to access API's included in this Product?
        """
        return pulumi.get(self, "subscription_required")

    @property
    @pulumi.getter(name="subscriptionsLimit")
    def subscriptions_limit(self) -> int:
        """
        The number of subscriptions a user can have to this Product at the same time.
        """
        return pulumi.get(self, "subscriptions_limit")

    @property
    @pulumi.getter
    def terms(self) -> str:
        """
        Any Terms and Conditions for this Product, which must be accepted by Developers before they can begin the Subscription process.
        """
        return pulumi.get(self, "terms")


class AwaitableGetProductResult(GetProductResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProductResult(
            api_management_name=self.api_management_name,
            approval_required=self.approval_required,
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            product_id=self.product_id,
            published=self.published,
            resource_group_name=self.resource_group_name,
            subscription_required=self.subscription_required,
            subscriptions_limit=self.subscriptions_limit,
            terms=self.terms)


def get_product(api_management_name: Optional[str] = None,
                product_id: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProductResult:
    """
    Use this data source to access information about an existing API Management Product.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.apimanagement.get_product(product_id="my-product",
        api_management_name="example-apim",
        resource_group_name="search-service")
    pulumi.export("productTerms", example.terms)
    ```


    :param str api_management_name: The Name of the API Management Service in which this Product exists.
    :param str product_id: The Identifier for the API Management Product.
    :param str resource_group_name: The Name of the Resource Group in which the API Management Service exists.
    """
    __args__ = dict()
    __args__['apiManagementName'] = api_management_name
    __args__['productId'] = product_id
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:apimanagement/getProduct:getProduct', __args__, opts=opts, typ=GetProductResult).value

    return AwaitableGetProductResult(
        api_management_name=__ret__.api_management_name,
        approval_required=__ret__.approval_required,
        description=__ret__.description,
        display_name=__ret__.display_name,
        id=__ret__.id,
        product_id=__ret__.product_id,
        published=__ret__.published,
        resource_group_name=__ret__.resource_group_name,
        subscription_required=__ret__.subscription_required,
        subscriptions_limit=__ret__.subscriptions_limit,
        terms=__ret__.terms)


@_utilities.lift_output_func(get_product)
def get_product_output(api_management_name: Optional[pulumi.Input[str]] = None,
                       product_id: Optional[pulumi.Input[str]] = None,
                       resource_group_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProductResult]:
    """
    Use this data source to access information about an existing API Management Product.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.apimanagement.get_product(product_id="my-product",
        api_management_name="example-apim",
        resource_group_name="search-service")
    pulumi.export("productTerms", example.terms)
    ```


    :param str api_management_name: The Name of the API Management Service in which this Product exists.
    :param str product_id: The Identifier for the API Management Product.
    :param str resource_group_name: The Name of the Resource Group in which the API Management Service exists.
    """
    ...
