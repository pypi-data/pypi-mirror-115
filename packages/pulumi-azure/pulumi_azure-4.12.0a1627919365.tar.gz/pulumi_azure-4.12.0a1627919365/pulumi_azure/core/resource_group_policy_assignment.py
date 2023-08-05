# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ResourceGroupPolicyAssignmentArgs', 'ResourceGroupPolicyAssignment']

@pulumi.input_type
class ResourceGroupPolicyAssignmentArgs:
    def __init__(__self__, *,
                 policy_definition_id: pulumi.Input[str],
                 resource_group_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enforce: Optional[pulumi.Input[bool]] = None,
                 identity: Optional[pulumi.Input['ResourceGroupPolicyAssignmentIdentityArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parameters: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ResourceGroupPolicyAssignment resource.
        :param pulumi.Input[str] policy_definition_id: The ID of the Policy Definition or Policy Definition Set. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] resource_group_id: The ID of the Resource Group where this Policy Assignment should be created. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] description: A description which should be used for this Policy Assignment.
        :param pulumi.Input[str] display_name: The Display Name for this Policy Assignment.
        :param pulumi.Input[bool] enforce: Specifies if this Policy should be enforced or not?
        :param pulumi.Input['ResourceGroupPolicyAssignmentIdentityArgs'] identity: A `identity` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the Policy Assignment should exist. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] metadata: A JSON mapping of any Metadata for this Policy.
        :param pulumi.Input[str] name: The name which should be used for this Policy Assignment. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_scopes: Specifies a list of Resource Scopes (for example a Subscription, or a Resource Group) within this Management Group which are excluded from this Policy.
        :param pulumi.Input[str] parameters: A JSON mapping of any Parameters for this Policy. Changing this forces a new Management Group Policy Assignment to be created.
        """
        pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if enforce is not None:
            pulumi.set(__self__, "enforce", enforce)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if not_scopes is not None:
            pulumi.set(__self__, "not_scopes", not_scopes)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> pulumi.Input[str]:
        """
        The ID of the Policy Definition or Policy Definition Set. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "policy_definition_id")

    @policy_definition_id.setter
    def policy_definition_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_definition_id", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Input[str]:
        """
        The ID of the Resource Group where this Policy Assignment should be created. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description which should be used for this Policy Assignment.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Display Name for this Policy Assignment.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enforce(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if this Policy should be enforced or not?
        """
        return pulumi.get(self, "enforce")

    @enforce.setter
    def enforce(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enforce", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ResourceGroupPolicyAssignmentIdentityArgs']]:
        """
        A `identity` block as defined below.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ResourceGroupPolicyAssignmentIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Policy Assignment should exist. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input[str]]:
        """
        A JSON mapping of any Metadata for this Policy.
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Policy Assignment. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notScopes")
    def not_scopes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of Resource Scopes (for example a Subscription, or a Resource Group) within this Management Group which are excluded from this Policy.
        """
        return pulumi.get(self, "not_scopes")

    @not_scopes.setter
    def not_scopes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_scopes", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[str]]:
        """
        A JSON mapping of any Parameters for this Policy. Changing this forces a new Management Group Policy Assignment to be created.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parameters", value)


@pulumi.input_type
class _ResourceGroupPolicyAssignmentState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enforce: Optional[pulumi.Input[bool]] = None,
                 identity: Optional[pulumi.Input['ResourceGroupPolicyAssignmentIdentityArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parameters: Optional[pulumi.Input[str]] = None,
                 policy_definition_id: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ResourceGroupPolicyAssignment resources.
        :param pulumi.Input[str] description: A description which should be used for this Policy Assignment.
        :param pulumi.Input[str] display_name: The Display Name for this Policy Assignment.
        :param pulumi.Input[bool] enforce: Specifies if this Policy should be enforced or not?
        :param pulumi.Input['ResourceGroupPolicyAssignmentIdentityArgs'] identity: A `identity` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the Policy Assignment should exist. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] metadata: A JSON mapping of any Metadata for this Policy.
        :param pulumi.Input[str] name: The name which should be used for this Policy Assignment. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_scopes: Specifies a list of Resource Scopes (for example a Subscription, or a Resource Group) within this Management Group which are excluded from this Policy.
        :param pulumi.Input[str] parameters: A JSON mapping of any Parameters for this Policy. Changing this forces a new Management Group Policy Assignment to be created.
        :param pulumi.Input[str] policy_definition_id: The ID of the Policy Definition or Policy Definition Set. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] resource_group_id: The ID of the Resource Group where this Policy Assignment should be created. Changing this forces a new Policy Assignment to be created.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if enforce is not None:
            pulumi.set(__self__, "enforce", enforce)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if not_scopes is not None:
            pulumi.set(__self__, "not_scopes", not_scopes)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if policy_definition_id is not None:
            pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description which should be used for this Policy Assignment.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Display Name for this Policy Assignment.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enforce(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if this Policy should be enforced or not?
        """
        return pulumi.get(self, "enforce")

    @enforce.setter
    def enforce(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enforce", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ResourceGroupPolicyAssignmentIdentityArgs']]:
        """
        A `identity` block as defined below.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ResourceGroupPolicyAssignmentIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Policy Assignment should exist. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input[str]]:
        """
        A JSON mapping of any Metadata for this Policy.
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Policy Assignment. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notScopes")
    def not_scopes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of Resource Scopes (for example a Subscription, or a Resource Group) within this Management Group which are excluded from this Policy.
        """
        return pulumi.get(self, "not_scopes")

    @not_scopes.setter
    def not_scopes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_scopes", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[str]]:
        """
        A JSON mapping of any Parameters for this Policy. Changing this forces a new Management Group Policy Assignment to be created.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Policy Definition or Policy Definition Set. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "policy_definition_id")

    @policy_definition_id.setter
    def policy_definition_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_definition_id", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Resource Group where this Policy Assignment should be created. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)


class ResourceGroupPolicyAssignment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enforce: Optional[pulumi.Input[bool]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ResourceGroupPolicyAssignmentIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parameters: Optional[pulumi.Input[str]] = None,
                 policy_definition_id: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Resource Group Policy Assignment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_definition = azure.policy.Definition("exampleDefinition",
            policy_type="Custom",
            mode="All",
            policy_rule=\"\"\"	{
            "if": {
              "not": {
                "field": "location",
                "equals": "westeurope"
              }
            },
            "then": {
              "effect": "Deny"
            }
          }
        \"\"\")
        example_resource_group_policy_assignment = azure.core.ResourceGroupPolicyAssignment("exampleResourceGroupPolicyAssignment",
            resource_group_id=example_resource_group.id,
            policy_definition_id=example_definition.id)
        ```

        ## Import

        Resource Group Policy Assignments can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:core/resourceGroupPolicyAssignment:ResourceGroupPolicyAssignment example /subscriptions/00000000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Authorization/policyAssignments/assignment1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description which should be used for this Policy Assignment.
        :param pulumi.Input[str] display_name: The Display Name for this Policy Assignment.
        :param pulumi.Input[bool] enforce: Specifies if this Policy should be enforced or not?
        :param pulumi.Input[pulumi.InputType['ResourceGroupPolicyAssignmentIdentityArgs']] identity: A `identity` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the Policy Assignment should exist. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] metadata: A JSON mapping of any Metadata for this Policy.
        :param pulumi.Input[str] name: The name which should be used for this Policy Assignment. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_scopes: Specifies a list of Resource Scopes (for example a Subscription, or a Resource Group) within this Management Group which are excluded from this Policy.
        :param pulumi.Input[str] parameters: A JSON mapping of any Parameters for this Policy. Changing this forces a new Management Group Policy Assignment to be created.
        :param pulumi.Input[str] policy_definition_id: The ID of the Policy Definition or Policy Definition Set. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] resource_group_id: The ID of the Resource Group where this Policy Assignment should be created. Changing this forces a new Policy Assignment to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceGroupPolicyAssignmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Resource Group Policy Assignment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_definition = azure.policy.Definition("exampleDefinition",
            policy_type="Custom",
            mode="All",
            policy_rule=\"\"\"	{
            "if": {
              "not": {
                "field": "location",
                "equals": "westeurope"
              }
            },
            "then": {
              "effect": "Deny"
            }
          }
        \"\"\")
        example_resource_group_policy_assignment = azure.core.ResourceGroupPolicyAssignment("exampleResourceGroupPolicyAssignment",
            resource_group_id=example_resource_group.id,
            policy_definition_id=example_definition.id)
        ```

        ## Import

        Resource Group Policy Assignments can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:core/resourceGroupPolicyAssignment:ResourceGroupPolicyAssignment example /subscriptions/00000000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Authorization/policyAssignments/assignment1
        ```

        :param str resource_name: The name of the resource.
        :param ResourceGroupPolicyAssignmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceGroupPolicyAssignmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enforce: Optional[pulumi.Input[bool]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ResourceGroupPolicyAssignmentIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parameters: Optional[pulumi.Input[str]] = None,
                 policy_definition_id: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceGroupPolicyAssignmentArgs.__new__(ResourceGroupPolicyAssignmentArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["enforce"] = enforce
            __props__.__dict__["identity"] = identity
            __props__.__dict__["location"] = location
            __props__.__dict__["metadata"] = metadata
            __props__.__dict__["name"] = name
            __props__.__dict__["not_scopes"] = not_scopes
            __props__.__dict__["parameters"] = parameters
            if policy_definition_id is None and not opts.urn:
                raise TypeError("Missing required property 'policy_definition_id'")
            __props__.__dict__["policy_definition_id"] = policy_definition_id
            if resource_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_id'")
            __props__.__dict__["resource_group_id"] = resource_group_id
        super(ResourceGroupPolicyAssignment, __self__).__init__(
            'azure:core/resourceGroupPolicyAssignment:ResourceGroupPolicyAssignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            enforce: Optional[pulumi.Input[bool]] = None,
            identity: Optional[pulumi.Input[pulumi.InputType['ResourceGroupPolicyAssignmentIdentityArgs']]] = None,
            location: Optional[pulumi.Input[str]] = None,
            metadata: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            not_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            parameters: Optional[pulumi.Input[str]] = None,
            policy_definition_id: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None) -> 'ResourceGroupPolicyAssignment':
        """
        Get an existing ResourceGroupPolicyAssignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description which should be used for this Policy Assignment.
        :param pulumi.Input[str] display_name: The Display Name for this Policy Assignment.
        :param pulumi.Input[bool] enforce: Specifies if this Policy should be enforced or not?
        :param pulumi.Input[pulumi.InputType['ResourceGroupPolicyAssignmentIdentityArgs']] identity: A `identity` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the Policy Assignment should exist. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] metadata: A JSON mapping of any Metadata for this Policy.
        :param pulumi.Input[str] name: The name which should be used for this Policy Assignment. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_scopes: Specifies a list of Resource Scopes (for example a Subscription, or a Resource Group) within this Management Group which are excluded from this Policy.
        :param pulumi.Input[str] parameters: A JSON mapping of any Parameters for this Policy. Changing this forces a new Management Group Policy Assignment to be created.
        :param pulumi.Input[str] policy_definition_id: The ID of the Policy Definition or Policy Definition Set. Changing this forces a new Policy Assignment to be created.
        :param pulumi.Input[str] resource_group_id: The ID of the Resource Group where this Policy Assignment should be created. Changing this forces a new Policy Assignment to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceGroupPolicyAssignmentState.__new__(_ResourceGroupPolicyAssignmentState)

        __props__.__dict__["description"] = description
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["enforce"] = enforce
        __props__.__dict__["identity"] = identity
        __props__.__dict__["location"] = location
        __props__.__dict__["metadata"] = metadata
        __props__.__dict__["name"] = name
        __props__.__dict__["not_scopes"] = not_scopes
        __props__.__dict__["parameters"] = parameters
        __props__.__dict__["policy_definition_id"] = policy_definition_id
        __props__.__dict__["resource_group_id"] = resource_group_id
        return ResourceGroupPolicyAssignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description which should be used for this Policy Assignment.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        The Display Name for this Policy Assignment.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enforce(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if this Policy should be enforced or not?
        """
        return pulumi.get(self, "enforce")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ResourceGroupPolicyAssignmentIdentity']]:
        """
        A `identity` block as defined below.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Policy Assignment should exist. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[str]:
        """
        A JSON mapping of any Metadata for this Policy.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Policy Assignment. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notScopes")
    def not_scopes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies a list of Resource Scopes (for example a Subscription, or a Resource Group) within this Management Group which are excluded from this Policy.
        """
        return pulumi.get(self, "not_scopes")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Optional[str]]:
        """
        A JSON mapping of any Parameters for this Policy. Changing this forces a new Management Group Policy Assignment to be created.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> pulumi.Output[str]:
        """
        The ID of the Policy Definition or Policy Definition Set. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the Resource Group where this Policy Assignment should be created. Changing this forces a new Policy Assignment to be created.
        """
        return pulumi.get(self, "resource_group_id")

