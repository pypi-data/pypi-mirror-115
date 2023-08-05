# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['CertificateArgs', 'Certificate']

@pulumi.input_type
class CertificateArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 hosting_environment_profile_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 pfx_blob: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Certificate resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] hosting_environment_profile_id: Must be specified when the certificate is for an App Service Environment hosted App Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_vault_secret_id: The ID of the Key Vault secret. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: The password to access the certificate's private key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pfx_blob: The base64-encoded contents of the certificate. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if hosting_environment_profile_id is not None:
            pulumi.set(__self__, "hosting_environment_profile_id", hosting_environment_profile_id)
        if key_vault_secret_id is not None:
            pulumi.set(__self__, "key_vault_secret_id", key_vault_secret_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if pfx_blob is not None:
            pulumi.set(__self__, "pfx_blob", pfx_blob)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="hostingEnvironmentProfileId")
    def hosting_environment_profile_id(self) -> Optional[pulumi.Input[str]]:
        """
        Must be specified when the certificate is for an App Service Environment hosted App Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "hosting_environment_profile_id")

    @hosting_environment_profile_id.setter
    def hosting_environment_profile_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hosting_environment_profile_id", value)

    @property
    @pulumi.getter(name="keyVaultSecretId")
    def key_vault_secret_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Key Vault secret. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_vault_secret_id")

    @key_vault_secret_id.setter
    def key_vault_secret_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_secret_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password to access the certificate's private key. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="pfxBlob")
    def pfx_blob(self) -> Optional[pulumi.Input[str]]:
        """
        The base64-encoded contents of the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "pfx_blob")

    @pfx_blob.setter
    def pfx_blob(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pfx_blob", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _CertificateState:
    def __init__(__self__, *,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 hosting_environment_profile_id: Optional[pulumi.Input[str]] = None,
                 issue_date: Optional[pulumi.Input[str]] = None,
                 issuer: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 pfx_blob: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subject_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Certificate resources.
        :param pulumi.Input[str] expiration_date: The expiration date for the certificate.
        :param pulumi.Input[str] friendly_name: The friendly name of the certificate.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] host_names: List of host names the certificate applies to.
        :param pulumi.Input[str] hosting_environment_profile_id: Must be specified when the certificate is for an App Service Environment hosted App Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] issue_date: The issue date for the certificate.
        :param pulumi.Input[str] issuer: The name of the certificate issuer.
        :param pulumi.Input[str] key_vault_secret_id: The ID of the Key Vault secret. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: The password to access the certificate's private key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pfx_blob: The base64-encoded contents of the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subject_name: The subject name of the certificate.
        :param pulumi.Input[str] thumbprint: The thumbprint for the certificate.
        """
        if expiration_date is not None:
            pulumi.set(__self__, "expiration_date", expiration_date)
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if host_names is not None:
            pulumi.set(__self__, "host_names", host_names)
        if hosting_environment_profile_id is not None:
            pulumi.set(__self__, "hosting_environment_profile_id", hosting_environment_profile_id)
        if issue_date is not None:
            pulumi.set(__self__, "issue_date", issue_date)
        if issuer is not None:
            pulumi.set(__self__, "issuer", issuer)
        if key_vault_secret_id is not None:
            pulumi.set(__self__, "key_vault_secret_id", key_vault_secret_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if pfx_blob is not None:
            pulumi.set(__self__, "pfx_blob", pfx_blob)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if subject_name is not None:
            pulumi.set(__self__, "subject_name", subject_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if thumbprint is not None:
            pulumi.set(__self__, "thumbprint", thumbprint)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> Optional[pulumi.Input[str]]:
        """
        The expiration date for the certificate.
        """
        return pulumi.get(self, "expiration_date")

    @expiration_date.setter
    def expiration_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expiration_date", value)

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        The friendly name of the certificate.
        """
        return pulumi.get(self, "friendly_name")

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "friendly_name", value)

    @property
    @pulumi.getter(name="hostNames")
    def host_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of host names the certificate applies to.
        """
        return pulumi.get(self, "host_names")

    @host_names.setter
    def host_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "host_names", value)

    @property
    @pulumi.getter(name="hostingEnvironmentProfileId")
    def hosting_environment_profile_id(self) -> Optional[pulumi.Input[str]]:
        """
        Must be specified when the certificate is for an App Service Environment hosted App Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "hosting_environment_profile_id")

    @hosting_environment_profile_id.setter
    def hosting_environment_profile_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hosting_environment_profile_id", value)

    @property
    @pulumi.getter(name="issueDate")
    def issue_date(self) -> Optional[pulumi.Input[str]]:
        """
        The issue date for the certificate.
        """
        return pulumi.get(self, "issue_date")

    @issue_date.setter
    def issue_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issue_date", value)

    @property
    @pulumi.getter
    def issuer(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the certificate issuer.
        """
        return pulumi.get(self, "issuer")

    @issuer.setter
    def issuer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer", value)

    @property
    @pulumi.getter(name="keyVaultSecretId")
    def key_vault_secret_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Key Vault secret. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_vault_secret_id")

    @key_vault_secret_id.setter
    def key_vault_secret_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_secret_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password to access the certificate's private key. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="pfxBlob")
    def pfx_blob(self) -> Optional[pulumi.Input[str]]:
        """
        The base64-encoded contents of the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "pfx_blob")

    @pfx_blob.setter
    def pfx_blob(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pfx_blob", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="subjectName")
    def subject_name(self) -> Optional[pulumi.Input[str]]:
        """
        The subject name of the certificate.
        """
        return pulumi.get(self, "subject_name")

    @subject_name.setter
    def subject_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subject_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        The thumbprint for the certificate.
        """
        return pulumi.get(self, "thumbprint")

    @thumbprint.setter
    def thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint", value)


class Certificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hosting_environment_profile_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 pfx_blob: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an App Service certificate.

        ## Import

        App Service Certificates can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/certificate:Certificate example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Web/certificates/certificate1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hosting_environment_profile_id: Must be specified when the certificate is for an App Service Environment hosted App Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_vault_secret_id: The ID of the Key Vault secret. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: The password to access the certificate's private key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pfx_blob: The base64-encoded contents of the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the certificate. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an App Service certificate.

        ## Import

        App Service Certificates can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/certificate:Certificate example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Web/certificates/certificate1
        ```

        :param str resource_name: The name of the resource.
        :param CertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hosting_environment_profile_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 pfx_blob: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = CertificateArgs.__new__(CertificateArgs)

            __props__.__dict__["hosting_environment_profile_id"] = hosting_environment_profile_id
            __props__.__dict__["key_vault_secret_id"] = key_vault_secret_id
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["password"] = password
            __props__.__dict__["pfx_blob"] = pfx_blob
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["expiration_date"] = None
            __props__.__dict__["friendly_name"] = None
            __props__.__dict__["host_names"] = None
            __props__.__dict__["issue_date"] = None
            __props__.__dict__["issuer"] = None
            __props__.__dict__["subject_name"] = None
            __props__.__dict__["thumbprint"] = None
        super(Certificate, __self__).__init__(
            'azure:appservice/certificate:Certificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            expiration_date: Optional[pulumi.Input[str]] = None,
            friendly_name: Optional[pulumi.Input[str]] = None,
            host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            hosting_environment_profile_id: Optional[pulumi.Input[str]] = None,
            issue_date: Optional[pulumi.Input[str]] = None,
            issuer: Optional[pulumi.Input[str]] = None,
            key_vault_secret_id: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            pfx_blob: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            subject_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            thumbprint: Optional[pulumi.Input[str]] = None) -> 'Certificate':
        """
        Get an existing Certificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] expiration_date: The expiration date for the certificate.
        :param pulumi.Input[str] friendly_name: The friendly name of the certificate.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] host_names: List of host names the certificate applies to.
        :param pulumi.Input[str] hosting_environment_profile_id: Must be specified when the certificate is for an App Service Environment hosted App Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] issue_date: The issue date for the certificate.
        :param pulumi.Input[str] issuer: The name of the certificate issuer.
        :param pulumi.Input[str] key_vault_secret_id: The ID of the Key Vault secret. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: The password to access the certificate's private key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pfx_blob: The base64-encoded contents of the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the certificate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subject_name: The subject name of the certificate.
        :param pulumi.Input[str] thumbprint: The thumbprint for the certificate.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CertificateState.__new__(_CertificateState)

        __props__.__dict__["expiration_date"] = expiration_date
        __props__.__dict__["friendly_name"] = friendly_name
        __props__.__dict__["host_names"] = host_names
        __props__.__dict__["hosting_environment_profile_id"] = hosting_environment_profile_id
        __props__.__dict__["issue_date"] = issue_date
        __props__.__dict__["issuer"] = issuer
        __props__.__dict__["key_vault_secret_id"] = key_vault_secret_id
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["password"] = password
        __props__.__dict__["pfx_blob"] = pfx_blob
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["subject_name"] = subject_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["thumbprint"] = thumbprint
        return Certificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> pulumi.Output[str]:
        """
        The expiration date for the certificate.
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> pulumi.Output[str]:
        """
        The friendly name of the certificate.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="hostNames")
    def host_names(self) -> pulumi.Output[Sequence[str]]:
        """
        List of host names the certificate applies to.
        """
        return pulumi.get(self, "host_names")

    @property
    @pulumi.getter(name="hostingEnvironmentProfileId")
    def hosting_environment_profile_id(self) -> pulumi.Output[Optional[str]]:
        """
        Must be specified when the certificate is for an App Service Environment hosted App Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "hosting_environment_profile_id")

    @property
    @pulumi.getter(name="issueDate")
    def issue_date(self) -> pulumi.Output[str]:
        """
        The issue date for the certificate.
        """
        return pulumi.get(self, "issue_date")

    @property
    @pulumi.getter
    def issuer(self) -> pulumi.Output[str]:
        """
        The name of the certificate issuer.
        """
        return pulumi.get(self, "issuer")

    @property
    @pulumi.getter(name="keyVaultSecretId")
    def key_vault_secret_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Key Vault secret. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_vault_secret_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The password to access the certificate's private key. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="pfxBlob")
    def pfx_blob(self) -> pulumi.Output[Optional[str]]:
        """
        The base64-encoded contents of the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "pfx_blob")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the certificate. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="subjectName")
    def subject_name(self) -> pulumi.Output[str]:
        """
        The subject name of the certificate.
        """
        return pulumi.get(self, "subject_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def thumbprint(self) -> pulumi.Output[str]:
        """
        The thumbprint for the certificate.
        """
        return pulumi.get(self, "thumbprint")

