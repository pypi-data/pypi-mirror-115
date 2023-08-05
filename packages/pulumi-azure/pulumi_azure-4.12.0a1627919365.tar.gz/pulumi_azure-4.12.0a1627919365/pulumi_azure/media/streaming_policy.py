# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['StreamingPolicyArgs', 'StreamingPolicy']

@pulumi.input_type
class StreamingPolicyArgs:
    def __init__(__self__, *,
                 media_services_account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 common_encryption_cbcs: Optional[pulumi.Input['StreamingPolicyCommonEncryptionCbcsArgs']] = None,
                 common_encryption_cenc: Optional[pulumi.Input['StreamingPolicyCommonEncryptionCencArgs']] = None,
                 default_content_key_policy_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 no_encryption_enabled_protocols: Optional[pulumi.Input['StreamingPolicyNoEncryptionEnabledProtocolsArgs']] = None):
        """
        The set of arguments for constructing a StreamingPolicy resource.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Streaming Policy should exist. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input['StreamingPolicyCommonEncryptionCbcsArgs'] common_encryption_cbcs: A `common_encryption_cbcs` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input['StreamingPolicyCommonEncryptionCencArgs'] common_encryption_cenc: A `common_encryption_cenc` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] default_content_key_policy_name: Default Content Key used by current Streaming Policy. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] name: The name which should be used for this Streaming Policy. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input['StreamingPolicyNoEncryptionEnabledProtocolsArgs'] no_encryption_enabled_protocols: A `no_encryption_enabled_protocols` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        pulumi.set(__self__, "media_services_account_name", media_services_account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if common_encryption_cbcs is not None:
            pulumi.set(__self__, "common_encryption_cbcs", common_encryption_cbcs)
        if common_encryption_cenc is not None:
            pulumi.set(__self__, "common_encryption_cenc", common_encryption_cenc)
        if default_content_key_policy_name is not None:
            pulumi.set(__self__, "default_content_key_policy_name", default_content_key_policy_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if no_encryption_enabled_protocols is not None:
            pulumi.set(__self__, "no_encryption_enabled_protocols", no_encryption_enabled_protocols)

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> pulumi.Input[str]:
        """
        The Media Services account name. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @media_services_account_name.setter
    def media_services_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "media_services_account_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Streaming Policy should exist. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="commonEncryptionCbcs")
    def common_encryption_cbcs(self) -> Optional[pulumi.Input['StreamingPolicyCommonEncryptionCbcsArgs']]:
        """
        A `common_encryption_cbcs` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "common_encryption_cbcs")

    @common_encryption_cbcs.setter
    def common_encryption_cbcs(self, value: Optional[pulumi.Input['StreamingPolicyCommonEncryptionCbcsArgs']]):
        pulumi.set(self, "common_encryption_cbcs", value)

    @property
    @pulumi.getter(name="commonEncryptionCenc")
    def common_encryption_cenc(self) -> Optional[pulumi.Input['StreamingPolicyCommonEncryptionCencArgs']]:
        """
        A `common_encryption_cenc` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "common_encryption_cenc")

    @common_encryption_cenc.setter
    def common_encryption_cenc(self, value: Optional[pulumi.Input['StreamingPolicyCommonEncryptionCencArgs']]):
        pulumi.set(self, "common_encryption_cenc", value)

    @property
    @pulumi.getter(name="defaultContentKeyPolicyName")
    def default_content_key_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        Default Content Key used by current Streaming Policy. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "default_content_key_policy_name")

    @default_content_key_policy_name.setter
    def default_content_key_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_content_key_policy_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Streaming Policy. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="noEncryptionEnabledProtocols")
    def no_encryption_enabled_protocols(self) -> Optional[pulumi.Input['StreamingPolicyNoEncryptionEnabledProtocolsArgs']]:
        """
        A `no_encryption_enabled_protocols` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "no_encryption_enabled_protocols")

    @no_encryption_enabled_protocols.setter
    def no_encryption_enabled_protocols(self, value: Optional[pulumi.Input['StreamingPolicyNoEncryptionEnabledProtocolsArgs']]):
        pulumi.set(self, "no_encryption_enabled_protocols", value)


@pulumi.input_type
class _StreamingPolicyState:
    def __init__(__self__, *,
                 common_encryption_cbcs: Optional[pulumi.Input['StreamingPolicyCommonEncryptionCbcsArgs']] = None,
                 common_encryption_cenc: Optional[pulumi.Input['StreamingPolicyCommonEncryptionCencArgs']] = None,
                 default_content_key_policy_name: Optional[pulumi.Input[str]] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 no_encryption_enabled_protocols: Optional[pulumi.Input['StreamingPolicyNoEncryptionEnabledProtocolsArgs']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering StreamingPolicy resources.
        :param pulumi.Input['StreamingPolicyCommonEncryptionCbcsArgs'] common_encryption_cbcs: A `common_encryption_cbcs` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input['StreamingPolicyCommonEncryptionCencArgs'] common_encryption_cenc: A `common_encryption_cenc` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] default_content_key_policy_name: Default Content Key used by current Streaming Policy. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] name: The name which should be used for this Streaming Policy. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input['StreamingPolicyNoEncryptionEnabledProtocolsArgs'] no_encryption_enabled_protocols: A `no_encryption_enabled_protocols` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Streaming Policy should exist. Changing this forces a new Streaming Policy to be created.
        """
        if common_encryption_cbcs is not None:
            pulumi.set(__self__, "common_encryption_cbcs", common_encryption_cbcs)
        if common_encryption_cenc is not None:
            pulumi.set(__self__, "common_encryption_cenc", common_encryption_cenc)
        if default_content_key_policy_name is not None:
            pulumi.set(__self__, "default_content_key_policy_name", default_content_key_policy_name)
        if media_services_account_name is not None:
            pulumi.set(__self__, "media_services_account_name", media_services_account_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if no_encryption_enabled_protocols is not None:
            pulumi.set(__self__, "no_encryption_enabled_protocols", no_encryption_enabled_protocols)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter(name="commonEncryptionCbcs")
    def common_encryption_cbcs(self) -> Optional[pulumi.Input['StreamingPolicyCommonEncryptionCbcsArgs']]:
        """
        A `common_encryption_cbcs` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "common_encryption_cbcs")

    @common_encryption_cbcs.setter
    def common_encryption_cbcs(self, value: Optional[pulumi.Input['StreamingPolicyCommonEncryptionCbcsArgs']]):
        pulumi.set(self, "common_encryption_cbcs", value)

    @property
    @pulumi.getter(name="commonEncryptionCenc")
    def common_encryption_cenc(self) -> Optional[pulumi.Input['StreamingPolicyCommonEncryptionCencArgs']]:
        """
        A `common_encryption_cenc` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "common_encryption_cenc")

    @common_encryption_cenc.setter
    def common_encryption_cenc(self, value: Optional[pulumi.Input['StreamingPolicyCommonEncryptionCencArgs']]):
        pulumi.set(self, "common_encryption_cenc", value)

    @property
    @pulumi.getter(name="defaultContentKeyPolicyName")
    def default_content_key_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        Default Content Key used by current Streaming Policy. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "default_content_key_policy_name")

    @default_content_key_policy_name.setter
    def default_content_key_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_content_key_policy_name", value)

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Media Services account name. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @media_services_account_name.setter
    def media_services_account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "media_services_account_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Streaming Policy. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="noEncryptionEnabledProtocols")
    def no_encryption_enabled_protocols(self) -> Optional[pulumi.Input['StreamingPolicyNoEncryptionEnabledProtocolsArgs']]:
        """
        A `no_encryption_enabled_protocols` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "no_encryption_enabled_protocols")

    @no_encryption_enabled_protocols.setter
    def no_encryption_enabled_protocols(self, value: Optional[pulumi.Input['StreamingPolicyNoEncryptionEnabledProtocolsArgs']]):
        pulumi.set(self, "no_encryption_enabled_protocols", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Streaming Policy should exist. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)


class StreamingPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 common_encryption_cbcs: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCbcsArgs']]] = None,
                 common_encryption_cenc: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCencArgs']]] = None,
                 default_content_key_policy_name: Optional[pulumi.Input[str]] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 no_encryption_enabled_protocols: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyNoEncryptionEnabledProtocolsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Streaming Policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="GRS")
        example_service_account = azure.media.ServiceAccount("exampleServiceAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            storage_accounts=[azure.media.ServiceAccountStorageAccountArgs(
                id=example_account.id,
                is_primary=True,
            )])
        example_streaming_policy = azure.media.StreamingPolicy("exampleStreamingPolicy",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            common_encryption_cenc=azure.media.StreamingPolicyCommonEncryptionCencArgs(
                enabled_protocols=azure.media.StreamingPolicyCommonEncryptionCencEnabledProtocolsArgs(
                    download=False,
                    dash=True,
                    hls=False,
                    smooth_streaming=False,
                ),
                drm_playready=azure.media.StreamingPolicyCommonEncryptionCencDrmPlayreadyArgs(
                    custom_license_acquisition_url_template="https://contoso.com/{AssetAlternativeId}/playready/{ContentKeyId}",
                    custom_attributes="PlayReady CustomAttributes",
                ),
                drm_widevine_custom_license_acquisition_url_template="https://contoso.com/{AssetAlternativeId}/widevine/{ContentKeyId}",
            ),
            common_encryption_cbcs=azure.media.StreamingPolicyCommonEncryptionCbcsArgs(
                enabled_protocols=azure.media.StreamingPolicyCommonEncryptionCbcsEnabledProtocolsArgs(
                    download=False,
                    dash=True,
                    hls=False,
                    smooth_streaming=False,
                ),
                drm_fairplay=azure.media.StreamingPolicyCommonEncryptionCbcsDrmFairplayArgs(
                    custom_license_acquisition_url_template="https://contoso.com/{AssetAlternativeId}/fairplay/{ContentKeyId}",
                    allow_persistent_license=True,
                ),
            ))
        ```

        ## Import

        Streaming Policys can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:media/streamingPolicy:StreamingPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Media/mediaservices/account1/streamingpolicies/policy1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCbcsArgs']] common_encryption_cbcs: A `common_encryption_cbcs` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCencArgs']] common_encryption_cenc: A `common_encryption_cenc` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] default_content_key_policy_name: Default Content Key used by current Streaming Policy. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] name: The name which should be used for this Streaming Policy. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[pulumi.InputType['StreamingPolicyNoEncryptionEnabledProtocolsArgs']] no_encryption_enabled_protocols: A `no_encryption_enabled_protocols` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Streaming Policy should exist. Changing this forces a new Streaming Policy to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StreamingPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Streaming Policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="GRS")
        example_service_account = azure.media.ServiceAccount("exampleServiceAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            storage_accounts=[azure.media.ServiceAccountStorageAccountArgs(
                id=example_account.id,
                is_primary=True,
            )])
        example_streaming_policy = azure.media.StreamingPolicy("exampleStreamingPolicy",
            resource_group_name=example_resource_group.name,
            media_services_account_name=example_service_account.name,
            common_encryption_cenc=azure.media.StreamingPolicyCommonEncryptionCencArgs(
                enabled_protocols=azure.media.StreamingPolicyCommonEncryptionCencEnabledProtocolsArgs(
                    download=False,
                    dash=True,
                    hls=False,
                    smooth_streaming=False,
                ),
                drm_playready=azure.media.StreamingPolicyCommonEncryptionCencDrmPlayreadyArgs(
                    custom_license_acquisition_url_template="https://contoso.com/{AssetAlternativeId}/playready/{ContentKeyId}",
                    custom_attributes="PlayReady CustomAttributes",
                ),
                drm_widevine_custom_license_acquisition_url_template="https://contoso.com/{AssetAlternativeId}/widevine/{ContentKeyId}",
            ),
            common_encryption_cbcs=azure.media.StreamingPolicyCommonEncryptionCbcsArgs(
                enabled_protocols=azure.media.StreamingPolicyCommonEncryptionCbcsEnabledProtocolsArgs(
                    download=False,
                    dash=True,
                    hls=False,
                    smooth_streaming=False,
                ),
                drm_fairplay=azure.media.StreamingPolicyCommonEncryptionCbcsDrmFairplayArgs(
                    custom_license_acquisition_url_template="https://contoso.com/{AssetAlternativeId}/fairplay/{ContentKeyId}",
                    allow_persistent_license=True,
                ),
            ))
        ```

        ## Import

        Streaming Policys can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:media/streamingPolicy:StreamingPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Media/mediaservices/account1/streamingpolicies/policy1
        ```

        :param str resource_name: The name of the resource.
        :param StreamingPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StreamingPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 common_encryption_cbcs: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCbcsArgs']]] = None,
                 common_encryption_cenc: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCencArgs']]] = None,
                 default_content_key_policy_name: Optional[pulumi.Input[str]] = None,
                 media_services_account_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 no_encryption_enabled_protocols: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyNoEncryptionEnabledProtocolsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = StreamingPolicyArgs.__new__(StreamingPolicyArgs)

            __props__.__dict__["common_encryption_cbcs"] = common_encryption_cbcs
            __props__.__dict__["common_encryption_cenc"] = common_encryption_cenc
            __props__.__dict__["default_content_key_policy_name"] = default_content_key_policy_name
            if media_services_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'media_services_account_name'")
            __props__.__dict__["media_services_account_name"] = media_services_account_name
            __props__.__dict__["name"] = name
            __props__.__dict__["no_encryption_enabled_protocols"] = no_encryption_enabled_protocols
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
        super(StreamingPolicy, __self__).__init__(
            'azure:media/streamingPolicy:StreamingPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            common_encryption_cbcs: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCbcsArgs']]] = None,
            common_encryption_cenc: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCencArgs']]] = None,
            default_content_key_policy_name: Optional[pulumi.Input[str]] = None,
            media_services_account_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            no_encryption_enabled_protocols: Optional[pulumi.Input[pulumi.InputType['StreamingPolicyNoEncryptionEnabledProtocolsArgs']]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None) -> 'StreamingPolicy':
        """
        Get an existing StreamingPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCbcsArgs']] common_encryption_cbcs: A `common_encryption_cbcs` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[pulumi.InputType['StreamingPolicyCommonEncryptionCencArgs']] common_encryption_cenc: A `common_encryption_cenc` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] default_content_key_policy_name: Default Content Key used by current Streaming Policy. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] media_services_account_name: The Media Services account name. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] name: The name which should be used for this Streaming Policy. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[pulumi.InputType['StreamingPolicyNoEncryptionEnabledProtocolsArgs']] no_encryption_enabled_protocols: A `no_encryption_enabled_protocols` block as defined below. Changing this forces a new Streaming Policy to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Streaming Policy should exist. Changing this forces a new Streaming Policy to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StreamingPolicyState.__new__(_StreamingPolicyState)

        __props__.__dict__["common_encryption_cbcs"] = common_encryption_cbcs
        __props__.__dict__["common_encryption_cenc"] = common_encryption_cenc
        __props__.__dict__["default_content_key_policy_name"] = default_content_key_policy_name
        __props__.__dict__["media_services_account_name"] = media_services_account_name
        __props__.__dict__["name"] = name
        __props__.__dict__["no_encryption_enabled_protocols"] = no_encryption_enabled_protocols
        __props__.__dict__["resource_group_name"] = resource_group_name
        return StreamingPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="commonEncryptionCbcs")
    def common_encryption_cbcs(self) -> pulumi.Output[Optional['outputs.StreamingPolicyCommonEncryptionCbcs']]:
        """
        A `common_encryption_cbcs` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "common_encryption_cbcs")

    @property
    @pulumi.getter(name="commonEncryptionCenc")
    def common_encryption_cenc(self) -> pulumi.Output[Optional['outputs.StreamingPolicyCommonEncryptionCenc']]:
        """
        A `common_encryption_cenc` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "common_encryption_cenc")

    @property
    @pulumi.getter(name="defaultContentKeyPolicyName")
    def default_content_key_policy_name(self) -> pulumi.Output[Optional[str]]:
        """
        Default Content Key used by current Streaming Policy. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "default_content_key_policy_name")

    @property
    @pulumi.getter(name="mediaServicesAccountName")
    def media_services_account_name(self) -> pulumi.Output[str]:
        """
        The Media Services account name. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "media_services_account_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Streaming Policy. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="noEncryptionEnabledProtocols")
    def no_encryption_enabled_protocols(self) -> pulumi.Output[Optional['outputs.StreamingPolicyNoEncryptionEnabledProtocols']]:
        """
        A `no_encryption_enabled_protocols` block as defined below. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "no_encryption_enabled_protocols")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Streaming Policy should exist. Changing this forces a new Streaming Policy to be created.
        """
        return pulumi.get(self, "resource_group_name")

