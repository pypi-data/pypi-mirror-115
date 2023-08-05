# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetDedicatedHostGroupResult',
    'AwaitableGetDedicatedHostGroupResult',
    'get_dedicated_host_group',
]

@pulumi.output_type
class GetDedicatedHostGroupResult:
    """
    A collection of values returned by getDedicatedHostGroup.
    """
    def __init__(__self__, automatic_placement_enabled=None, id=None, location=None, name=None, platform_fault_domain_count=None, resource_group_name=None, tags=None, zones=None):
        if automatic_placement_enabled and not isinstance(automatic_placement_enabled, bool):
            raise TypeError("Expected argument 'automatic_placement_enabled' to be a bool")
        pulumi.set(__self__, "automatic_placement_enabled", automatic_placement_enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if platform_fault_domain_count and not isinstance(platform_fault_domain_count, int):
            raise TypeError("Expected argument 'platform_fault_domain_count' to be a int")
        pulumi.set(__self__, "platform_fault_domain_count", platform_fault_domain_count)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="automaticPlacementEnabled")
    def automatic_placement_enabled(self) -> bool:
        """
        Whether virtual machines or virtual machine scale sets be placed automatically on this Dedicated Host Group.
        """
        return pulumi.get(self, "automatic_placement_enabled")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure location where the Dedicated Host Group exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="platformFaultDomainCount")
    def platform_fault_domain_count(self) -> int:
        """
        The number of fault domains that the Dedicated Host Group spans.
        """
        return pulumi.get(self, "platform_fault_domain_count")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        """
        The Availability Zones in which this Dedicated Host Group is located.
        """
        return pulumi.get(self, "zones")


class AwaitableGetDedicatedHostGroupResult(GetDedicatedHostGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDedicatedHostGroupResult(
            automatic_placement_enabled=self.automatic_placement_enabled,
            id=self.id,
            location=self.location,
            name=self.name,
            platform_fault_domain_count=self.platform_fault_domain_count,
            resource_group_name=self.resource_group_name,
            tags=self.tags,
            zones=self.zones)


def get_dedicated_host_group(name: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDedicatedHostGroupResult:
    """
    Use this data source to access information about an existing Dedicated Host Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_dedicated_host_group(name="example-dedicated-host-group",
        resource_group_name="example-rg")
    pulumi.export("id", example.id)
    ```


    :param str name: Specifies the name of the Dedicated Host Group.
    :param str resource_group_name: Specifies the name of the resource group the Dedicated Host Group is located in.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:compute/getDedicatedHostGroup:getDedicatedHostGroup', __args__, opts=opts, typ=GetDedicatedHostGroupResult).value

    return AwaitableGetDedicatedHostGroupResult(
        automatic_placement_enabled=__ret__.automatic_placement_enabled,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        platform_fault_domain_count=__ret__.platform_fault_domain_count,
        resource_group_name=__ret__.resource_group_name,
        tags=__ret__.tags,
        zones=__ret__.zones)
