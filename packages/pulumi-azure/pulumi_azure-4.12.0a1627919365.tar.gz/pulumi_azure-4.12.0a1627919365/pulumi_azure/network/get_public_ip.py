# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetPublicIPResult',
    'AwaitableGetPublicIPResult',
    'get_public_ip',
]

@pulumi.output_type
class GetPublicIPResult:
    """
    A collection of values returned by getPublicIP.
    """
    def __init__(__self__, allocation_method=None, domain_name_label=None, fqdn=None, id=None, idle_timeout_in_minutes=None, ip_address=None, ip_tags=None, ip_version=None, location=None, name=None, resource_group_name=None, reverse_fqdn=None, sku=None, tags=None, zones=None):
        if allocation_method and not isinstance(allocation_method, str):
            raise TypeError("Expected argument 'allocation_method' to be a str")
        pulumi.set(__self__, "allocation_method", allocation_method)
        if domain_name_label and not isinstance(domain_name_label, str):
            raise TypeError("Expected argument 'domain_name_label' to be a str")
        pulumi.set(__self__, "domain_name_label", domain_name_label)
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if idle_timeout_in_minutes and not isinstance(idle_timeout_in_minutes, int):
            raise TypeError("Expected argument 'idle_timeout_in_minutes' to be a int")
        pulumi.set(__self__, "idle_timeout_in_minutes", idle_timeout_in_minutes)
        if ip_address and not isinstance(ip_address, str):
            raise TypeError("Expected argument 'ip_address' to be a str")
        pulumi.set(__self__, "ip_address", ip_address)
        if ip_tags and not isinstance(ip_tags, dict):
            raise TypeError("Expected argument 'ip_tags' to be a dict")
        pulumi.set(__self__, "ip_tags", ip_tags)
        if ip_version and not isinstance(ip_version, str):
            raise TypeError("Expected argument 'ip_version' to be a str")
        pulumi.set(__self__, "ip_version", ip_version)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if reverse_fqdn and not isinstance(reverse_fqdn, str):
            raise TypeError("Expected argument 'reverse_fqdn' to be a str")
        pulumi.set(__self__, "reverse_fqdn", reverse_fqdn)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="allocationMethod")
    def allocation_method(self) -> str:
        return pulumi.get(self, "allocation_method")

    @property
    @pulumi.getter(name="domainNameLabel")
    def domain_name_label(self) -> str:
        """
        The label for the Domain Name.
        """
        return pulumi.get(self, "domain_name_label")

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        Fully qualified domain name of the A DNS record associated with the public IP. This is the concatenation of the domainNameLabel and the regionalized DNS zone.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="idleTimeoutInMinutes")
    def idle_timeout_in_minutes(self) -> int:
        """
        Specifies the timeout for the TCP idle connection.
        """
        return pulumi.get(self, "idle_timeout_in_minutes")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        The IP address value that was allocated.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="ipTags")
    def ip_tags(self) -> Mapping[str, str]:
        """
        A mapping of tags to assigned to the resource.
        """
        return pulumi.get(self, "ip_tags")

    @property
    @pulumi.getter(name="ipVersion")
    def ip_version(self) -> str:
        """
        The IP version being used, for example `IPv4` or `IPv6`.
        """
        return pulumi.get(self, "ip_version")

    @property
    @pulumi.getter
    def location(self) -> str:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="reverseFqdn")
    def reverse_fqdn(self) -> str:
        return pulumi.get(self, "reverse_fqdn")

    @property
    @pulumi.getter
    def sku(self) -> str:
        """
        The SKU of the Public IP.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        A mapping of tags to assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        return pulumi.get(self, "zones")


class AwaitableGetPublicIPResult(GetPublicIPResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPublicIPResult(
            allocation_method=self.allocation_method,
            domain_name_label=self.domain_name_label,
            fqdn=self.fqdn,
            id=self.id,
            idle_timeout_in_minutes=self.idle_timeout_in_minutes,
            ip_address=self.ip_address,
            ip_tags=self.ip_tags,
            ip_version=self.ip_version,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            reverse_fqdn=self.reverse_fqdn,
            sku=self.sku,
            tags=self.tags,
            zones=self.zones)


def get_public_ip(name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  tags: Optional[Mapping[str, str]] = None,
                  zones: Optional[Sequence[str]] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPublicIPResult:
    """
    Use this data source to access information about an existing Public IP Address.

    ## Example Usage
    ### Reference An Existing)

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_public_ip(name="name_of_public_ip",
        resource_group_name="name_of_resource_group")
    pulumi.export("domainNameLabel", example.domain_name_label)
    pulumi.export("publicIpAddress", example.ip_address)
    ```
    ### Retrieve The Dynamic Public IP Of A New VM)

    ```python
    import pulumi
    import pulumi_azure as azure

    example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
    example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
        address_spaces=["10.0.0.0/16"],
        location=example_resource_group.location,
        resource_group_name=example_resource_group.name)
    example_subnet = azure.network.Subnet("exampleSubnet",
        resource_group_name=example_resource_group.name,
        virtual_network_name=example_virtual_network.name,
        address_prefixes=["10.0.2.0/24"])
    example_public_ip = azure.network.PublicIp("examplePublicIp",
        location=example_resource_group.location,
        resource_group_name=example_resource_group.name,
        allocation_method="Dynamic",
        idle_timeout_in_minutes=30,
        tags={
            "environment": "test",
        })
    example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
        location=example_resource_group.location,
        resource_group_name=example_resource_group.name,
        ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
            name="testconfiguration1",
            subnet_id=example_subnet.id,
            private_ip_address_allocation="Static",
            private_ip_address="10.0.2.5",
            public_ip_address_id=example_public_ip.id,
        )])
    example_virtual_machine = azure.compute.VirtualMachine("exampleVirtualMachine",
        location=example_resource_group.location,
        resource_group_name=example_resource_group.name,
        network_interface_ids=[example_network_interface.id])
    # ...
    example_public_ip = pulumi.Output.all(example_public_ip.name, example_virtual_machine.resource_group_name).apply(lambda name, resource_group_name: azure.network.get_public_ip(name=name,
        resource_group_name=resource_group_name))
    pulumi.export("publicIpAddress", example_public_ip.ip_address)
    ```


    :param str name: Specifies the name of the public IP address.
    :param str resource_group_name: Specifies the name of the resource group.
    :param Mapping[str, str] tags: A mapping of tags to assigned to the resource.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['tags'] = tags
    __args__['zones'] = zones
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:network/getPublicIP:getPublicIP', __args__, opts=opts, typ=GetPublicIPResult).value

    return AwaitableGetPublicIPResult(
        allocation_method=__ret__.allocation_method,
        domain_name_label=__ret__.domain_name_label,
        fqdn=__ret__.fqdn,
        id=__ret__.id,
        idle_timeout_in_minutes=__ret__.idle_timeout_in_minutes,
        ip_address=__ret__.ip_address,
        ip_tags=__ret__.ip_tags,
        ip_version=__ret__.ip_version,
        location=__ret__.location,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        reverse_fqdn=__ret__.reverse_fqdn,
        sku=__ret__.sku,
        tags=__ret__.tags,
        zones=__ret__.zones)
