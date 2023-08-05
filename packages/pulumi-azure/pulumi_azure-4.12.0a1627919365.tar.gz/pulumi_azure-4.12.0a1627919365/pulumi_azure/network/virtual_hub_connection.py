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

__all__ = ['VirtualHubConnectionArgs', 'VirtualHubConnection']

@pulumi.input_type
class VirtualHubConnectionArgs:
    def __init__(__self__, *,
                 remote_virtual_network_id: pulumi.Input[str],
                 virtual_hub_id: pulumi.Input[str],
                 hub_to_vitual_network_traffic_allowed: Optional[pulumi.Input[bool]] = None,
                 internet_security_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 routing: Optional[pulumi.Input['VirtualHubConnectionRoutingArgs']] = None,
                 vitual_network_to_hub_gateways_traffic_allowed: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a VirtualHubConnection resource.
        :param pulumi.Input[str] remote_virtual_network_id: The ID of the Virtual Network which the Virtual Hub should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub within which this connection should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] internet_security_enabled: Should Internet Security be enabled to secure internet traffic? Changing this forces a new resource to be created. Defaults to `false`.
        :param pulumi.Input[str] name: The Name which should be used for this Connection, which must be unique within the Virtual Hub. Changing this forces a new resource to be created.
        :param pulumi.Input['VirtualHubConnectionRoutingArgs'] routing: A `routing` block as defined below.
        """
        pulumi.set(__self__, "remote_virtual_network_id", remote_virtual_network_id)
        pulumi.set(__self__, "virtual_hub_id", virtual_hub_id)
        if hub_to_vitual_network_traffic_allowed is not None:
            warnings.warn("""Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""", DeprecationWarning)
            pulumi.log.warn("""hub_to_vitual_network_traffic_allowed is deprecated: Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""")
        if hub_to_vitual_network_traffic_allowed is not None:
            pulumi.set(__self__, "hub_to_vitual_network_traffic_allowed", hub_to_vitual_network_traffic_allowed)
        if internet_security_enabled is not None:
            pulumi.set(__self__, "internet_security_enabled", internet_security_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if routing is not None:
            pulumi.set(__self__, "routing", routing)
        if vitual_network_to_hub_gateways_traffic_allowed is not None:
            warnings.warn("""Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""", DeprecationWarning)
            pulumi.log.warn("""vitual_network_to_hub_gateways_traffic_allowed is deprecated: Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""")
        if vitual_network_to_hub_gateways_traffic_allowed is not None:
            pulumi.set(__self__, "vitual_network_to_hub_gateways_traffic_allowed", vitual_network_to_hub_gateways_traffic_allowed)

    @property
    @pulumi.getter(name="remoteVirtualNetworkId")
    def remote_virtual_network_id(self) -> pulumi.Input[str]:
        """
        The ID of the Virtual Network which the Virtual Hub should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "remote_virtual_network_id")

    @remote_virtual_network_id.setter
    def remote_virtual_network_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "remote_virtual_network_id", value)

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> pulumi.Input[str]:
        """
        The ID of the Virtual Hub within which this connection should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_hub_id", value)

    @property
    @pulumi.getter(name="hubToVitualNetworkTrafficAllowed")
    def hub_to_vitual_network_traffic_allowed(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "hub_to_vitual_network_traffic_allowed")

    @hub_to_vitual_network_traffic_allowed.setter
    def hub_to_vitual_network_traffic_allowed(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hub_to_vitual_network_traffic_allowed", value)

    @property
    @pulumi.getter(name="internetSecurityEnabled")
    def internet_security_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should Internet Security be enabled to secure internet traffic? Changing this forces a new resource to be created. Defaults to `false`.
        """
        return pulumi.get(self, "internet_security_enabled")

    @internet_security_enabled.setter
    def internet_security_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "internet_security_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The Name which should be used for this Connection, which must be unique within the Virtual Hub. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def routing(self) -> Optional[pulumi.Input['VirtualHubConnectionRoutingArgs']]:
        """
        A `routing` block as defined below.
        """
        return pulumi.get(self, "routing")

    @routing.setter
    def routing(self, value: Optional[pulumi.Input['VirtualHubConnectionRoutingArgs']]):
        pulumi.set(self, "routing", value)

    @property
    @pulumi.getter(name="vitualNetworkToHubGatewaysTrafficAllowed")
    def vitual_network_to_hub_gateways_traffic_allowed(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "vitual_network_to_hub_gateways_traffic_allowed")

    @vitual_network_to_hub_gateways_traffic_allowed.setter
    def vitual_network_to_hub_gateways_traffic_allowed(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "vitual_network_to_hub_gateways_traffic_allowed", value)


