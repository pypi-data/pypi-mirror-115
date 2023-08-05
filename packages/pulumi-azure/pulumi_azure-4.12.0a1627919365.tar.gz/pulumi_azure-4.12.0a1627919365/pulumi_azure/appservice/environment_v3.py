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

__all__ = ['EnvironmentV3Args', 'EnvironmentV3']

@pulumi.input_type
class EnvironmentV3Args:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 subnet_id: pulumi.Input[str],
                 cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentV3ClusterSettingArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a EnvironmentV3 resource.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the App Service Environment exists. Defaults to the Resource Group of the Subnet (specified by `subnet_id`).
        :param pulumi.Input[str] subnet_id: The ID of the Subnet which the App Service Environment should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['EnvironmentV3ClusterSettingArgs']]] cluster_settings: Zero or more `cluster_setting` blocks as defined below.
        :param pulumi.Input[str] name: The name of the App Service Environment. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "subnet_id", subnet_id)
        if cluster_settings is not None:
            pulumi.set(__self__, "cluster_settings", cluster_settings)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the App Service Environment exists. Defaults to the Resource Group of the Subnet (specified by `subnet_id`).
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The ID of the Subnet which the App Service Environment should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter(name="clusterSettings")
    def cluster_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentV3ClusterSettingArgs']]]]:
        """
        Zero or more `cluster_setting` blocks as defined below.
        """
        return pulumi.get(self, "cluster_settings")

    @cluster_settings.setter
    def cluster_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentV3ClusterSettingArgs']]]]):
        pulumi.set(self, "cluster_settings", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the App Service Environment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _EnvironmentV3State:
    def __init__(__self__, *,
                 cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentV3ClusterSettingArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pricing_tier: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering EnvironmentV3 resources.
        :param pulumi.Input[Sequence[pulumi.Input['EnvironmentV3ClusterSettingArgs']]] cluster_settings: Zero or more `cluster_setting` blocks as defined below.
        :param pulumi.Input[str] location: The location where the App Service Environment exists.
        :param pulumi.Input[str] name: The name of the App Service Environment. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pricing_tier: Pricing tier for the front end instances.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the App Service Environment exists. Defaults to the Resource Group of the Subnet (specified by `subnet_id`).
        :param pulumi.Input[str] subnet_id: The ID of the Subnet which the App Service Environment should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        if cluster_settings is not None:
            pulumi.set(__self__, "cluster_settings", cluster_settings)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if pricing_tier is not None:
            pulumi.set(__self__, "pricing_tier", pricing_tier)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="clusterSettings")
    def cluster_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentV3ClusterSettingArgs']]]]:
        """
        Zero or more `cluster_setting` blocks as defined below.
        """
        return pulumi.get(self, "cluster_settings")

    @cluster_settings.setter
    def cluster_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentV3ClusterSettingArgs']]]]):
        pulumi.set(self, "cluster_settings", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location where the App Service Environment exists.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the App Service Environment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="pricingTier")
    def pricing_tier(self) -> Optional[pulumi.Input[str]]:
        """
        Pricing tier for the front end instances.
        """
        return pulumi.get(self, "pricing_tier")

    @pricing_tier.setter
    def pricing_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pricing_tier", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the App Service Environment exists. Defaults to the Resource Group of the Subnet (specified by `subnet_id`).
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Subnet which the App Service Environment should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class EnvironmentV3(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentV3ClusterSettingArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a 3rd Generation (v3) App Service Environment.

        > **NOTE:** App Service Environment V3 is currently in Preview.

        ## Import

        A 3rd Generation (v3) App Service Environment can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/environmentV3:EnvironmentV3 myAppServiceEnv /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.Web/hostingEnvironments/myAppServiceEnv
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentV3ClusterSettingArgs']]]] cluster_settings: Zero or more `cluster_setting` blocks as defined below.
        :param pulumi.Input[str] name: The name of the App Service Environment. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the App Service Environment exists. Defaults to the Resource Group of the Subnet (specified by `subnet_id`).
        :param pulumi.Input[str] subnet_id: The ID of the Subnet which the App Service Environment should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnvironmentV3Args,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a 3rd Generation (v3) App Service Environment.

        > **NOTE:** App Service Environment V3 is currently in Preview.

        ## Import

        A 3rd Generation (v3) App Service Environment can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/environmentV3:EnvironmentV3 myAppServiceEnv /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.Web/hostingEnvironments/myAppServiceEnv
        ```

        :param str resource_name: The name of the resource.
        :param EnvironmentV3Args args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvironmentV3Args, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentV3ClusterSettingArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = EnvironmentV3Args.__new__(EnvironmentV3Args)

            __props__.__dict__["cluster_settings"] = cluster_settings
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if subnet_id is None and not opts.urn:
                raise TypeError("Missing required property 'subnet_id'")
            __props__.__dict__["subnet_id"] = subnet_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["location"] = None
            __props__.__dict__["pricing_tier"] = None
        super(EnvironmentV3, __self__).__init__(
            'azure:appservice/environmentV3:EnvironmentV3',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentV3ClusterSettingArgs']]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            pricing_tier: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            subnet_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'EnvironmentV3':
        """
        Get an existing EnvironmentV3 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentV3ClusterSettingArgs']]]] cluster_settings: Zero or more `cluster_setting` blocks as defined below.
        :param pulumi.Input[str] location: The location where the App Service Environment exists.
        :param pulumi.Input[str] name: The name of the App Service Environment. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pricing_tier: Pricing tier for the front end instances.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the App Service Environment exists. Defaults to the Resource Group of the Subnet (specified by `subnet_id`).
        :param pulumi.Input[str] subnet_id: The ID of the Subnet which the App Service Environment should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EnvironmentV3State.__new__(_EnvironmentV3State)

        __props__.__dict__["cluster_settings"] = cluster_settings
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["pricing_tier"] = pricing_tier
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["subnet_id"] = subnet_id
        __props__.__dict__["tags"] = tags
        return EnvironmentV3(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterSettings")
    def cluster_settings(self) -> pulumi.Output[Sequence['outputs.EnvironmentV3ClusterSetting']]:
        """
        Zero or more `cluster_setting` blocks as defined below.
        """
        return pulumi.get(self, "cluster_settings")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location where the App Service Environment exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the App Service Environment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pricingTier")
    def pricing_tier(self) -> pulumi.Output[str]:
        """
        Pricing tier for the front end instances.
        """
        return pulumi.get(self, "pricing_tier")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the App Service Environment exists. Defaults to the Resource Group of the Subnet (specified by `subnet_id`).
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Output[str]:
        """
        The ID of the Subnet which the App Service Environment should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

