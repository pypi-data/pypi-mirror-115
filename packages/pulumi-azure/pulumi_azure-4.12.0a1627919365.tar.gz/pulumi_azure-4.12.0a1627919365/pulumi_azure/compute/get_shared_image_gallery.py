# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetSharedImageGalleryResult',
    'AwaitableGetSharedImageGalleryResult',
    'get_shared_image_gallery',
]

@pulumi.output_type
class GetSharedImageGalleryResult:
    """
    A collection of values returned by getSharedImageGallery.
    """
    def __init__(__self__, description=None, id=None, location=None, name=None, resource_group_name=None, tags=None, unique_name=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if unique_name and not isinstance(unique_name, str):
            raise TypeError("Expected argument 'unique_name' to be a str")
        pulumi.set(__self__, "unique_name", unique_name)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        A description for the Shared Image Gallery.
        """
        return pulumi.get(self, "description")

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
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags which are assigned to the Shared Image Gallery.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="uniqueName")
    def unique_name(self) -> str:
        """
        The unique name assigned to the Shared Image Gallery.
        """
        return pulumi.get(self, "unique_name")


class AwaitableGetSharedImageGalleryResult(GetSharedImageGalleryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSharedImageGalleryResult(
            description=self.description,
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            tags=self.tags,
            unique_name=self.unique_name)


def get_shared_image_gallery(name: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSharedImageGalleryResult:
    """
    Use this data source to access information about an existing Shared Image Gallery.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_shared_image_gallery(name="my-image-gallery",
        resource_group_name="example-resources")
    ```


    :param str name: The name of the Shared Image Gallery.
    :param str resource_group_name: The name of the Resource Group in which the Shared Image Gallery exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:compute/getSharedImageGallery:getSharedImageGallery', __args__, opts=opts, typ=GetSharedImageGalleryResult).value

    return AwaitableGetSharedImageGalleryResult(
        description=__ret__.description,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        tags=__ret__.tags,
        unique_name=__ret__.unique_name)
