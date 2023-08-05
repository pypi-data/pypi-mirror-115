# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetClusterResult',
    'AwaitableGetClusterResult',
    'get_cluster',
]

@pulumi.output_type
class GetClusterResult:
    """
    A collection of values returned by getCluster.
    """
    def __init__(__self__, data_ingestion_uri=None, id=None, location=None, name=None, resource_group_name=None, tags=None, uri=None):
        if data_ingestion_uri and not isinstance(data_ingestion_uri, str):
            raise TypeError("Expected argument 'data_ingestion_uri' to be a str")
        pulumi.set(__self__, "data_ingestion_uri", data_ingestion_uri)
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
        if uri and not isinstance(uri, str):
            raise TypeError("Expected argument 'uri' to be a str")
        pulumi.set(__self__, "uri", uri)

    @property
    @pulumi.getter(name="dataIngestionUri")
    def data_ingestion_uri(self) -> str:
        """
        The Kusto Cluster URI to be used for data ingestion.
        """
        return pulumi.get(self, "data_ingestion_uri")

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
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The FQDN of the Azure Kusto Cluster.
        """
        return pulumi.get(self, "uri")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            data_ingestion_uri=self.data_ingestion_uri,
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            tags=self.tags,
            uri=self.uri)


def get_cluster(name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    Use this data source to access information about an existing Kusto (also known as Azure Data Explorer) Cluster

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.kusto.get_cluster(name="kustocluster",
        resource_group_name="test_resource_group")
    ```


    :param str name: Specifies the name of the Kusto Cluster.
    :param str resource_group_name: The name of the Resource Group where the Kusto Cluster exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:kusto/getCluster:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        data_ingestion_uri=__ret__.data_ingestion_uri,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        tags=__ret__.tags,
        uri=__ret__.uri)
