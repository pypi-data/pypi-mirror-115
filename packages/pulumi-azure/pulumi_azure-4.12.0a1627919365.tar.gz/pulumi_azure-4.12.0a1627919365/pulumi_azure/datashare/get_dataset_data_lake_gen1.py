# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetDatasetDataLakeGen1Result',
    'AwaitableGetDatasetDataLakeGen1Result',
    'get_dataset_data_lake_gen1',
]

@pulumi.output_type
class GetDatasetDataLakeGen1Result:
    """
    A collection of values returned by getDatasetDataLakeGen1.
    """
    def __init__(__self__, data_lake_store_id=None, data_share_id=None, display_name=None, file_name=None, folder_path=None, id=None, name=None):
        if data_lake_store_id and not isinstance(data_lake_store_id, str):
            raise TypeError("Expected argument 'data_lake_store_id' to be a str")
        pulumi.set(__self__, "data_lake_store_id", data_lake_store_id)
        if data_share_id and not isinstance(data_share_id, str):
            raise TypeError("Expected argument 'data_share_id' to be a str")
        pulumi.set(__self__, "data_share_id", data_share_id)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if file_name and not isinstance(file_name, str):
            raise TypeError("Expected argument 'file_name' to be a str")
        pulumi.set(__self__, "file_name", file_name)
        if folder_path and not isinstance(folder_path, str):
            raise TypeError("Expected argument 'folder_path' to be a str")
        pulumi.set(__self__, "folder_path", folder_path)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="dataLakeStoreId")
    def data_lake_store_id(self) -> str:
        """
        The resource ID of the Data Lake Store to be shared with the receiver.
        """
        return pulumi.get(self, "data_lake_store_id")

    @property
    @pulumi.getter(name="dataShareId")
    def data_share_id(self) -> str:
        return pulumi.get(self, "data_share_id")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The displayed name of the Data Share Dataset.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="fileName")
    def file_name(self) -> str:
        """
        The file name of the data lake store to be shared with the receiver.
        """
        return pulumi.get(self, "file_name")

    @property
    @pulumi.getter(name="folderPath")
    def folder_path(self) -> str:
        """
        The folder path of the data lake store to be shared with the receiver.
        """
        return pulumi.get(self, "folder_path")

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


class AwaitableGetDatasetDataLakeGen1Result(GetDatasetDataLakeGen1Result):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatasetDataLakeGen1Result(
            data_lake_store_id=self.data_lake_store_id,
            data_share_id=self.data_share_id,
            display_name=self.display_name,
            file_name=self.file_name,
            folder_path=self.folder_path,
            id=self.id,
            name=self.name)


def get_dataset_data_lake_gen1(data_share_id: Optional[str] = None,
                               name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDatasetDataLakeGen1Result:
    """
    Use this data source to access information about an existing DataShareDataLakeGen1Dataset.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.datashare.get_dataset_data_lake_gen1(name="example-dsdsdlg1",
        data_share_id="example-share-id")
    pulumi.export("id", example.id)
    ```


    :param str data_share_id: The resource ID of the Data Share where this Data Share Data Lake Gen1 Dataset should be created.
    :param str name: The name of the Data Share Data Lake Gen1 Dataset.
    """
    __args__ = dict()
    __args__['dataShareId'] = data_share_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:datashare/getDatasetDataLakeGen1:getDatasetDataLakeGen1', __args__, opts=opts, typ=GetDatasetDataLakeGen1Result).value

    return AwaitableGetDatasetDataLakeGen1Result(
        data_lake_store_id=__ret__.data_lake_store_id,
        data_share_id=__ret__.data_share_id,
        display_name=__ret__.display_name,
        file_name=__ret__.file_name,
        folder_path=__ret__.folder_path,
        id=__ret__.id,
        name=__ret__.name)
