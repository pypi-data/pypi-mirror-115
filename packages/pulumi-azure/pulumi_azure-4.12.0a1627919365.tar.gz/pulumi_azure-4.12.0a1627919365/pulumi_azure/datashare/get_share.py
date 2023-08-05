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
    'GetShareResult',
    'AwaitableGetShareResult',
    'get_share',
]

@pulumi.output_type
class GetShareResult:
    """
    A collection of values returned by getShare.
    """
    def __init__(__self__, account_id=None, description=None, id=None, kind=None, name=None, snapshot_schedules=None, terms=None):
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        pulumi.set(__self__, "account_id", account_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if snapshot_schedules and not isinstance(snapshot_schedules, list):
            raise TypeError("Expected argument 'snapshot_schedules' to be a list")
        pulumi.set(__self__, "snapshot_schedules", snapshot_schedules)
        if terms and not isinstance(terms, str):
            raise TypeError("Expected argument 'terms' to be a str")
        pulumi.set(__self__, "terms", terms)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the Data Share.
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
    def kind(self) -> str:
        """
        The kind of the Data Share.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the snapshot schedule.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="snapshotSchedules")
    def snapshot_schedules(self) -> Sequence['outputs.GetShareSnapshotScheduleResult']:
        """
        A `snapshot_schedule` block as defined below.
        """
        return pulumi.get(self, "snapshot_schedules")

    @property
    @pulumi.getter
    def terms(self) -> str:
        """
        The terms of the Data Share.
        """
        return pulumi.get(self, "terms")


class AwaitableGetShareResult(GetShareResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetShareResult(
            account_id=self.account_id,
            description=self.description,
            id=self.id,
            kind=self.kind,
            name=self.name,
            snapshot_schedules=self.snapshot_schedules,
            terms=self.terms)


def get_share(account_id: Optional[str] = None,
              name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetShareResult:
    """
    Use this data source to access information about an existing Data Share.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example_account = azure.datashare.get_account(name="example-account",
        resource_group_name="example-resource-group")
    example_share = azure.datashare.get_share(name="existing",
        account_id=example_account.id)
    pulumi.export("id", example_share.id)
    ```


    :param str account_id: The ID of the Data Share account in which the Data Share is created.
    :param str name: The name of this Data Share.
    """
    __args__ = dict()
    __args__['accountId'] = account_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:datashare/getShare:getShare', __args__, opts=opts, typ=GetShareResult).value

    return AwaitableGetShareResult(
        account_id=__ret__.account_id,
        description=__ret__.description,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        snapshot_schedules=__ret__.snapshot_schedules,
        terms=__ret__.terms)
