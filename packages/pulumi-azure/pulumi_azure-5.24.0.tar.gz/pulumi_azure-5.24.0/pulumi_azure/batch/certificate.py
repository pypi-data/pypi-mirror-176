# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['CertificateArgs', 'Certificate']

@pulumi.input_type
class CertificateArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 certificate: pulumi.Input[str],
                 format: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 thumbprint: pulumi.Input[str],
                 thumbprint_algorithm: pulumi.Input[str],
                 password: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Certificate resource.
        :param pulumi.Input[str] account_name: Specifies the name of the Batch account. Changing this forces a new resource to be created.
        :param pulumi.Input[str] certificate: The base64-encoded contents of the certificate.
        :param pulumi.Input[str] format: The format of the certificate. Possible values are `Cer` or `Pfx`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Batch account. Changing this forces a new resource to be created.
        :param pulumi.Input[str] thumbprint: The thumbprint of the certificate. At this time the only supported value is 'SHA1'.
        :param pulumi.Input[str] password: The password to access the certificate's private key. This can only be specified when `format` is `Pfx`.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "certificate", certificate)
        pulumi.set(__self__, "format", format)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "thumbprint", thumbprint)
        pulumi.set(__self__, "thumbprint_algorithm", thumbprint_algorithm)
        if password is not None:
            pulumi.set(__self__, "password", password)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the Batch account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Input[str]:
        """
        The base64-encoded contents of the certificate.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter
    def format(self) -> pulumi.Input[str]:
        """
        The format of the certificate. Possible values are `Cer` or `Pfx`.
        """
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: pulumi.Input[str]):
        pulumi.set(self, "format", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the Batch account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def thumbprint(self) -> pulumi.Input[str]:
        """
        The thumbprint of the certificate. At this time the only supported value is 'SHA1'.
        """
        return pulumi.get(self, "thumbprint")

    @thumbprint.setter
    def thumbprint(self, value: pulumi.Input[str]):
        pulumi.set(self, "thumbprint", value)

    @property
    @pulumi.getter(name="thumbprintAlgorithm")
    def thumbprint_algorithm(self) -> pulumi.Input[str]:
        return pulumi.get(self, "thumbprint_algorithm")

    @thumbprint_algorithm.setter
    def thumbprint_algorithm(self, value: pulumi.Input[str]):
        pulumi.set(self, "thumbprint_algorithm", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password to access the certificate's private key. This can only be specified when `format` is `Pfx`.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)


@pulumi.input_type
class _CertificateState:
    def __init__(__self__, *,
                 account_name: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 public_data: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None,
                 thumbprint_algorithm: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Certificate resources.
        :param pulumi.Input[str] account_name: Specifies the name of the Batch account. Changing this forces a new resource to be created.
        :param pulumi.Input[str] certificate: The base64-encoded contents of the certificate.
        :param pulumi.Input[str] format: The format of the certificate. Possible values are `Cer` or `Pfx`.
        :param pulumi.Input[str] name: The generated name of the certificate.
        :param pulumi.Input[str] password: The password to access the certificate's private key. This can only be specified when `format` is `Pfx`.
        :param pulumi.Input[str] public_data: The public key of the certificate.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Batch account. Changing this forces a new resource to be created.
        :param pulumi.Input[str] thumbprint: The thumbprint of the certificate. At this time the only supported value is 'SHA1'.
        """
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if certificate is not None:
            pulumi.set(__self__, "certificate", certificate)
        if format is not None:
            pulumi.set(__self__, "format", format)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if public_data is not None:
            pulumi.set(__self__, "public_data", public_data)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if thumbprint is not None:
            pulumi.set(__self__, "thumbprint", thumbprint)
        if thumbprint_algorithm is not None:
            pulumi.set(__self__, "thumbprint_algorithm", thumbprint_algorithm)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Batch account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter
    def certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The base64-encoded contents of the certificate.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter
    def format(self) -> Optional[pulumi.Input[str]]:
        """
        The format of the certificate. Possible values are `Cer` or `Pfx`.
        """
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "format", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The generated name of the certificate.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password to access the certificate's private key. This can only be specified when `format` is `Pfx`.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="publicData")
    def public_data(self) -> Optional[pulumi.Input[str]]:
        """
        The public key of the certificate.
        """
        return pulumi.get(self, "public_data")

    @public_data.setter
    def public_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_data", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the Batch account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        The thumbprint of the certificate. At this time the only supported value is 'SHA1'.
        """
        return pulumi.get(self, "thumbprint")

    @thumbprint.setter
    def thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint", value)

    @property
    @pulumi.getter(name="thumbprintAlgorithm")
    def thumbprint_algorithm(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "thumbprint_algorithm")

    @thumbprint_algorithm.setter
    def thumbprint_algorithm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint_algorithm", value)


class Certificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None,
                 thumbprint_algorithm: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a certificate in an Azure Batch account.

        ## Example Usage

        ```python
        import pulumi
        import base64
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS")
        example_batch_account_account = azure.batch.Account("exampleBatch/accountAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            pool_allocation_mode="BatchService",
            storage_account_id=example_account.id,
            tags={
                "env": "test",
            })
        example_certificate = azure.batch.Certificate("exampleCertificate",
            resource_group_name=example_resource_group.name,
            account_name=example_batch / account_account["name"],
            certificate=(lambda path: base64.b64encode(open(path).read().encode()).decode())("certificate.pfx"),
            format="Pfx",
            password="password",
            thumbprint="42C107874FD0E4A9583292A2F1098E8FE4B2EDDA",
            thumbprint_algorithm="SHA1")
        ```

        ## Import

        Batch Certificates can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:batch/certificate:Certificate example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example-rg/providers/Microsoft.Batch/batchAccounts/batch1/certificates/certificate1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Specifies the name of the Batch account. Changing this forces a new resource to be created.
        :param pulumi.Input[str] certificate: The base64-encoded contents of the certificate.
        :param pulumi.Input[str] format: The format of the certificate. Possible values are `Cer` or `Pfx`.
        :param pulumi.Input[str] password: The password to access the certificate's private key. This can only be specified when `format` is `Pfx`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Batch account. Changing this forces a new resource to be created.
        :param pulumi.Input[str] thumbprint: The thumbprint of the certificate. At this time the only supported value is 'SHA1'.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a certificate in an Azure Batch account.

        ## Example Usage

        ```python
        import pulumi
        import base64
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS")
        example_batch_account_account = azure.batch.Account("exampleBatch/accountAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            pool_allocation_mode="BatchService",
            storage_account_id=example_account.id,
            tags={
                "env": "test",
            })
        example_certificate = azure.batch.Certificate("exampleCertificate",
            resource_group_name=example_resource_group.name,
            account_name=example_batch / account_account["name"],
            certificate=(lambda path: base64.b64encode(open(path).read().encode()).decode())("certificate.pfx"),
            format="Pfx",
            password="password",
            thumbprint="42C107874FD0E4A9583292A2F1098E8FE4B2EDDA",
            thumbprint_algorithm="SHA1")
        ```

        ## Import

        Batch Certificates can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:batch/certificate:Certificate example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example-rg/providers/Microsoft.Batch/batchAccounts/batch1/certificates/certificate1
        ```

        :param str resource_name: The name of the resource.
        :param CertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None,
                 thumbprint_algorithm: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CertificateArgs.__new__(CertificateArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            if certificate is None and not opts.urn:
                raise TypeError("Missing required property 'certificate'")
            __props__.__dict__["certificate"] = certificate
            if format is None and not opts.urn:
                raise TypeError("Missing required property 'format'")
            __props__.__dict__["format"] = format
            __props__.__dict__["password"] = password
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if thumbprint is None and not opts.urn:
                raise TypeError("Missing required property 'thumbprint'")
            __props__.__dict__["thumbprint"] = thumbprint
            if thumbprint_algorithm is None and not opts.urn:
                raise TypeError("Missing required property 'thumbprint_algorithm'")
            __props__.__dict__["thumbprint_algorithm"] = thumbprint_algorithm
            __props__.__dict__["name"] = None
            __props__.__dict__["public_data"] = None
        super(Certificate, __self__).__init__(
            'azure:batch/certificate:Certificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_name: Optional[pulumi.Input[str]] = None,
            certificate: Optional[pulumi.Input[str]] = None,
            format: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            public_data: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            thumbprint: Optional[pulumi.Input[str]] = None,
            thumbprint_algorithm: Optional[pulumi.Input[str]] = None) -> 'Certificate':
        """
        Get an existing Certificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Specifies the name of the Batch account. Changing this forces a new resource to be created.
        :param pulumi.Input[str] certificate: The base64-encoded contents of the certificate.
        :param pulumi.Input[str] format: The format of the certificate. Possible values are `Cer` or `Pfx`.
        :param pulumi.Input[str] name: The generated name of the certificate.
        :param pulumi.Input[str] password: The password to access the certificate's private key. This can only be specified when `format` is `Pfx`.
        :param pulumi.Input[str] public_data: The public key of the certificate.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Batch account. Changing this forces a new resource to be created.
        :param pulumi.Input[str] thumbprint: The thumbprint of the certificate. At this time the only supported value is 'SHA1'.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CertificateState.__new__(_CertificateState)

        __props__.__dict__["account_name"] = account_name
        __props__.__dict__["certificate"] = certificate
        __props__.__dict__["format"] = format
        __props__.__dict__["name"] = name
        __props__.__dict__["password"] = password
        __props__.__dict__["public_data"] = public_data
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["thumbprint"] = thumbprint
        __props__.__dict__["thumbprint_algorithm"] = thumbprint_algorithm
        return Certificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Batch account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Output[str]:
        """
        The base64-encoded contents of the certificate.
        """
        return pulumi.get(self, "certificate")

    @property
    @pulumi.getter
    def format(self) -> pulumi.Output[str]:
        """
        The format of the certificate. Possible values are `Cer` or `Pfx`.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The generated name of the certificate.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The password to access the certificate's private key. This can only be specified when `format` is `Pfx`.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="publicData")
    def public_data(self) -> pulumi.Output[str]:
        """
        The public key of the certificate.
        """
        return pulumi.get(self, "public_data")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the Batch account. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def thumbprint(self) -> pulumi.Output[str]:
        """
        The thumbprint of the certificate. At this time the only supported value is 'SHA1'.
        """
        return pulumi.get(self, "thumbprint")

    @property
    @pulumi.getter(name="thumbprintAlgorithm")
    def thumbprint_algorithm(self) -> pulumi.Output[str]:
        return pulumi.get(self, "thumbprint_algorithm")

