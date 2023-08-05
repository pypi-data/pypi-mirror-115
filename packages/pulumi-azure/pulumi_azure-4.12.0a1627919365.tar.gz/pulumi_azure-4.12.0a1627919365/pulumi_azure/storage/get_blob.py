# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetBlobResult',
    'AwaitableGetBlobResult',
    'get_blob',
]

@pulumi.output_type
class GetBlobResult:
    """
    A collection of values returned by getBlob.
    """
    def __init__(__self__, access_tier=None, content_md5=None, content_type=None, id=None, metadata=None, name=None, storage_account_name=None, storage_container_name=None, type=None, url=None):
        if access_tier and not isinstance(access_tier, str):
            raise TypeError("Expected argument 'access_tier' to be a str")
        pulumi.set(__self__, "access_tier", access_tier)
        if content_md5 and not isinstance(content_md5, str):
            raise TypeError("Expected argument 'content_md5' to be a str")
        pulumi.set(__self__, "content_md5", content_md5)
        if content_type and not isinstance(content_type, str):
            raise TypeError("Expected argument 'content_type' to be a str")
        pulumi.set(__self__, "content_type", content_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Expected argument 'metadata' to be a dict")
        pulumi.set(__self__, "metadata", metadata)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if storage_account_name and not isinstance(storage_account_name, str):
            raise TypeError("Expected argument 'storage_account_name' to be a str")
        pulumi.set(__self__, "storage_account_name", storage_account_name)
        if storage_container_name and not isinstance(storage_container_name, str):
            raise TypeError("Expected argument 'storage_container_name' to be a str")
        pulumi.set(__self__, "storage_container_name", storage_container_name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="accessTier")
    def access_tier(self) -> str:
        """
        The access tier of the storage blob.
        """
        return pulumi.get(self, "access_tier")

    @property
    @pulumi.getter(name="contentMd5")
    def content_md5(self) -> str:
        """
        The MD5 sum of the blob contents.
        """
        return pulumi.get(self, "content_md5")

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> str:
        """
        The content type of the storage blob.
        """
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def metadata(self) -> Mapping[str, str]:
        """
        A map of custom blob metadata.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> str:
        return pulumi.get(self, "storage_account_name")

    @property
    @pulumi.getter(name="storageContainerName")
    def storage_container_name(self) -> str:
        return pulumi.get(self, "storage_container_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the storage blob
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        The URL of the storage blob.
        """
        return pulumi.get(self, "url")


class AwaitableGetBlobResult(GetBlobResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBlobResult(
            access_tier=self.access_tier,
            content_md5=self.content_md5,
            content_type=self.content_type,
            id=self.id,
            metadata=self.metadata,
            name=self.name,
            storage_account_name=self.storage_account_name,
            storage_container_name=self.storage_container_name,
            type=self.type,
            url=self.url)


def get_blob(metadata: Optional[Mapping[str, str]] = None,
             name: Optional[str] = None,
             storage_account_name: Optional[str] = None,
             storage_container_name: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBlobResult:
    """
    Use this data source to access information about an existing Storage Blob.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.storage.get_blob(name="example-blob-name",
        storage_account_name="example-storage-account-name",
        storage_container_name="example-storage-container-name")
    ```


    :param Mapping[str, str] metadata: A map of custom blob metadata.
    :param str name: The name of the Blob.
    :param str storage_account_name: The name of the Storage Account where the Container exists.
    :param str storage_container_name: The name of the Storage Container where the Blob exists.
    """
    __args__ = dict()
    __args__['metadata'] = metadata
    __args__['name'] = name
    __args__['storageAccountName'] = storage_account_name
    __args__['storageContainerName'] = storage_container_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:storage/getBlob:getBlob', __args__, opts=opts, typ=GetBlobResult).value

    return AwaitableGetBlobResult(
        access_tier=__ret__.access_tier,
        content_md5=__ret__.content_md5,
        content_type=__ret__.content_type,
        id=__ret__.id,
        metadata=__ret__.metadata,
        name=__ret__.name,
        storage_account_name=__ret__.storage_account_name,
        storage_container_name=__ret__.storage_container_name,
        type=__ret__.type,
        url=__ret__.url)
