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
    'GetSharedImageResult',
    'AwaitableGetSharedImageResult',
    'get_shared_image',
]

@pulumi.output_type
class GetSharedImageResult:
    """
    A collection of values returned by getSharedImage.
    """
    def __init__(__self__, description=None, eula=None, gallery_name=None, hyper_v_generation=None, id=None, identifiers=None, location=None, name=None, os_type=None, privacy_statement_uri=None, release_note_uri=None, resource_group_name=None, specialized=None, tags=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if eula and not isinstance(eula, str):
            raise TypeError("Expected argument 'eula' to be a str")
        pulumi.set(__self__, "eula", eula)
        if gallery_name and not isinstance(gallery_name, str):
            raise TypeError("Expected argument 'gallery_name' to be a str")
        pulumi.set(__self__, "gallery_name", gallery_name)
        if hyper_v_generation and not isinstance(hyper_v_generation, str):
            raise TypeError("Expected argument 'hyper_v_generation' to be a str")
        pulumi.set(__self__, "hyper_v_generation", hyper_v_generation)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifiers and not isinstance(identifiers, list):
            raise TypeError("Expected argument 'identifiers' to be a list")
        pulumi.set(__self__, "identifiers", identifiers)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if os_type and not isinstance(os_type, str):
            raise TypeError("Expected argument 'os_type' to be a str")
        pulumi.set(__self__, "os_type", os_type)
        if privacy_statement_uri and not isinstance(privacy_statement_uri, str):
            raise TypeError("Expected argument 'privacy_statement_uri' to be a str")
        pulumi.set(__self__, "privacy_statement_uri", privacy_statement_uri)
        if release_note_uri and not isinstance(release_note_uri, str):
            raise TypeError("Expected argument 'release_note_uri' to be a str")
        pulumi.set(__self__, "release_note_uri", release_note_uri)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if specialized and not isinstance(specialized, bool):
            raise TypeError("Expected argument 'specialized' to be a bool")
        pulumi.set(__self__, "specialized", specialized)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of this Shared Image.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def eula(self) -> str:
        """
        The End User Licence Agreement for the Shared Image.
        """
        return pulumi.get(self, "eula")

    @property
    @pulumi.getter(name="galleryName")
    def gallery_name(self) -> str:
        return pulumi.get(self, "gallery_name")

    @property
    @pulumi.getter(name="hyperVGeneration")
    def hyper_v_generation(self) -> str:
        """
        The generation of HyperV that the Virtual Machine used to create the Shared Image is based on.
        """
        return pulumi.get(self, "hyper_v_generation")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identifiers(self) -> Sequence['outputs.GetSharedImageIdentifierResult']:
        """
        An `identifier` block as defined below.
        """
        return pulumi.get(self, "identifiers")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The supported Azure location where the Shared Image Gallery exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> str:
        """
        The type of Operating System present in this Shared Image.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="privacyStatementUri")
    def privacy_statement_uri(self) -> str:
        """
        The URI containing the Privacy Statement for this Shared Image.
        """
        return pulumi.get(self, "privacy_statement_uri")

    @property
    @pulumi.getter(name="releaseNoteUri")
    def release_note_uri(self) -> str:
        """
        The URI containing the Release Notes for this Shared Image.
        """
        return pulumi.get(self, "release_note_uri")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def specialized(self) -> bool:
        """
        Specifies that the Operating System used inside this Image has not been Generalized (for example, `sysprep` on Windows has not been run).
        """
        return pulumi.get(self, "specialized")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the Shared Image.
        """
        return pulumi.get(self, "tags")


class AwaitableGetSharedImageResult(GetSharedImageResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSharedImageResult(
            description=self.description,
            eula=self.eula,
            gallery_name=self.gallery_name,
            hyper_v_generation=self.hyper_v_generation,
            id=self.id,
            identifiers=self.identifiers,
            location=self.location,
            name=self.name,
            os_type=self.os_type,
            privacy_statement_uri=self.privacy_statement_uri,
            release_note_uri=self.release_note_uri,
            resource_group_name=self.resource_group_name,
            specialized=self.specialized,
            tags=self.tags)


def get_shared_image(gallery_name: Optional[str] = None,
                     name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSharedImageResult:
    """
    Use this data source to access information about an existing Shared Image within a Shared Image Gallery.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_shared_image(gallery_name="my-image-gallery",
        name="my-image",
        resource_group_name="example-resources")
    ```


    :param str gallery_name: The name of the Shared Image Gallery in which the Shared Image exists.
    :param str name: The name of the Shared Image.
    :param str resource_group_name: The name of the Resource Group in which the Shared Image Gallery exists.
    """
    __args__ = dict()
    __args__['galleryName'] = gallery_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:compute/getSharedImage:getSharedImage', __args__, opts=opts, typ=GetSharedImageResult).value

    return AwaitableGetSharedImageResult(
        description=__ret__.description,
        eula=__ret__.eula,
        gallery_name=__ret__.gallery_name,
        hyper_v_generation=__ret__.hyper_v_generation,
        id=__ret__.id,
        identifiers=__ret__.identifiers,
        location=__ret__.location,
        name=__ret__.name,
        os_type=__ret__.os_type,
        privacy_statement_uri=__ret__.privacy_statement_uri,
        release_note_uri=__ret__.release_note_uri,
        resource_group_name=__ret__.resource_group_name,
        specialized=__ret__.specialized,
        tags=__ret__.tags)
