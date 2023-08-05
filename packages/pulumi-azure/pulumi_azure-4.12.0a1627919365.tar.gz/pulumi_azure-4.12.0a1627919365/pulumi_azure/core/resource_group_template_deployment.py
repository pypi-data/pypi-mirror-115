# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ResourceGroupTemplateDeploymentArgs', 'ResourceGroupTemplateDeployment']

@pulumi.input_type
class ResourceGroupTemplateDeploymentArgs:
    def __init__(__self__, *,
                 deployment_mode: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 debug_level: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters_content: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_content: Optional[pulumi.Input[str]] = None,
                 template_spec_version_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ResourceGroupTemplateDeployment resource.
        :param pulumi.Input[str] deployment_mode: The Deployment Mode for this Resource Group Template Deployment. Possible values are `Complete` (where resources in the Resource Group not specified in the ARM Template will be destroyed) and `Incremental` (where resources are additive only).
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Resource Group Template Deployment should exist. Changing this forces a new Resource Group Template Deployment to be created.
        :param pulumi.Input[str] debug_level: The Debug Level which should be used for this Resource Group Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        :param pulumi.Input[str] name: The name which should be used for this Resource Group Template Deployment. Changing this forces a new Resource Group Template Deployment to be created.
        :param pulumi.Input[str] parameters_content: The contents of the ARM Template parameters file - containing a JSON list of parameters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Resource Group Template Deployment.
        :param pulumi.Input[str] template_content: The contents of the ARM Template which should be deployed into this Resource Group. Cannot be specified with `template_spec_version_id`.
        :param pulumi.Input[str] template_spec_version_id: The ID of the Template Spec Version to deploy. Cannot be specified with `template_content`.
        """
        pulumi.set(__self__, "deployment_mode", deployment_mode)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if debug_level is not None:
            pulumi.set(__self__, "debug_level", debug_level)
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
    @pulumi.getter(name="deploymentMode")
    def deployment_mode(self) -> pulumi.Input[str]:
        """
        The Deployment Mode for this Resource Group Template Deployment. Possible values are `Complete` (where resources in the Resource Group not specified in the ARM Template will be destroyed) and `Incremental` (where resources are additive only).
        """
        return pulumi.get(self, "deployment_mode")

    @deployment_mode.setter
    def deployment_mode(self, value: pulumi.Input[str]):
        pulumi.set(self, "deployment_mode", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Resource Group Template Deployment should exist. Changing this forces a new Resource Group Template Deployment to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="debugLevel")
    def debug_level(self) -> Optional[pulumi.Input[str]]:
        """
        The Debug Level which should be used for this Resource Group Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        """
        return pulumi.get(self, "debug_level")

    @debug_level.setter
    def debug_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "debug_level", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Resource Group Template Deployment. Changing this forces a new Resource Group Template Deployment to be created.
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
        A mapping of tags which should be assigned to the Resource Group Template Deployment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="templateContent")
    def template_content(self) -> Optional[pulumi.Input[str]]:
        """
        The contents of the ARM Template which should be deployed into this Resource Group. Cannot be specified with `template_spec_version_id`.
        """
        return pulumi.get(self, "template_content")

    @template_content.setter
    def template_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_content", value)

    @property
    @pulumi.getter(name="templateSpecVersionId")
    def template_spec_version_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Template Spec Version to deploy. Cannot be specified with `template_content`.
        """
        return pulumi.get(self, "template_spec_version_id")

    @template_spec_version_id.setter
    def template_spec_version_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_spec_version_id", value)


@pulumi.input_type
class _ResourceGroupTemplateDeploymentState:
    def __init__(__self__, *,
                 debug_level: Optional[pulumi.Input[str]] = None,
                 deployment_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_content: Optional[pulumi.Input[str]] = None,
                 parameters_content: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_content: Optional[pulumi.Input[str]] = None,
                 template_spec_version_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ResourceGroupTemplateDeployment resources.
        :param pulumi.Input[str] debug_level: The Debug Level which should be used for this Resource Group Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        :param pulumi.Input[str] deployment_mode: The Deployment Mode for this Resource Group Template Deployment. Possible values are `Complete` (where resources in the Resource Group not specified in the ARM Template will be destroyed) and `Incremental` (where resources are additive only).
        :param pulumi.Input[str] name: The name which should be used for this Resource Group Template Deployment. Changing this forces a new Resource Group Template Deployment to be created.
        :param pulumi.Input[str] output_content: The JSON Content of the Outputs of the ARM Template Deployment.
        :param pulumi.Input[str] parameters_content: The contents of the ARM Template parameters file - containing a JSON list of parameters.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Resource Group Template Deployment should exist. Changing this forces a new Resource Group Template Deployment to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Resource Group Template Deployment.
        :param pulumi.Input[str] template_content: The contents of the ARM Template which should be deployed into this Resource Group. Cannot be specified with `template_spec_version_id`.
        :param pulumi.Input[str] template_spec_version_id: The ID of the Template Spec Version to deploy. Cannot be specified with `template_content`.
        """
        if debug_level is not None:
            pulumi.set(__self__, "debug_level", debug_level)
        if deployment_mode is not None:
            pulumi.set(__self__, "deployment_mode", deployment_mode)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if output_content is not None:
            pulumi.set(__self__, "output_content", output_content)
        if parameters_content is not None:
            pulumi.set(__self__, "parameters_content", parameters_content)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
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
        The Debug Level which should be used for this Resource Group Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        """
        return pulumi.get(self, "debug_level")

    @debug_level.setter
    def debug_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "debug_level", value)

    @property
    @pulumi.getter(name="deploymentMode")
    def deployment_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The Deployment Mode for this Resource Group Template Deployment. Possible values are `Complete` (where resources in the Resource Group not specified in the ARM Template will be destroyed) and `Incremental` (where resources are additive only).
        """
        return pulumi.get(self, "deployment_mode")

    @deployment_mode.setter
    def deployment_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deployment_mode", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Resource Group Template Deployment. Changing this forces a new Resource Group Template Deployment to be created.
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
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Resource Group Template Deployment should exist. Changing this forces a new Resource Group Template Deployment to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Resource Group Template Deployment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="templateContent")
    def template_content(self) -> Optional[pulumi.Input[str]]:
        """
        The contents of the ARM Template which should be deployed into this Resource Group. Cannot be specified with `template_spec_version_id`.
        """
        return pulumi.get(self, "template_content")

    @template_content.setter
    def template_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_content", value)

    @property
    @pulumi.getter(name="templateSpecVersionId")
    def template_spec_version_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Template Spec Version to deploy. Cannot be specified with `template_content`.
        """
        return pulumi.get(self, "template_spec_version_id")

    @template_spec_version_id.setter
    def template_spec_version_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_spec_version_id", value)


class ResourceGroupTemplateDeployment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 debug_level: Optional[pulumi.Input[str]] = None,
                 deployment_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters_content: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_content: Optional[pulumi.Input[str]] = None,
                 template_spec_version_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Resource Group Template Deployment.

        > **Note:** This resource will automatically attempt to delete resources deployed by the ARM Template when it is deleted. You can opt-out of this by setting the `delete_nested_items_during_deletion` field within the `template_deployment` block of the `features` block to `false`.

        ## Import

        Resource Group Template Deployments can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:core/resourceGroupTemplateDeployment:ResourceGroupTemplateDeployment example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Resources/deployments/template1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] debug_level: The Debug Level which should be used for this Resource Group Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        :param pulumi.Input[str] deployment_mode: The Deployment Mode for this Resource Group Template Deployment. Possible values are `Complete` (where resources in the Resource Group not specified in the ARM Template will be destroyed) and `Incremental` (where resources are additive only).
        :param pulumi.Input[str] name: The name which should be used for this Resource Group Template Deployment. Changing this forces a new Resource Group Template Deployment to be created.
        :param pulumi.Input[str] parameters_content: The contents of the ARM Template parameters file - containing a JSON list of parameters.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Resource Group Template Deployment should exist. Changing this forces a new Resource Group Template Deployment to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Resource Group Template Deployment.
        :param pulumi.Input[str] template_content: The contents of the ARM Template which should be deployed into this Resource Group. Cannot be specified with `template_spec_version_id`.
        :param pulumi.Input[str] template_spec_version_id: The ID of the Template Spec Version to deploy. Cannot be specified with `template_content`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceGroupTemplateDeploymentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Resource Group Template Deployment.

        > **Note:** This resource will automatically attempt to delete resources deployed by the ARM Template when it is deleted. You can opt-out of this by setting the `delete_nested_items_during_deletion` field within the `template_deployment` block of the `features` block to `false`.

        ## Import

        Resource Group Template Deployments can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:core/resourceGroupTemplateDeployment:ResourceGroupTemplateDeployment example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Resources/deployments/template1
        ```

        :param str resource_name: The name of the resource.
        :param ResourceGroupTemplateDeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceGroupTemplateDeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 debug_level: Optional[pulumi.Input[str]] = None,
                 deployment_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters_content: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_content: Optional[pulumi.Input[str]] = None,
                 template_spec_version_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = ResourceGroupTemplateDeploymentArgs.__new__(ResourceGroupTemplateDeploymentArgs)

            __props__.__dict__["debug_level"] = debug_level
            if deployment_mode is None and not opts.urn:
                raise TypeError("Missing required property 'deployment_mode'")
            __props__.__dict__["deployment_mode"] = deployment_mode
            __props__.__dict__["name"] = name
            __props__.__dict__["parameters_content"] = parameters_content
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["template_content"] = template_content
            __props__.__dict__["template_spec_version_id"] = template_spec_version_id
            __props__.__dict__["output_content"] = None
        super(ResourceGroupTemplateDeployment, __self__).__init__(
            'azure:core/resourceGroupTemplateDeployment:ResourceGroupTemplateDeployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            debug_level: Optional[pulumi.Input[str]] = None,
            deployment_mode: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            output_content: Optional[pulumi.Input[str]] = None,
            parameters_content: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            template_content: Optional[pulumi.Input[str]] = None,
            template_spec_version_id: Optional[pulumi.Input[str]] = None) -> 'ResourceGroupTemplateDeployment':
        """
        Get an existing ResourceGroupTemplateDeployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] debug_level: The Debug Level which should be used for this Resource Group Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        :param pulumi.Input[str] deployment_mode: The Deployment Mode for this Resource Group Template Deployment. Possible values are `Complete` (where resources in the Resource Group not specified in the ARM Template will be destroyed) and `Incremental` (where resources are additive only).
        :param pulumi.Input[str] name: The name which should be used for this Resource Group Template Deployment. Changing this forces a new Resource Group Template Deployment to be created.
        :param pulumi.Input[str] output_content: The JSON Content of the Outputs of the ARM Template Deployment.
        :param pulumi.Input[str] parameters_content: The contents of the ARM Template parameters file - containing a JSON list of parameters.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Resource Group Template Deployment should exist. Changing this forces a new Resource Group Template Deployment to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Resource Group Template Deployment.
        :param pulumi.Input[str] template_content: The contents of the ARM Template which should be deployed into this Resource Group. Cannot be specified with `template_spec_version_id`.
        :param pulumi.Input[str] template_spec_version_id: The ID of the Template Spec Version to deploy. Cannot be specified with `template_content`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceGroupTemplateDeploymentState.__new__(_ResourceGroupTemplateDeploymentState)

        __props__.__dict__["debug_level"] = debug_level
        __props__.__dict__["deployment_mode"] = deployment_mode
        __props__.__dict__["name"] = name
        __props__.__dict__["output_content"] = output_content
        __props__.__dict__["parameters_content"] = parameters_content
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["template_content"] = template_content
        __props__.__dict__["template_spec_version_id"] = template_spec_version_id
        return ResourceGroupTemplateDeployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="debugLevel")
    def debug_level(self) -> pulumi.Output[Optional[str]]:
        """
        The Debug Level which should be used for this Resource Group Template Deployment. Possible values are `none`, `requestContent`, `responseContent` and `requestContent, responseContent`.
        """
        return pulumi.get(self, "debug_level")

    @property
    @pulumi.getter(name="deploymentMode")
    def deployment_mode(self) -> pulumi.Output[str]:
        """
        The Deployment Mode for this Resource Group Template Deployment. Possible values are `Complete` (where resources in the Resource Group not specified in the ARM Template will be destroyed) and `Incremental` (where resources are additive only).
        """
        return pulumi.get(self, "deployment_mode")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Resource Group Template Deployment. Changing this forces a new Resource Group Template Deployment to be created.
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
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Resource Group Template Deployment should exist. Changing this forces a new Resource Group Template Deployment to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Resource Group Template Deployment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="templateContent")
    def template_content(self) -> pulumi.Output[str]:
        """
        The contents of the ARM Template which should be deployed into this Resource Group. Cannot be specified with `template_spec_version_id`.
        """
        return pulumi.get(self, "template_content")

    @property
    @pulumi.getter(name="templateSpecVersionId")
    def template_spec_version_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Template Spec Version to deploy. Cannot be specified with `template_content`.
        """
        return pulumi.get(self, "template_spec_version_id")

