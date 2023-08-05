# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AutoProvisioningArgs', 'AutoProvisioning']

@pulumi.input_type
class AutoProvisioningArgs:
    def __init__(__self__, *,
                 auto_provision: pulumi.Input[str]):
        """
        The set of arguments for constructing a AutoProvisioning resource.
        :param pulumi.Input[str] auto_provision: Should the security agent be automatically provisioned on Virtual Machines in this subscription? Possible values are `On` (to install the security agent automatically, if it's missing) or `Off` (to not install the security agent automatically).
        """
        pulumi.set(__self__, "auto_provision", auto_provision)

    @property
    @pulumi.getter(name="autoProvision")
    def auto_provision(self) -> pulumi.Input[str]:
        """
        Should the security agent be automatically provisioned on Virtual Machines in this subscription? Possible values are `On` (to install the security agent automatically, if it's missing) or `Off` (to not install the security agent automatically).
        """
        return pulumi.get(self, "auto_provision")

    @auto_provision.setter
    def auto_provision(self, value: pulumi.Input[str]):
        pulumi.set(self, "auto_provision", value)


@pulumi.input_type
class _AutoProvisioningState:
    def __init__(__self__, *,
                 auto_provision: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AutoProvisioning resources.
        :param pulumi.Input[str] auto_provision: Should the security agent be automatically provisioned on Virtual Machines in this subscription? Possible values are `On` (to install the security agent automatically, if it's missing) or `Off` (to not install the security agent automatically).
        """
        if auto_provision is not None:
            pulumi.set(__self__, "auto_provision", auto_provision)

    @property
    @pulumi.getter(name="autoProvision")
    def auto_provision(self) -> Optional[pulumi.Input[str]]:
        """
        Should the security agent be automatically provisioned on Virtual Machines in this subscription? Possible values are `On` (to install the security agent automatically, if it's missing) or `Off` (to not install the security agent automatically).
        """
        return pulumi.get(self, "auto_provision")

    @auto_provision.setter
    def auto_provision(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auto_provision", value)


class AutoProvisioning(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_provision: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Enables or disables the Security Center Auto Provisioning feature for the subscription

        > **NOTE:** There is no resource name required, it will always be "default"

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.securitycenter.AutoProvisioning("example", auto_provision="On")
        ```

        ## Import

        Security Center Auto Provisioning can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:securitycenter/autoProvisioning:AutoProvisioning example /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Security/autoProvisioningSettings/default
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auto_provision: Should the security agent be automatically provisioned on Virtual Machines in this subscription? Possible values are `On` (to install the security agent automatically, if it's missing) or `Off` (to not install the security agent automatically).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AutoProvisioningArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Enables or disables the Security Center Auto Provisioning feature for the subscription

        > **NOTE:** There is no resource name required, it will always be "default"

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.securitycenter.AutoProvisioning("example", auto_provision="On")
        ```

        ## Import

        Security Center Auto Provisioning can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:securitycenter/autoProvisioning:AutoProvisioning example /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Security/autoProvisioningSettings/default
        ```

        :param str resource_name: The name of the resource.
        :param AutoProvisioningArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AutoProvisioningArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_provision: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AutoProvisioningArgs.__new__(AutoProvisioningArgs)

            if auto_provision is None and not opts.urn:
                raise TypeError("Missing required property 'auto_provision'")
            __props__.__dict__["auto_provision"] = auto_provision
        super(AutoProvisioning, __self__).__init__(
            'azure:securitycenter/autoProvisioning:AutoProvisioning',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            auto_provision: Optional[pulumi.Input[str]] = None) -> 'AutoProvisioning':
        """
        Get an existing AutoProvisioning resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auto_provision: Should the security agent be automatically provisioned on Virtual Machines in this subscription? Possible values are `On` (to install the security agent automatically, if it's missing) or `Off` (to not install the security agent automatically).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AutoProvisioningState.__new__(_AutoProvisioningState)

        __props__.__dict__["auto_provision"] = auto_provision
        return AutoProvisioning(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoProvision")
    def auto_provision(self) -> pulumi.Output[str]:
        """
        Should the security agent be automatically provisioned on Virtual Machines in this subscription? Possible values are `On` (to install the security agent automatically, if it's missing) or `Off` (to not install the security agent automatically).
        """
        return pulumi.get(self, "auto_provision")

