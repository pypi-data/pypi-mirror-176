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
    'PolicySetDefinitionPolicyDefinitionGroup',
    'PolicySetDefinitionPolicyDefinitionReference',
    'VirtualMachineConfigurationAssignmentConfiguration',
    'VirtualMachineConfigurationAssignmentConfigurationParameter',
    'GetPolicyAssignmentIdentityResult',
    'GetPolicyAssignmentNonComplianceMessageResult',
    'GetPolicySetDefinitionPolicyDefinitionGroupResult',
    'GetPolicySetDefinitionPolicyDefinitionReferenceResult',
]

@pulumi.output_type
class PolicySetDefinitionPolicyDefinitionGroup(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "additionalMetadataResourceId":
            suggest = "additional_metadata_resource_id"
        elif key == "displayName":
            suggest = "display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicySetDefinitionPolicyDefinitionGroup. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicySetDefinitionPolicyDefinitionGroup.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicySetDefinitionPolicyDefinitionGroup.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 additional_metadata_resource_id: Optional[str] = None,
                 category: Optional[str] = None,
                 description: Optional[str] = None,
                 display_name: Optional[str] = None):
        """
        :param str name: The name of this policy definition group.
        :param str additional_metadata_resource_id: The ID of a resource that contains additional metadata about this policy definition group.
        :param str category: The category of this policy definition group.
        :param str description: The description of this policy definition group.
        :param str display_name: The display name of this policy definition group.
        """
        pulumi.set(__self__, "name", name)
        if additional_metadata_resource_id is not None:
            pulumi.set(__self__, "additional_metadata_resource_id", additional_metadata_resource_id)
        if category is not None:
            pulumi.set(__self__, "category", category)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of this policy definition group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="additionalMetadataResourceId")
    def additional_metadata_resource_id(self) -> Optional[str]:
        """
        The ID of a resource that contains additional metadata about this policy definition group.
        """
        return pulumi.get(self, "additional_metadata_resource_id")

    @property
    @pulumi.getter
    def category(self) -> Optional[str]:
        """
        The category of this policy definition group.
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of this policy definition group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name of this policy definition group.
        """
        return pulumi.get(self, "display_name")


