# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetTemplateSpecVersionResult',
    'AwaitableGetTemplateSpecVersionResult',
    'get_template_spec_version',
]

@pulumi.output_type
class GetTemplateSpecVersionResult:
    """
    A collection of values returned by getTemplateSpecVersion.
    """
    def __init__(__self__, id=None, name=None, resource_group_name=None, tags=None, template_body=None, version=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if template_body and not isinstance(template_body, str):
            raise TypeError("Expected argument 'template_body' to be a str")
        pulumi.set(__self__, "template_body", template_body)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

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
        A mapping of tags assigned to the Template.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="templateBody")
    def template_body(self) -> str:
        """
        The ARM Template body of the Template Spec Version.
        """
        return pulumi.get(self, "template_body")

    @property
    @pulumi.getter
    def version(self) -> str:
        return pulumi.get(self, "version")


class AwaitableGetTemplateSpecVersionResult(GetTemplateSpecVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTemplateSpecVersionResult(
            id=self.id,
            name=self.name,
            resource_group_name=self.resource_group_name,
            tags=self.tags,
            template_body=self.template_body,
            version=self.version)


def get_template_spec_version(name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              version: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTemplateSpecVersionResult:
    """
    Use this data source to access information about an existing Template Spec Version.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.core.get_template_spec_version(name="exampleTemplateSpec",
        resource_group_name="MyResourceGroup",
        version="v1.0.4")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Template Spec.
    :param str resource_group_name: The name of the Resource Group where the Template Spec exists.
    :param str version: The Version Name of the Template Spec.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['version'] = version
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:core/getTemplateSpecVersion:getTemplateSpecVersion', __args__, opts=opts, typ=GetTemplateSpecVersionResult).value

    return AwaitableGetTemplateSpecVersionResult(
        id=__ret__.id,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        tags=__ret__.tags,
        template_body=__ret__.template_body,
        version=__ret__.version)
