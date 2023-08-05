# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetVirtualMachineScaleSetResult',
    'AwaitableGetVirtualMachineScaleSetResult',
    'get_virtual_machine_scale_set',
]

@pulumi.output_type
class GetVirtualMachineScaleSetResult:
    """
    A collection of values returned by getVirtualMachineScaleSet.
    """
    def __init__(__self__, id=None, identities=None, location=None, name=None, network_interfaces=None, resource_group_name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        pulumi.set(__self__, "identities", identities)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetVirtualMachineScaleSetIdentityResult']:
        """
        A `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter
    def location(self) -> str:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the public ip address configuration
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Sequence['outputs.GetVirtualMachineScaleSetNetworkInterfaceResult']:
        """
        A list of `network_interface` blocks as defined below.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")


class AwaitableGetVirtualMachineScaleSetResult(GetVirtualMachineScaleSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualMachineScaleSetResult(
            id=self.id,
            identities=self.identities,
            location=self.location,
            name=self.name,
            network_interfaces=self.network_interfaces,
            resource_group_name=self.resource_group_name)


def get_virtual_machine_scale_set(name: Optional[str] = None,
                                  resource_group_name: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualMachineScaleSetResult:
    """
    Use this data source to access information about an existing Virtual Machine Scale Set.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_virtual_machine_scale_set(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Virtual Machine Scale Set.
    :param str resource_group_name: The name of the Resource Group where the Virtual Machine Scale Set exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:compute/getVirtualMachineScaleSet:getVirtualMachineScaleSet', __args__, opts=opts, typ=GetVirtualMachineScaleSetResult).value

    return AwaitableGetVirtualMachineScaleSetResult(
        id=__ret__.id,
        identities=__ret__.identities,
        location=__ret__.location,
        name=__ret__.name,
        network_interfaces=__ret__.network_interfaces,
        resource_group_name=__ret__.resource_group_name)