@pulumi.output_type
class PolicySetDefinitionPolicyDefinitionReference(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "policyDefinitionId":
            suggest = "policy_definition_id"
        elif key == "parameterValues":
            suggest = "parameter_values"
        elif key == "policyGroupNames":
            suggest = "policy_group_names"
        elif key == "referenceId":
            suggest = "reference_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicySetDefinitionPolicyDefinitionReference. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicySetDefinitionPolicyDefinitionReference.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicySetDefinitionPolicyDefinitionReference.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 policy_definition_id: str,
                 parameter_values: Optional[str] = None,
                 policy_group_names: Optional[Sequence[str]] = None,
                 reference_id: Optional[str] = None):
        """
        :param str policy_definition_id: The ID of the policy definition or policy set definition that will be included in this policy set definition.
        :param str parameter_values: Parameter values for the referenced policy rule. This field is a JSON string that allows you to assign parameters to this policy rule.
        :param Sequence[str] policy_group_names: A list of names of the policy definition groups that this policy definition reference belongs to.
        :param str reference_id: A unique ID within this policy set definition for this policy definition reference.
        """
        pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        if parameter_values is not None:
            pulumi.set(__self__, "parameter_values", parameter_values)
        if policy_group_names is not None:
            pulumi.set(__self__, "policy_group_names", policy_group_names)
        if reference_id is not None:
            pulumi.set(__self__, "reference_id", reference_id)

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> str:
        """
        The ID of the policy definition or policy set definition that will be included in this policy set definition.
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter(name="parameterValues")
    def parameter_values(self) -> Optional[str]:
        """
        Parameter values for the referenced policy rule. This field is a JSON string that allows you to assign parameters to this policy rule.
        """
        return pulumi.get(self, "parameter_values")

    @property
    @pulumi.getter(name="policyGroupNames")
    def policy_group_names(self) -> Optional[Sequence[str]]:
        """
        A list of names of the policy definition groups that this policy definition reference belongs to.
        """
        return pulumi.get(self, "policy_group_names")

    @property
    @pulumi.getter(name="referenceId")
    def reference_id(self) -> Optional[str]:
        """
        A unique ID within this policy set definition for this policy definition reference.
        """
        return pulumi.get(self, "reference_id")


@pulumi.output_type
class VirtualMachineConfigurationAssignmentConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "assignmentType":
            suggest = "assignment_type"
        elif key == "contentHash":
            suggest = "content_hash"
        elif key == "contentUri":
            suggest = "content_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VirtualMachineConfigurationAssignmentConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VirtualMachineConfigurationAssignmentConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VirtualMachineConfigurationAssignmentConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 assignment_type: Optional[str] = None,
                 content_hash: Optional[str] = None,
                 content_uri: Optional[str] = None,
                 parameters: Optional[Sequence['outputs.VirtualMachineConfigurationAssignmentConfigurationParameter']] = None,
                 version: Optional[str] = None):
        """
        :param str assignment_type: The assignment type for the Guest Configuration Assignment. Possible values are `Audit`, `ApplyAndAutoCorrect`, `ApplyAndMonitor` and `DeployAndAutoCorrect`.
        :param str content_hash: The content hash for the Guest Configuration package.
        :param str content_uri: The content URI where the Guest Configuration package is stored.
        :param Sequence['VirtualMachineConfigurationAssignmentConfigurationParameterArgs'] parameters: One or more `parameter` blocks which define what configuration parameters and values against.
        :param str version: The version of the Guest Configuration that will be assigned in this Guest Configuration Assignment.
        """
        if assignment_type is not None:
            pulumi.set(__self__, "assignment_type", assignment_type)
        if content_hash is not None:
            pulumi.set(__self__, "content_hash", content_hash)
        if content_uri is not None:
            pulumi.set(__self__, "content_uri", content_uri)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="assignmentType")
    def assignment_type(self) -> Optional[str]:
        """
        The assignment type for the Guest Configuration Assignment. Possible values are `Audit`, `ApplyAndAutoCorrect`, `ApplyAndMonitor` and `DeployAndAutoCorrect`.
        """
        return pulumi.get(self, "assignment_type")

    @property
    @pulumi.getter(name="contentHash")
    def content_hash(self) -> Optional[str]:
        """
        The content hash for the Guest Configuration package.
        """
        return pulumi.get(self, "content_hash")

    @property
    @pulumi.getter(name="contentUri")
    def content_uri(self) -> Optional[str]:
        """
        The content URI where the Guest Configuration package is stored.
        """
        return pulumi.get(self, "content_uri")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Sequence['outputs.VirtualMachineConfigurationAssignmentConfigurationParameter']]:
        """
        One or more `parameter` blocks which define what configuration parameters and values against.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        The version of the Guest Configuration that will be assigned in this Guest Configuration Assignment.
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class VirtualMachineConfigurationAssignmentConfigurationParameter(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: The name of the configuration parameter to check.
        :param str value: The value to check the configuration parameter with.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the configuration parameter to check.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value to check the configuration parameter with.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class GetPolicyAssignmentIdentityResult(dict):
    def __init__(__self__, *,
                 identity_ids: Sequence[str],
                 principal_id: str,
                 tenant_id: str,
                 type: str):
        """
        :param Sequence[str] identity_ids: A `identity_ids` block as defined below.
        :param str principal_id: The Principal ID of the Policy Assignment for this Resource.
        :param str tenant_id: The Tenant ID of the Policy Assignment for this Resource.
        :param str type: The Type of Managed Identity which is added to this Policy Assignment.
        """
        pulumi.set(__self__, "identity_ids", identity_ids)
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Sequence[str]:
        """
        A `identity_ids` block as defined below.
        """
        return pulumi.get(self, "identity_ids")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The Principal ID of the Policy Assignment for this Resource.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The Tenant ID of the Policy Assignment for this Resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The Type of Managed Identity which is added to this Policy Assignment.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class GetPolicyAssignmentNonComplianceMessageResult(dict):
    def __init__(__self__, *,
                 content: str,
                 policy_definition_reference_id: str):
        """
        :param str content: The non-compliance message text.
        :param str policy_definition_reference_id: The ID of the Policy Definition that the non-compliance message applies to.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "policy_definition_reference_id", policy_definition_reference_id)

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        The non-compliance message text.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="policyDefinitionReferenceId")
    def policy_definition_reference_id(self) -> str:
        """
        The ID of the Policy Definition that the non-compliance message applies to.
        """
        return pulumi.get(self, "policy_definition_reference_id")


@pulumi.output_type
class GetPolicySetDefinitionPolicyDefinitionGroupResult(dict):
    def __init__(__self__, *,
                 additional_metadata_resource_id: str,
                 category: str,
                 description: str,
                 display_name: str,
                 name: str):
        """
        :param str additional_metadata_resource_id: The ID of a resource that contains additional metadata about this policy definition group.
        :param str category: The category of this policy definition group.
        :param str description: The description of this policy definition group.
        :param str display_name: Specifies the display name of the Policy Set Definition. Conflicts with `name`.
        :param str name: Specifies the name of the Policy Set Definition. Conflicts with `display_name`.
        """
        pulumi.set(__self__, "additional_metadata_resource_id", additional_metadata_resource_id)
        pulumi.set(__self__, "category", category)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="additionalMetadataResourceId")
    def additional_metadata_resource_id(self) -> str:
        """
        The ID of a resource that contains additional metadata about this policy definition group.
        """
        return pulumi.get(self, "additional_metadata_resource_id")

    @property
    @pulumi.getter
    def category(self) -> str:
        """
        The category of this policy definition group.
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of this policy definition group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Specifies the display name of the Policy Set Definition. Conflicts with `name`.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the Policy Set Definition. Conflicts with `display_name`.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class GetPolicySetDefinitionPolicyDefinitionReferenceResult(dict):
    def __init__(__self__, *,
                 parameter_values: str,
                 parameters: Mapping[str, str],
                 policy_definition_id: str,
                 policy_group_names: Sequence[str],
                 reference_id: str):
        """
        :param str parameter_values: The parameter values for the referenced policy rule. This field is a JSON object.
        :param Mapping[str, str] parameters: The mapping of the parameter values for the referenced policy rule. The keys are the parameter names.
        :param str policy_definition_id: The ID of the policy definition or policy set definition that is included in this policy set definition.
        :param Sequence[str] policy_group_names: The list of names of the policy definition groups that this policy definition reference belongs to.
        :param str reference_id: The unique ID within this policy set definition for this policy definition reference.
        """
        pulumi.set(__self__, "parameter_values", parameter_values)
        pulumi.set(__self__, "parameters", parameters)
        pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        pulumi.set(__self__, "policy_group_names", policy_group_names)
        pulumi.set(__self__, "reference_id", reference_id)

    @property
    @pulumi.getter(name="parameterValues")
    def parameter_values(self) -> str:
        """
        The parameter values for the referenced policy rule. This field is a JSON object.
        """
        return pulumi.get(self, "parameter_values")

    @property
    @pulumi.getter
    def parameters(self) -> Mapping[str, str]:
        """
        The mapping of the parameter values for the referenced policy rule. The keys are the parameter names.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> str:
        """
        The ID of the policy definition or policy set definition that is included in this policy set definition.
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter(name="policyGroupNames")
    def policy_group_names(self) -> Sequence[str]:
        """
        The list of names of the policy definition groups that this policy definition reference belongs to.
        """
        return pulumi.get(self, "policy_group_names")

    @property
    @pulumi.getter(name="referenceId")
    def reference_id(self) -> str:
        """
        The unique ID within this policy set definition for this policy definition reference.
        """
        return pulumi.get(self, "reference_id")


