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
    'GetConfigurationResult',
    'AwaitableGetConfigurationResult',
    'get_configuration',
]

@pulumi.output_type
class GetConfigurationResult:
    """
    A collection of values returned by getConfiguration.
    """
    def __init__(__self__, id=None, location=None, name=None, properties=None, resource_group_name=None, scope=None, tags=None, visibility=None, windows=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if scope and not isinstance(scope, str):
            raise TypeError("Expected argument 'scope' to be a str")
        pulumi.set(__self__, "scope", scope)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if visibility and not isinstance(visibility, str):
            raise TypeError("Expected argument 'visibility' to be a str")
        pulumi.set(__self__, "visibility", visibility)
        if windows and not isinstance(windows, list):
            raise TypeError("Expected argument 'windows' to be a list")
        pulumi.set(__self__, "windows", windows)

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
        The Azure location where the resource exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> Mapping[str, str]:
        """
        The properties assigned to the resource.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def scope(self) -> str:
        """
        The scope of the Maintenance Configuration.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def visibility(self) -> str:
        """
        The visibility of the Maintenance Configuration.
        """
        return pulumi.get(self, "visibility")

    @property
    @pulumi.getter
    def windows(self) -> Sequence['outputs.GetConfigurationWindowResult']:
        """
        A `window` block as defined below.
        """
        return pulumi.get(self, "windows")


class AwaitableGetConfigurationResult(GetConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationResult(
            id=self.id,
            location=self.location,
            name=self.name,
            properties=self.properties,
            resource_group_name=self.resource_group_name,
            scope=self.scope,
            tags=self.tags,
            visibility=self.visibility,
            windows=self.windows)


def get_configuration(name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConfigurationResult:
    """
    Use this data source to access information about an existing Maintenance Configuration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    existing = azure.maintenance.get_configuration(name="example-mc",
        resource_group_name="example-resources")
    pulumi.export("id", azurerm_maintenance_configuration["existing"]["id"])
    ```


    :param str name: Specifies the name of the Maintenance Configuration.
    :param str resource_group_name: Specifies the name of the Resource Group where this Maintenance Configuration exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:maintenance/getConfiguration:getConfiguration', __args__, opts=opts, typ=GetConfigurationResult).value

    return AwaitableGetConfigurationResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        properties=__ret__.properties,
        resource_group_name=__ret__.resource_group_name,
        scope=__ret__.scope,
        tags=__ret__.tags,
        visibility=__ret__.visibility,
        windows=__ret__.windows)
