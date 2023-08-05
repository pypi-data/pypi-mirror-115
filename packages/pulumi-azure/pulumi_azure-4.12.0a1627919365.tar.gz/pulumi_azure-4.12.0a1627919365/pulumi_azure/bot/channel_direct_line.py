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

__all__ = ['ChannelDirectLineArgs', 'ChannelDirectLine']

@pulumi.input_type
class ChannelDirectLineArgs:
    def __init__(__self__, *,
                 bot_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 sites: pulumi.Input[Sequence[pulumi.Input['ChannelDirectLineSiteArgs']]],
                 location: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ChannelDirectLine resource.
        :param pulumi.Input[str] bot_name: The name of the Bot Resource this channel will be associated with. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Bot Channel. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['ChannelDirectLineSiteArgs']]] sites: A site represents a client application that you want to connect to your bot. Multiple `site` blocks may be defined as below
        :param pulumi.Input[str] location: The supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "bot_name", bot_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sites", sites)
        if location is not None:
            pulumi.set(__self__, "location", location)

    @property
    @pulumi.getter(name="botName")
    def bot_name(self) -> pulumi.Input[str]:
        """
        The name of the Bot Resource this channel will be associated with. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "bot_name")

    @bot_name.setter
    def bot_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "bot_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the Bot Channel. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def sites(self) -> pulumi.Input[Sequence[pulumi.Input['ChannelDirectLineSiteArgs']]]:
        """
        A site represents a client application that you want to connect to your bot. Multiple `site` blocks may be defined as below
        """
        return pulumi.get(self, "sites")

    @sites.setter
    def sites(self, value: pulumi.Input[Sequence[pulumi.Input['ChannelDirectLineSiteArgs']]]):
        pulumi.set(self, "sites", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)


@pulumi.input_type
class _ChannelDirectLineState:
    def __init__(__self__, *,
                 bot_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sites: Optional[pulumi.Input[Sequence[pulumi.Input['ChannelDirectLineSiteArgs']]]] = None):
        """
        Input properties used for looking up and filtering ChannelDirectLine resources.
        :param pulumi.Input[str] bot_name: The name of the Bot Resource this channel will be associated with. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Bot Channel. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['ChannelDirectLineSiteArgs']]] sites: A site represents a client application that you want to connect to your bot. Multiple `site` blocks may be defined as below
        """
        if bot_name is not None:
            pulumi.set(__self__, "bot_name", bot_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sites is not None:
            pulumi.set(__self__, "sites", sites)

    @property
    @pulumi.getter(name="botName")
    def bot_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Bot Resource this channel will be associated with. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "bot_name")

    @bot_name.setter
    def bot_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bot_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the Bot Channel. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def sites(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ChannelDirectLineSiteArgs']]]]:
        """
        A site represents a client application that you want to connect to your bot. Multiple `site` blocks may be defined as below
        """
        return pulumi.get(self, "sites")

    @sites.setter
    def sites(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ChannelDirectLineSiteArgs']]]]):
        pulumi.set(self, "sites", value)


class ChannelDirectLine(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bot_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sites: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ChannelDirectLineSiteArgs']]]]] = None,
                 __props__=None):
        """
        Manages a Directline integration for a Bot Channel

        ## Import

        The Directline Channel for a Bot can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:bot/channelDirectLine:ChannelDirectLine example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example/providers/Microsoft.BotService/botServices/example/channels/DirectlineChannel
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bot_name: The name of the Bot Resource this channel will be associated with. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Bot Channel. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ChannelDirectLineSiteArgs']]]] sites: A site represents a client application that you want to connect to your bot. Multiple `site` blocks may be defined as below
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ChannelDirectLineArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Directline integration for a Bot Channel

        ## Import

        The Directline Channel for a Bot can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:bot/channelDirectLine:ChannelDirectLine example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example/providers/Microsoft.BotService/botServices/example/channels/DirectlineChannel
        ```

        :param str resource_name: The name of the resource.
        :param ChannelDirectLineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ChannelDirectLineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bot_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sites: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ChannelDirectLineSiteArgs']]]]] = None,
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
            __props__ = ChannelDirectLineArgs.__new__(ChannelDirectLineArgs)

            if bot_name is None and not opts.urn:
                raise TypeError("Missing required property 'bot_name'")
            __props__.__dict__["bot_name"] = bot_name
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sites is None and not opts.urn:
                raise TypeError("Missing required property 'sites'")
            __props__.__dict__["sites"] = sites
        super(ChannelDirectLine, __self__).__init__(
            'azure:bot/channelDirectLine:ChannelDirectLine',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bot_name: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            sites: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ChannelDirectLineSiteArgs']]]]] = None) -> 'ChannelDirectLine':
        """
        Get an existing ChannelDirectLine resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bot_name: The name of the Bot Resource this channel will be associated with. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Bot Channel. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ChannelDirectLineSiteArgs']]]] sites: A site represents a client application that you want to connect to your bot. Multiple `site` blocks may be defined as below
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ChannelDirectLineState.__new__(_ChannelDirectLineState)

        __props__.__dict__["bot_name"] = bot_name
        __props__.__dict__["location"] = location
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["sites"] = sites
        return ChannelDirectLine(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="botName")
    def bot_name(self) -> pulumi.Output[str]:
        """
        The name of the Bot Resource this channel will be associated with. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "bot_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the Bot Channel. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def sites(self) -> pulumi.Output[Sequence['outputs.ChannelDirectLineSite']]:
        """
        A site represents a client application that you want to connect to your bot. Multiple `site` blocks may be defined as below
        """
        return pulumi.get(self, "sites")

