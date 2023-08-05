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

__all__ = [
    'GetPolicyAssignmentResult',
    'AwaitableGetPolicyAssignmentResult',
    'get_policy_assignment',
    'get_policy_assignment_output',
]

@pulumi.output_type
class GetPolicyAssignmentResult:
    """
    A collection of values returned by getPolicyAssignment.
    """
    def __init__(__self__, description=None, display_name=None, enforce=None, id=None, identities=None, location=None, metadata=None, name=None, non_compliance_messages=None, not_scopes=None, parameters=None, policy_definition_id=None, scope_id=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if enforce and not isinstance(enforce, bool):
            raise TypeError("Expected argument 'enforce' to be a bool")
        pulumi.set(__self__, "enforce", enforce)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        pulumi.set(__self__, "identities", identities)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if metadata and not isinstance(metadata, str):
            raise TypeError("Expected argument 'metadata' to be a str")
        pulumi.set(__self__, "metadata", metadata)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if non_compliance_messages and not isinstance(non_compliance_messages, list):
            raise TypeError("Expected argument 'non_compliance_messages' to be a list")
        pulumi.set(__self__, "non_compliance_messages", non_compliance_messages)
        if not_scopes and not isinstance(not_scopes, list):
            raise TypeError("Expected argument 'not_scopes' to be a list")
        pulumi.set(__self__, "not_scopes", not_scopes)
        if parameters and not isinstance(parameters, str):
            raise TypeError("Expected argument 'parameters' to be a str")
        pulumi.set(__self__, "parameters", parameters)
        if policy_definition_id and not isinstance(policy_definition_id, str):
            raise TypeError("Expected argument 'policy_definition_id' to be a str")
        pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        if scope_id and not isinstance(scope_id, str):
            raise TypeError("Expected argument 'scope_id' to be a str")
        pulumi.set(__self__, "scope_id", scope_id)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of this Policy Assignment.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name of this Policy Assignment.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enforce(self) -> bool:
        """
        Whether this Policy is enforced or not?
        """
        return pulumi.get(self, "enforce")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetPolicyAssignmentIdentityResult']:
        """
        A `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure Region where the Policy Assignment exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def metadata(self) -> str:
        """
        A JSON mapping of any Metadata for this Policy.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nonComplianceMessages")
    def non_compliance_messages(self) -> Sequence['outputs.GetPolicyAssignmentNonComplianceMessageResult']:
        """
        A `non_compliance_message` block as defined below.
        """
        return pulumi.get(self, "non_compliance_messages")

    @property
    @pulumi.getter(name="notScopes")
    def not_scopes(self) -> Sequence[str]:
        """
        A `not_scopes` block as defined below.
        """
        return pulumi.get(self, "not_scopes")

    @property
    @pulumi.getter
    def parameters(self) -> str:
        """
        A JSON mapping of any Parameters for this Policy.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> str:
        """
        The ID of the assigned Policy Definition.
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter(name="scopeId")
    def scope_id(self) -> str:
        return pulumi.get(self, "scope_id")


class AwaitableGetPolicyAssignmentResult(GetPolicyAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyAssignmentResult(
            description=self.description,
            display_name=self.display_name,
            enforce=self.enforce,
            id=self.id,
            identities=self.identities,
            location=self.location,
            metadata=self.metadata,
            name=self.name,
            non_compliance_messages=self.non_compliance_messages,
            not_scopes=self.not_scopes,
            parameters=self.parameters,
            policy_definition_id=self.policy_definition_id,
            scope_id=self.scope_id)


def get_policy_assignment(name: Optional[str] = None,
                          scope_id: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyAssignmentResult:
    """
    Use this data source to access information about an existing Policy Assignment.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.policy.get_policy_assignment(name="existing",
        scope_id=data["azurerm_resource_group"]["example"]["id"])
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Policy Assignment. Changing this forces a new Policy Assignment to be created.
    :param str scope_id: The ID of the scope this Policy Assignment is assigned to. The `scope_id` can be a subscription id, a resource group id, a management group id, or an ID of any resource that is assigned with a policy. Changing this forces a new Policy Assignment to be created.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['scopeId'] = scope_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:policy/getPolicyAssignment:getPolicyAssignment', __args__, opts=opts, typ=GetPolicyAssignmentResult).value

    return AwaitableGetPolicyAssignmentResult(
        description=__ret__.description,
        display_name=__ret__.display_name,
        enforce=__ret__.enforce,
        id=__ret__.id,
        identities=__ret__.identities,
        location=__ret__.location,
        metadata=__ret__.metadata,
        name=__ret__.name,
        non_compliance_messages=__ret__.non_compliance_messages,
        not_scopes=__ret__.not_scopes,
        parameters=__ret__.parameters,
        policy_definition_id=__ret__.policy_definition_id,
        scope_id=__ret__.scope_id)


@_utilities.lift_output_func(get_policy_assignment)
def get_policy_assignment_output(name: Optional[pulumi.Input[str]] = None,
                                 scope_id: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPolicyAssignmentResult]:
    """
    Use this data source to access information about an existing Policy Assignment.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.policy.get_policy_assignment(name="existing",
        scope_id=data["azurerm_resource_group"]["example"]["id"])
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Policy Assignment. Changing this forces a new Policy Assignment to be created.
    :param str scope_id: The ID of the scope this Policy Assignment is assigned to. The `scope_id` can be a subscription id, a resource group id, a management group id, or an ID of any resource that is assigned with a policy. Changing this forces a new Policy Assignment to be created.
    """
    ...
