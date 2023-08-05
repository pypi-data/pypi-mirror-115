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

__all__ = ['BlobInventoryPolicyArgs', 'BlobInventoryPolicy']

@pulumi.input_type
class BlobInventoryPolicyArgs:
    def __init__(__self__, *,
                 rules: pulumi.Input[Sequence[pulumi.Input['BlobInventoryPolicyRuleArgs']]],
                 storage_account_id: pulumi.Input[str],
                 storage_container_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a BlobInventoryPolicy resource.
        :param pulumi.Input[Sequence[pulumi.Input['BlobInventoryPolicyRuleArgs']]] rules: One or more `rules` blocks as defined below.
        :param pulumi.Input[str] storage_account_id: The ID of the storage account to apply this Blob Inventory Policy to. Changing this forces a new Storage Blob Inventory Policy to be created.
        :param pulumi.Input[str] storage_container_name: The storage container name to store the blob inventory files. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        pulumi.set(__self__, "rules", rules)
        pulumi.set(__self__, "storage_account_id", storage_account_id)
        pulumi.set(__self__, "storage_container_name", storage_container_name)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Input[Sequence[pulumi.Input['BlobInventoryPolicyRuleArgs']]]:
        """
        One or more `rules` blocks as defined below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: pulumi.Input[Sequence[pulumi.Input['BlobInventoryPolicyRuleArgs']]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> pulumi.Input[str]:
        """
        The ID of the storage account to apply this Blob Inventory Policy to. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        return pulumi.get(self, "storage_account_id")

    @storage_account_id.setter
    def storage_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_account_id", value)

    @property
    @pulumi.getter(name="storageContainerName")
    def storage_container_name(self) -> pulumi.Input[str]:
        """
        The storage container name to store the blob inventory files. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        return pulumi.get(self, "storage_container_name")

    @storage_container_name.setter
    def storage_container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_container_name", value)


@pulumi.input_type
class _BlobInventoryPolicyState:
    def __init__(__self__, *,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['BlobInventoryPolicyRuleArgs']]]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 storage_container_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BlobInventoryPolicy resources.
        :param pulumi.Input[Sequence[pulumi.Input['BlobInventoryPolicyRuleArgs']]] rules: One or more `rules` blocks as defined below.
        :param pulumi.Input[str] storage_account_id: The ID of the storage account to apply this Blob Inventory Policy to. Changing this forces a new Storage Blob Inventory Policy to be created.
        :param pulumi.Input[str] storage_container_name: The storage container name to store the blob inventory files. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if storage_account_id is not None:
            pulumi.set(__self__, "storage_account_id", storage_account_id)
        if storage_container_name is not None:
            pulumi.set(__self__, "storage_container_name", storage_container_name)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BlobInventoryPolicyRuleArgs']]]]:
        """
        One or more `rules` blocks as defined below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BlobInventoryPolicyRuleArgs']]]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the storage account to apply this Blob Inventory Policy to. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        return pulumi.get(self, "storage_account_id")

    @storage_account_id.setter
    def storage_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_id", value)

    @property
    @pulumi.getter(name="storageContainerName")
    def storage_container_name(self) -> Optional[pulumi.Input[str]]:
        """
        The storage container name to store the blob inventory files. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        return pulumi.get(self, "storage_container_name")

    @storage_container_name.setter
    def storage_container_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_container_name", value)


class BlobInventoryPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlobInventoryPolicyRuleArgs']]]]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 storage_container_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Storage Blob Inventory Policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            blob_properties=azure.storage.AccountBlobPropertiesArgs(
                versioning_enabled=True,
            ))
        example_container = azure.storage.Container("exampleContainer",
            storage_account_name=example_account.name,
            container_access_type="private")
        example_blob_inventory_policy = azure.storage.BlobInventoryPolicy("exampleBlobInventoryPolicy",
            storage_account_id=example_account.id,
            storage_container_name=example_container.name,
            rules=[azure.storage.BlobInventoryPolicyRuleArgs(
                name="rule1",
                filter=azure.storage.BlobInventoryPolicyRuleFilterArgs(
                    blob_types=["blockBlob"],
                    include_blob_versions=True,
                    include_snapshots=True,
                    prefix_matches=["*/example"],
                ),
            )])
        ```

        ## Import

        Storage Blob Inventory Policys can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:storage/blobInventoryPolicy:BlobInventoryPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Storage/storageAccounts/storageAccount1/inventoryPolicies/inventoryPolicy1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlobInventoryPolicyRuleArgs']]]] rules: One or more `rules` blocks as defined below.
        :param pulumi.Input[str] storage_account_id: The ID of the storage account to apply this Blob Inventory Policy to. Changing this forces a new Storage Blob Inventory Policy to be created.
        :param pulumi.Input[str] storage_container_name: The storage container name to store the blob inventory files. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BlobInventoryPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Storage Blob Inventory Policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            blob_properties=azure.storage.AccountBlobPropertiesArgs(
                versioning_enabled=True,
            ))
        example_container = azure.storage.Container("exampleContainer",
            storage_account_name=example_account.name,
            container_access_type="private")
        example_blob_inventory_policy = azure.storage.BlobInventoryPolicy("exampleBlobInventoryPolicy",
            storage_account_id=example_account.id,
            storage_container_name=example_container.name,
            rules=[azure.storage.BlobInventoryPolicyRuleArgs(
                name="rule1",
                filter=azure.storage.BlobInventoryPolicyRuleFilterArgs(
                    blob_types=["blockBlob"],
                    include_blob_versions=True,
                    include_snapshots=True,
                    prefix_matches=["*/example"],
                ),
            )])
        ```

        ## Import

        Storage Blob Inventory Policys can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:storage/blobInventoryPolicy:BlobInventoryPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Storage/storageAccounts/storageAccount1/inventoryPolicies/inventoryPolicy1
        ```

        :param str resource_name: The name of the resource.
        :param BlobInventoryPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BlobInventoryPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlobInventoryPolicyRuleArgs']]]]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 storage_container_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = BlobInventoryPolicyArgs.__new__(BlobInventoryPolicyArgs)

            if rules is None and not opts.urn:
                raise TypeError("Missing required property 'rules'")
            __props__.__dict__["rules"] = rules
            if storage_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'storage_account_id'")
            __props__.__dict__["storage_account_id"] = storage_account_id
            if storage_container_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_container_name'")
            __props__.__dict__["storage_container_name"] = storage_container_name
        super(BlobInventoryPolicy, __self__).__init__(
            'azure:storage/blobInventoryPolicy:BlobInventoryPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlobInventoryPolicyRuleArgs']]]]] = None,
            storage_account_id: Optional[pulumi.Input[str]] = None,
            storage_container_name: Optional[pulumi.Input[str]] = None) -> 'BlobInventoryPolicy':
        """
        Get an existing BlobInventoryPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlobInventoryPolicyRuleArgs']]]] rules: One or more `rules` blocks as defined below.
        :param pulumi.Input[str] storage_account_id: The ID of the storage account to apply this Blob Inventory Policy to. Changing this forces a new Storage Blob Inventory Policy to be created.
        :param pulumi.Input[str] storage_container_name: The storage container name to store the blob inventory files. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BlobInventoryPolicyState.__new__(_BlobInventoryPolicyState)

        __props__.__dict__["rules"] = rules
        __props__.__dict__["storage_account_id"] = storage_account_id
        __props__.__dict__["storage_container_name"] = storage_container_name
        return BlobInventoryPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Sequence['outputs.BlobInventoryPolicyRule']]:
        """
        One or more `rules` blocks as defined below.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> pulumi.Output[str]:
        """
        The ID of the storage account to apply this Blob Inventory Policy to. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter(name="storageContainerName")
    def storage_container_name(self) -> pulumi.Output[str]:
        """
        The storage container name to store the blob inventory files. Changing this forces a new Storage Blob Inventory Policy to be created.
        """
        return pulumi.get(self, "storage_container_name")

