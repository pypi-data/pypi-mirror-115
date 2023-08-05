# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['QueueAuthorizationRuleArgs', 'QueueAuthorizationRule']

@pulumi.input_type
class QueueAuthorizationRuleArgs:
    def __init__(__self__, *,
                 namespace_name: pulumi.Input[str],
                 queue_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 listen: Optional[pulumi.Input[bool]] = None,
                 manage: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 send: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a QueueAuthorizationRule resource.
        :param pulumi.Input[str] namespace_name: Specifies the name of the ServiceBus Namespace in which the Queue exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] queue_name: Specifies the name of the ServiceBus Queue. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] listen: Does this Authorization Rule have Listen permissions to the ServiceBus Queue? Defaults to `false`.
        :param pulumi.Input[bool] manage: Does this Authorization Rule have Manage permissions to the ServiceBus Queue? When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        :param pulumi.Input[str] name: Specifies the name of the Authorization Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] send: Does this Authorization Rule have Send permissions to the ServiceBus Queue? Defaults to `false`.
        """
        pulumi.set(__self__, "namespace_name", namespace_name)
        pulumi.set(__self__, "queue_name", queue_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if listen is not None:
            pulumi.set(__self__, "listen", listen)
        if manage is not None:
            pulumi.set(__self__, "manage", manage)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if send is not None:
            pulumi.set(__self__, "send", send)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the ServiceBus Namespace in which the Queue exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="queueName")
    def queue_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the ServiceBus Queue. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "queue_name")

    @queue_name.setter
    def queue_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "queue_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def listen(self) -> Optional[pulumi.Input[bool]]:
        """
        Does this Authorization Rule have Listen permissions to the ServiceBus Queue? Defaults to `false`.
        """
        return pulumi.get(self, "listen")

    @listen.setter
    def listen(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "listen", value)

    @property
    @pulumi.getter
    def manage(self) -> Optional[pulumi.Input[bool]]:
        """
        Does this Authorization Rule have Manage permissions to the ServiceBus Queue? When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        """
        return pulumi.get(self, "manage")

    @manage.setter
    def manage(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "manage", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Authorization Rule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def send(self) -> Optional[pulumi.Input[bool]]:
        """
        Does this Authorization Rule have Send permissions to the ServiceBus Queue? Defaults to `false`.
        """
        return pulumi.get(self, "send")

    @send.setter
    def send(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send", value)


@pulumi.input_type
class _QueueAuthorizationRuleState:
    def __init__(__self__, *,
                 listen: Optional[pulumi.Input[bool]] = None,
                 manage: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 primary_connection_string: Optional[pulumi.Input[str]] = None,
                 primary_key: Optional[pulumi.Input[str]] = None,
                 queue_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 secondary_connection_string: Optional[pulumi.Input[str]] = None,
                 secondary_key: Optional[pulumi.Input[str]] = None,
                 send: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering QueueAuthorizationRule resources.
        :param pulumi.Input[bool] listen: Does this Authorization Rule have Listen permissions to the ServiceBus Queue? Defaults to `false`.
        :param pulumi.Input[bool] manage: Does this Authorization Rule have Manage permissions to the ServiceBus Queue? When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        :param pulumi.Input[str] name: Specifies the name of the Authorization Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the ServiceBus Namespace in which the Queue exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] primary_connection_string: The Primary Connection String for the Authorization Rule.
        :param pulumi.Input[str] primary_key: The Primary Key for the Authorization Rule.
        :param pulumi.Input[str] queue_name: Specifies the name of the ServiceBus Queue. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] secondary_connection_string: The Secondary Connection String for the Authorization Rule.
        :param pulumi.Input[str] secondary_key: The Secondary Key for the Authorization Rule.
        :param pulumi.Input[bool] send: Does this Authorization Rule have Send permissions to the ServiceBus Queue? Defaults to `false`.
        """
        if listen is not None:
            pulumi.set(__self__, "listen", listen)
        if manage is not None:
            pulumi.set(__self__, "manage", manage)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace_name is not None:
            pulumi.set(__self__, "namespace_name", namespace_name)
        if primary_connection_string is not None:
            pulumi.set(__self__, "primary_connection_string", primary_connection_string)
        if primary_key is not None:
            pulumi.set(__self__, "primary_key", primary_key)
        if queue_name is not None:
            pulumi.set(__self__, "queue_name", queue_name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if secondary_connection_string is not None:
            pulumi.set(__self__, "secondary_connection_string", secondary_connection_string)
        if secondary_key is not None:
            pulumi.set(__self__, "secondary_key", secondary_key)
        if send is not None:
            pulumi.set(__self__, "send", send)

    @property
    @pulumi.getter
    def listen(self) -> Optional[pulumi.Input[bool]]:
        """
        Does this Authorization Rule have Listen permissions to the ServiceBus Queue? Defaults to `false`.
        """
        return pulumi.get(self, "listen")

    @listen.setter
    def listen(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "listen", value)

    @property
    @pulumi.getter
    def manage(self) -> Optional[pulumi.Input[bool]]:
        """
        Does this Authorization Rule have Manage permissions to the ServiceBus Queue? When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        """
        return pulumi.get(self, "manage")

    @manage.setter
    def manage(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "manage", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Authorization Rule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the ServiceBus Namespace in which the Queue exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        The Primary Connection String for the Authorization Rule.
        """
        return pulumi.get(self, "primary_connection_string")

    @primary_connection_string.setter
    def primary_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_connection_string", value)

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Primary Key for the Authorization Rule.
        """
        return pulumi.get(self, "primary_key")

    @primary_key.setter
    def primary_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_key", value)

    @property
    @pulumi.getter(name="queueName")
    def queue_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the ServiceBus Queue. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "queue_name")

    @queue_name.setter
    def queue_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "queue_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        The Secondary Connection String for the Authorization Rule.
        """
        return pulumi.get(self, "secondary_connection_string")

    @secondary_connection_string.setter
    def secondary_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_connection_string", value)

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Secondary Key for the Authorization Rule.
        """
        return pulumi.get(self, "secondary_key")

    @secondary_key.setter
    def secondary_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_key", value)

    @property
    @pulumi.getter
    def send(self) -> Optional[pulumi.Input[bool]]:
        """
        Does this Authorization Rule have Send permissions to the ServiceBus Queue? Defaults to `false`.
        """
        return pulumi.get(self, "send")

    @send.setter
    def send(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send", value)


warnings.warn("""azure.eventhub.QueueAuthorizationRule has been deprecated in favor of azure.servicebus.QueueAuthorizationRule""", DeprecationWarning)


class QueueAuthorizationRule(pulumi.CustomResource):
    warnings.warn("""azure.eventhub.QueueAuthorizationRule has been deprecated in favor of azure.servicebus.QueueAuthorizationRule""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 listen: Optional[pulumi.Input[bool]] = None,
                 manage: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 queue_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 send: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Manages an Authorization Rule for a ServiceBus Queue.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_namespace = azure.servicebus.Namespace("exampleNamespace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="Standard",
            tags={
                "source": "example",
            })
        example_queue = azure.servicebus.Queue("exampleQueue",
            resource_group_name=example_resource_group.name,
            namespace_name=example_namespace.name,
            enable_partitioning=True)
        example_queue_authorization_rule = azure.servicebus.QueueAuthorizationRule("exampleQueueAuthorizationRule",
            namespace_name=example_namespace.name,
            queue_name=example_queue.name,
            resource_group_name=example_resource_group.name,
            listen=True,
            send=True,
            manage=False)
        ```

        ## Import

        ServiceBus Queue Authorization Rules can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:eventhub/queueAuthorizationRule:QueueAuthorizationRule rule1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ServiceBus/namespaces/namespace1/queues/queue1/authorizationRules/rule1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] listen: Does this Authorization Rule have Listen permissions to the ServiceBus Queue? Defaults to `false`.
        :param pulumi.Input[bool] manage: Does this Authorization Rule have Manage permissions to the ServiceBus Queue? When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        :param pulumi.Input[str] name: Specifies the name of the Authorization Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the ServiceBus Namespace in which the Queue exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] queue_name: Specifies the name of the ServiceBus Queue. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] send: Does this Authorization Rule have Send permissions to the ServiceBus Queue? Defaults to `false`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QueueAuthorizationRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Authorization Rule for a ServiceBus Queue.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_namespace = azure.servicebus.Namespace("exampleNamespace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="Standard",
            tags={
                "source": "example",
            })
        example_queue = azure.servicebus.Queue("exampleQueue",
            resource_group_name=example_resource_group.name,
            namespace_name=example_namespace.name,
            enable_partitioning=True)
        example_queue_authorization_rule = azure.servicebus.QueueAuthorizationRule("exampleQueueAuthorizationRule",
            namespace_name=example_namespace.name,
            queue_name=example_queue.name,
            resource_group_name=example_resource_group.name,
            listen=True,
            send=True,
            manage=False)
        ```

        ## Import

        ServiceBus Queue Authorization Rules can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:eventhub/queueAuthorizationRule:QueueAuthorizationRule rule1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ServiceBus/namespaces/namespace1/queues/queue1/authorizationRules/rule1
        ```

        :param str resource_name: The name of the resource.
        :param QueueAuthorizationRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QueueAuthorizationRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 listen: Optional[pulumi.Input[bool]] = None,
                 manage: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 queue_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 send: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        pulumi.log.warn("""QueueAuthorizationRule is deprecated: azure.eventhub.QueueAuthorizationRule has been deprecated in favor of azure.servicebus.QueueAuthorizationRule""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QueueAuthorizationRuleArgs.__new__(QueueAuthorizationRuleArgs)

            __props__.__dict__["listen"] = listen
            __props__.__dict__["manage"] = manage
            __props__.__dict__["name"] = name
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__["namespace_name"] = namespace_name
            if queue_name is None and not opts.urn:
                raise TypeError("Missing required property 'queue_name'")
            __props__.__dict__["queue_name"] = queue_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["send"] = send
            __props__.__dict__["primary_connection_string"] = None
            __props__.__dict__["primary_key"] = None
            __props__.__dict__["secondary_connection_string"] = None
            __props__.__dict__["secondary_key"] = None
        super(QueueAuthorizationRule, __self__).__init__(
            'azure:eventhub/queueAuthorizationRule:QueueAuthorizationRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            listen: Optional[pulumi.Input[bool]] = None,
            manage: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            namespace_name: Optional[pulumi.Input[str]] = None,
            primary_connection_string: Optional[pulumi.Input[str]] = None,
            primary_key: Optional[pulumi.Input[str]] = None,
            queue_name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            secondary_connection_string: Optional[pulumi.Input[str]] = None,
            secondary_key: Optional[pulumi.Input[str]] = None,
            send: Optional[pulumi.Input[bool]] = None) -> 'QueueAuthorizationRule':
        """
        Get an existing QueueAuthorizationRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] listen: Does this Authorization Rule have Listen permissions to the ServiceBus Queue? Defaults to `false`.
        :param pulumi.Input[bool] manage: Does this Authorization Rule have Manage permissions to the ServiceBus Queue? When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        :param pulumi.Input[str] name: Specifies the name of the Authorization Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the ServiceBus Namespace in which the Queue exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] primary_connection_string: The Primary Connection String for the Authorization Rule.
        :param pulumi.Input[str] primary_key: The Primary Key for the Authorization Rule.
        :param pulumi.Input[str] queue_name: Specifies the name of the ServiceBus Queue. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] secondary_connection_string: The Secondary Connection String for the Authorization Rule.
        :param pulumi.Input[str] secondary_key: The Secondary Key for the Authorization Rule.
        :param pulumi.Input[bool] send: Does this Authorization Rule have Send permissions to the ServiceBus Queue? Defaults to `false`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _QueueAuthorizationRuleState.__new__(_QueueAuthorizationRuleState)

        __props__.__dict__["listen"] = listen
        __props__.__dict__["manage"] = manage
        __props__.__dict__["name"] = name
        __props__.__dict__["namespace_name"] = namespace_name
        __props__.__dict__["primary_connection_string"] = primary_connection_string
        __props__.__dict__["primary_key"] = primary_key
        __props__.__dict__["queue_name"] = queue_name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["secondary_connection_string"] = secondary_connection_string
        __props__.__dict__["secondary_key"] = secondary_key
        __props__.__dict__["send"] = send
        return QueueAuthorizationRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def listen(self) -> pulumi.Output[Optional[bool]]:
        """
        Does this Authorization Rule have Listen permissions to the ServiceBus Queue? Defaults to `false`.
        """
        return pulumi.get(self, "listen")

    @property
    @pulumi.getter
    def manage(self) -> pulumi.Output[Optional[bool]]:
        """
        Does this Authorization Rule have Manage permissions to the ServiceBus Queue? When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        """
        return pulumi.get(self, "manage")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Authorization Rule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the ServiceBus Namespace in which the Queue exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "namespace_name")

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> pulumi.Output[str]:
        """
        The Primary Connection String for the Authorization Rule.
        """
        return pulumi.get(self, "primary_connection_string")

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> pulumi.Output[str]:
        """
        The Primary Key for the Authorization Rule.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="queueName")
    def queue_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the ServiceBus Queue. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "queue_name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> pulumi.Output[str]:
        """
        The Secondary Connection String for the Authorization Rule.
        """
        return pulumi.get(self, "secondary_connection_string")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> pulumi.Output[str]:
        """
        The Secondary Key for the Authorization Rule.
        """
        return pulumi.get(self, "secondary_key")

    @property
    @pulumi.getter
    def send(self) -> pulumi.Output[Optional[bool]]:
        """
        Does this Authorization Rule have Send permissions to the ServiceBus Queue? Defaults to `false`.
        """
        return pulumi.get(self, "send")