@pulumi.input_type
class _VirtualHubConnectionState:
    def __init__(__self__, *,
                 hub_to_vitual_network_traffic_allowed: Optional[pulumi.Input[bool]] = None,
                 internet_security_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_virtual_network_id: Optional[pulumi.Input[str]] = None,
                 routing: Optional[pulumi.Input['VirtualHubConnectionRoutingArgs']] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 vitual_network_to_hub_gateways_traffic_allowed: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering VirtualHubConnection resources.
        :param pulumi.Input[bool] internet_security_enabled: Should Internet Security be enabled to secure internet traffic? Changing this forces a new resource to be created. Defaults to `false`.
        :param pulumi.Input[str] name: The Name which should be used for this Connection, which must be unique within the Virtual Hub. Changing this forces a new resource to be created.
        :param pulumi.Input[str] remote_virtual_network_id: The ID of the Virtual Network which the Virtual Hub should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input['VirtualHubConnectionRoutingArgs'] routing: A `routing` block as defined below.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub within which this connection should be created. Changing this forces a new resource to be created.
        """
        if hub_to_vitual_network_traffic_allowed is not None:
            warnings.warn("""Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""", DeprecationWarning)
            pulumi.log.warn("""hub_to_vitual_network_traffic_allowed is deprecated: Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""")
        if hub_to_vitual_network_traffic_allowed is not None:
            pulumi.set(__self__, "hub_to_vitual_network_traffic_allowed", hub_to_vitual_network_traffic_allowed)
        if internet_security_enabled is not None:
            pulumi.set(__self__, "internet_security_enabled", internet_security_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if remote_virtual_network_id is not None:
            pulumi.set(__self__, "remote_virtual_network_id", remote_virtual_network_id)
        if routing is not None:
            pulumi.set(__self__, "routing", routing)
        if virtual_hub_id is not None:
            pulumi.set(__self__, "virtual_hub_id", virtual_hub_id)
        if vitual_network_to_hub_gateways_traffic_allowed is not None:
            warnings.warn("""Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""", DeprecationWarning)
            pulumi.log.warn("""vitual_network_to_hub_gateways_traffic_allowed is deprecated: Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""")
        if vitual_network_to_hub_gateways_traffic_allowed is not None:
            pulumi.set(__self__, "vitual_network_to_hub_gateways_traffic_allowed", vitual_network_to_hub_gateways_traffic_allowed)

    @property
    @pulumi.getter(name="hubToVitualNetworkTrafficAllowed")
    def hub_to_vitual_network_traffic_allowed(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "hub_to_vitual_network_traffic_allowed")

    @hub_to_vitual_network_traffic_allowed.setter
    def hub_to_vitual_network_traffic_allowed(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hub_to_vitual_network_traffic_allowed", value)

    @property
    @pulumi.getter(name="internetSecurityEnabled")
    def internet_security_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should Internet Security be enabled to secure internet traffic? Changing this forces a new resource to be created. Defaults to `false`.
        """
        return pulumi.get(self, "internet_security_enabled")

    @internet_security_enabled.setter
    def internet_security_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "internet_security_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The Name which should be used for this Connection, which must be unique within the Virtual Hub. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="remoteVirtualNetworkId")
    def remote_virtual_network_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Virtual Network which the Virtual Hub should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "remote_virtual_network_id")

    @remote_virtual_network_id.setter
    def remote_virtual_network_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "remote_virtual_network_id", value)

    @property
    @pulumi.getter
    def routing(self) -> Optional[pulumi.Input['VirtualHubConnectionRoutingArgs']]:
        """
        A `routing` block as defined below.
        """
        return pulumi.get(self, "routing")

    @routing.setter
    def routing(self, value: Optional[pulumi.Input['VirtualHubConnectionRoutingArgs']]):
        pulumi.set(self, "routing", value)

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Virtual Hub within which this connection should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_hub_id", value)

    @property
    @pulumi.getter(name="vitualNetworkToHubGatewaysTrafficAllowed")
    def vitual_network_to_hub_gateways_traffic_allowed(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "vitual_network_to_hub_gateways_traffic_allowed")

    @vitual_network_to_hub_gateways_traffic_allowed.setter
    def vitual_network_to_hub_gateways_traffic_allowed(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "vitual_network_to_hub_gateways_traffic_allowed", value)


class VirtualHubConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hub_to_vitual_network_traffic_allowed: Optional[pulumi.Input[bool]] = None,
                 internet_security_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_virtual_network_id: Optional[pulumi.Input[str]] = None,
                 routing: Optional[pulumi.Input[pulumi.InputType['VirtualHubConnectionRoutingArgs']]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 vitual_network_to_hub_gateways_traffic_allowed: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Manages a Connection for a Virtual Hub.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["172.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        test = azure.network.VirtualWan("test",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location)
        example_virtual_hub = azure.network.VirtualHub("exampleVirtualHub",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            virtual_wan_id=azurerm_virtual_wan["example"]["id"],
            address_prefix="10.0.1.0/24")
        example_virtual_hub_connection = azure.network.VirtualHubConnection("exampleVirtualHubConnection",
            virtual_hub_id=example_virtual_hub.id,
            remote_virtual_network_id=example_virtual_network.id)
        ```

        ## Import

        Virtual Hub Connection's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/virtualHubConnection:VirtualHubConnection example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/virtualHubs/hub1/hubVirtualNetworkConnections/connection1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] internet_security_enabled: Should Internet Security be enabled to secure internet traffic? Changing this forces a new resource to be created. Defaults to `false`.
        :param pulumi.Input[str] name: The Name which should be used for this Connection, which must be unique within the Virtual Hub. Changing this forces a new resource to be created.
        :param pulumi.Input[str] remote_virtual_network_id: The ID of the Virtual Network which the Virtual Hub should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['VirtualHubConnectionRoutingArgs']] routing: A `routing` block as defined below.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub within which this connection should be created. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VirtualHubConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Connection for a Virtual Hub.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["172.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        test = azure.network.VirtualWan("test",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location)
        example_virtual_hub = azure.network.VirtualHub("exampleVirtualHub",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            virtual_wan_id=azurerm_virtual_wan["example"]["id"],
            address_prefix="10.0.1.0/24")
        example_virtual_hub_connection = azure.network.VirtualHubConnection("exampleVirtualHubConnection",
            virtual_hub_id=example_virtual_hub.id,
            remote_virtual_network_id=example_virtual_network.id)
        ```

        ## Import

        Virtual Hub Connection's can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:network/virtualHubConnection:VirtualHubConnection example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/virtualHubs/hub1/hubVirtualNetworkConnections/connection1
        ```

        :param str resource_name: The name of the resource.
        :param VirtualHubConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualHubConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hub_to_vitual_network_traffic_allowed: Optional[pulumi.Input[bool]] = None,
                 internet_security_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_virtual_network_id: Optional[pulumi.Input[str]] = None,
                 routing: Optional[pulumi.Input[pulumi.InputType['VirtualHubConnectionRoutingArgs']]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 vitual_network_to_hub_gateways_traffic_allowed: Optional[pulumi.Input[bool]] = None,
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
            __props__ = VirtualHubConnectionArgs.__new__(VirtualHubConnectionArgs)

            if hub_to_vitual_network_traffic_allowed is not None and not opts.urn:
                warnings.warn("""Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""", DeprecationWarning)
                pulumi.log.warn("""hub_to_vitual_network_traffic_allowed is deprecated: Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""")
            __props__.__dict__["hub_to_vitual_network_traffic_allowed"] = hub_to_vitual_network_traffic_allowed
            __props__.__dict__["internet_security_enabled"] = internet_security_enabled
            __props__.__dict__["name"] = name
            if remote_virtual_network_id is None and not opts.urn:
                raise TypeError("Missing required property 'remote_virtual_network_id'")
            __props__.__dict__["remote_virtual_network_id"] = remote_virtual_network_id
            __props__.__dict__["routing"] = routing
            if virtual_hub_id is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_id'")
            __props__.__dict__["virtual_hub_id"] = virtual_hub_id
            if vitual_network_to_hub_gateways_traffic_allowed is not None and not opts.urn:
                warnings.warn("""Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""", DeprecationWarning)
                pulumi.log.warn("""vitual_network_to_hub_gateways_traffic_allowed is deprecated: Due to a breaking behavioural change in the Azure API this property is no longer functional and will be removed in version 3.0 of the provider""")
            __props__.__dict__["vitual_network_to_hub_gateways_traffic_allowed"] = vitual_network_to_hub_gateways_traffic_allowed
        super(VirtualHubConnection, __self__).__init__(
            'azure:network/virtualHubConnection:VirtualHubConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            hub_to_vitual_network_traffic_allowed: Optional[pulumi.Input[bool]] = None,
            internet_security_enabled: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            remote_virtual_network_id: Optional[pulumi.Input[str]] = None,
            routing: Optional[pulumi.Input[pulumi.InputType['VirtualHubConnectionRoutingArgs']]] = None,
            virtual_hub_id: Optional[pulumi.Input[str]] = None,
            vitual_network_to_hub_gateways_traffic_allowed: Optional[pulumi.Input[bool]] = None) -> 'VirtualHubConnection':
        """
        Get an existing VirtualHubConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] internet_security_enabled: Should Internet Security be enabled to secure internet traffic? Changing this forces a new resource to be created. Defaults to `false`.
        :param pulumi.Input[str] name: The Name which should be used for this Connection, which must be unique within the Virtual Hub. Changing this forces a new resource to be created.
        :param pulumi.Input[str] remote_virtual_network_id: The ID of the Virtual Network which the Virtual Hub should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['VirtualHubConnectionRoutingArgs']] routing: A `routing` block as defined below.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub within which this connection should be created. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VirtualHubConnectionState.__new__(_VirtualHubConnectionState)

        __props__.__dict__["hub_to_vitual_network_traffic_allowed"] = hub_to_vitual_network_traffic_allowed
        __props__.__dict__["internet_security_enabled"] = internet_security_enabled
        __props__.__dict__["name"] = name
        __props__.__dict__["remote_virtual_network_id"] = remote_virtual_network_id
        __props__.__dict__["routing"] = routing
        __props__.__dict__["virtual_hub_id"] = virtual_hub_id
        __props__.__dict__["vitual_network_to_hub_gateways_traffic_allowed"] = vitual_network_to_hub_gateways_traffic_allowed
        return VirtualHubConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="hubToVitualNetworkTrafficAllowed")
    def hub_to_vitual_network_traffic_allowed(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "hub_to_vitual_network_traffic_allowed")

    @property
    @pulumi.getter(name="internetSecurityEnabled")
    def internet_security_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Should Internet Security be enabled to secure internet traffic? Changing this forces a new resource to be created. Defaults to `false`.
        """
        return pulumi.get(self, "internet_security_enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The Name which should be used for this Connection, which must be unique within the Virtual Hub. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="remoteVirtualNetworkId")
    def remote_virtual_network_id(self) -> pulumi.Output[str]:
        """
        The ID of the Virtual Network which the Virtual Hub should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "remote_virtual_network_id")

    @property
    @pulumi.getter
    def routing(self) -> pulumi.Output['outputs.VirtualHubConnectionRouting']:
        """
        A `routing` block as defined below.
        """
        return pulumi.get(self, "routing")

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> pulumi.Output[str]:
        """
        The ID of the Virtual Hub within which this connection should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @property
    @pulumi.getter(name="vitualNetworkToHubGatewaysTrafficAllowed")
    def vitual_network_to_hub_gateways_traffic_allowed(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "vitual_network_to_hub_gateways_traffic_allowed")

