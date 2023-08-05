# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetEnrollmentAccountScopeResult',
    'AwaitableGetEnrollmentAccountScopeResult',
    'get_enrollment_account_scope',
]

@pulumi.output_type
class GetEnrollmentAccountScopeResult:
    """
    A collection of values returned by getEnrollmentAccountScope.
    """
    def __init__(__self__, billing_account_name=None, enrollment_account_name=None, id=None):
        if billing_account_name and not isinstance(billing_account_name, str):
            raise TypeError("Expected argument 'billing_account_name' to be a str")
        pulumi.set(__self__, "billing_account_name", billing_account_name)
        if enrollment_account_name and not isinstance(enrollment_account_name, str):
            raise TypeError("Expected argument 'enrollment_account_name' to be a str")
        pulumi.set(__self__, "enrollment_account_name", enrollment_account_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="billingAccountName")
    def billing_account_name(self) -> str:
        return pulumi.get(self, "billing_account_name")

    @property
    @pulumi.getter(name="enrollmentAccountName")
    def enrollment_account_name(self) -> str:
        return pulumi.get(self, "enrollment_account_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetEnrollmentAccountScopeResult(GetEnrollmentAccountScopeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEnrollmentAccountScopeResult(
            billing_account_name=self.billing_account_name,
            enrollment_account_name=self.enrollment_account_name,
            id=self.id)


def get_enrollment_account_scope(billing_account_name: Optional[str] = None,
                                 enrollment_account_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEnrollmentAccountScopeResult:
    """
    Use this data source to access information about an existing Enrollment Account Billing Scope.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.billing.get_enrollment_account_scope(billing_account_name="existing",
        enrollment_account_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str billing_account_name: The Billing Account Name of the Enterprise Account.
    :param str enrollment_account_name: The Enrollment Account Name in the above Enterprise Account.
    """
    __args__ = dict()
    __args__['billingAccountName'] = billing_account_name
    __args__['enrollmentAccountName'] = enrollment_account_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:billing/getEnrollmentAccountScope:getEnrollmentAccountScope', __args__, opts=opts, typ=GetEnrollmentAccountScopeResult).value

    return AwaitableGetEnrollmentAccountScopeResult(
        billing_account_name=__ret__.billing_account_name,
        enrollment_account_name=__ret__.enrollment_account_name,
        id=__ret__.id)
