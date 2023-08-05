# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TopicAuthorizationRuleArgs', 'TopicAuthorizationRule']

@pulumi.input_type
class TopicAuthorizationRuleArgs:
    def __init__(__self__, *,
                 namespace_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 topic_name: pulumi.Input[str],
                 listen: Optional[pulumi.Input[bool]] = None,
                 manage: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 send: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a TopicAuthorizationRule resource.
        :param pulumi.Input[str] namespace_name: Specifies the name of the ServiceBus Namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] topic_name: Specifies the name of the ServiceBus Topic. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] listen: Grants listen access to this this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[bool] manage: Grants manage access to this this Authorization Rule. When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        :param pulumi.Input[str] name: Specifies the name of the ServiceBus Topic Authorization Rule resource. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] send: Grants send access to this this Authorization Rule. Defaults to `false`.
        """
        pulumi.set(__self__, "namespace_name", namespace_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "topic_name", topic_name)
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
        Specifies the name of the ServiceBus Namespace. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="topicName")
    def topic_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the ServiceBus Topic. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "topic_name")

    @topic_name.setter
    def topic_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "topic_name", value)

    @property
    @pulumi.getter
    def listen(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants listen access to this this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, "listen")

    @listen.setter
    def listen(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "listen", value)

    @property
    @pulumi.getter
    def manage(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants manage access to this this Authorization Rule. When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        """
        return pulumi.get(self, "manage")

    @manage.setter
    def manage(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "manage", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the ServiceBus Topic Authorization Rule resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def send(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants send access to this this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, "send")

    @send.setter
    def send(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send", value)


@pulumi.input_type
class _TopicAuthorizationRuleState:
    def __init__(__self__, *,
                 listen: Optional[pulumi.Input[bool]] = None,
                 manage: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 primary_connection_string: Optional[pulumi.Input[str]] = None,
                 primary_key: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 secondary_connection_string: Optional[pulumi.Input[str]] = None,
                 secondary_key: Optional[pulumi.Input[str]] = None,
                 send: Optional[pulumi.Input[bool]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TopicAuthorizationRule resources.
        :param pulumi.Input[bool] listen: Grants listen access to this this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[bool] manage: Grants manage access to this this Authorization Rule. When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        :param pulumi.Input[str] name: Specifies the name of the ServiceBus Topic Authorization Rule resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the ServiceBus Namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] primary_connection_string: The Primary Connection String for the ServiceBus Topic authorization Rule.
        :param pulumi.Input[str] primary_key: The Primary Key for the ServiceBus Topic authorization Rule.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] secondary_connection_string: The Secondary Connection String for the ServiceBus Topic authorization Rule.
        :param pulumi.Input[str] secondary_key: The Secondary Key for the ServiceBus Topic authorization Rule.
        :param pulumi.Input[bool] send: Grants send access to this this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[str] topic_name: Specifies the name of the ServiceBus Topic. Changing this forces a new resource to be created.
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
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if secondary_connection_string is not None:
            pulumi.set(__self__, "secondary_connection_string", secondary_connection_string)
        if secondary_key is not None:
            pulumi.set(__self__, "secondary_key", secondary_key)
        if send is not None:
            pulumi.set(__self__, "send", send)
        if topic_name is not None:
            pulumi.set(__self__, "topic_name", topic_name)

    @property
    @pulumi.getter
    def listen(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants listen access to this this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, "listen")

    @listen.setter
    def listen(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "listen", value)

    @property
    @pulumi.getter
    def manage(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants manage access to this this Authorization Rule. When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        """
        return pulumi.get(self, "manage")

    @manage.setter
    def manage(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "manage", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the ServiceBus Topic Authorization Rule resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the ServiceBus Namespace. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        The Primary Connection String for the ServiceBus Topic authorization Rule.
        """
        return pulumi.get(self, "primary_connection_string")

    @primary_connection_string.setter
    def primary_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_connection_string", value)

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Primary Key for the ServiceBus Topic authorization Rule.
        """
        return pulumi.get(self, "primary_key")

    @primary_key.setter
    def primary_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_key", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        The Secondary Connection String for the ServiceBus Topic authorization Rule.
        """
        return pulumi.get(self, "secondary_connection_string")

    @secondary_connection_string.setter
    def secondary_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_connection_string", value)

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Secondary Key for the ServiceBus Topic authorization Rule.
        """
        return pulumi.get(self, "secondary_key")

    @secondary_key.setter
    def secondary_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_key", value)

    @property
    @pulumi.getter
    def send(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants send access to this this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, "send")

    @send.setter
    def send(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send", value)

    @property
    @pulumi.getter(name="topicName")
    def topic_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the ServiceBus Topic. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "topic_name")

    @topic_name.setter
    def topic_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "topic_name", value)


warnings.warn("""azure.eventhub.TopicAuthorizationRule has been deprecated in favor of azure.servicebus.TopicAuthorizationRule""", DeprecationWarning)


class TopicAuthorizationRule(pulumi.CustomResource):
    warnings.warn("""azure.eventhub.TopicAuthorizationRule has been deprecated in favor of azure.servicebus.TopicAuthorizationRule""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 listen: Optional[pulumi.Input[bool]] = None,
                 manage: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 send: Optional[pulumi.Input[bool]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a ServiceBus Topic authorization Rule within a ServiceBus Topic.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_namespace = azure.servicebus.Namespace("exampleNamespace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="Standard",
            tags={
                "source": "example",
            })
        example_topic = azure.servicebus.Topic("exampleTopic",
            resource_group_name=example_resource_group.name,
            namespace_name=example_namespace.name)
        example_topic_authorization_rule = azure.servicebus.TopicAuthorizationRule("exampleTopicAuthorizationRule",
            namespace_name=example_namespace.name,
            topic_name=example_topic.name,
            resource_group_name=example_resource_group.name,
            listen=True,
            send=False,
            manage=False)
        ```

        ## Import

        ServiceBus Topic authorization rules can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:eventhub/topicAuthorizationRule:TopicAuthorizationRule rule1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ServiceBus/namespaces/namespace1/topics/topic1/authorizationRules/rule1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] listen: Grants listen access to this this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[bool] manage: Grants manage access to this this Authorization Rule. When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        :param pulumi.Input[str] name: Specifies the name of the ServiceBus Topic Authorization Rule resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the ServiceBus Namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] send: Grants send access to this this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[str] topic_name: Specifies the name of the ServiceBus Topic. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TopicAuthorizationRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a ServiceBus Topic authorization Rule within a ServiceBus Topic.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_namespace = azure.servicebus.Namespace("exampleNamespace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="Standard",
            tags={
                "source": "example",
            })
        example_topic = azure.servicebus.Topic("exampleTopic",
            resource_group_name=example_resource_group.name,
            namespace_name=example_namespace.name)
        example_topic_authorization_rule = azure.servicebus.TopicAuthorizationRule("exampleTopicAuthorizationRule",
            namespace_name=example_namespace.name,
            topic_name=example_topic.name,
            resource_group_name=example_resource_group.name,
            listen=True,
            send=False,
            manage=False)
        ```

        ## Import

        ServiceBus Topic authorization rules can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:eventhub/topicAuthorizationRule:TopicAuthorizationRule rule1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.ServiceBus/namespaces/namespace1/topics/topic1/authorizationRules/rule1
        ```

        :param str resource_name: The name of the resource.
        :param TopicAuthorizationRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TopicAuthorizationRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
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
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 send: Optional[pulumi.Input[bool]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""TopicAuthorizationRule is deprecated: azure.eventhub.TopicAuthorizationRule has been deprecated in favor of azure.servicebus.TopicAuthorizationRule""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TopicAuthorizationRuleArgs.__new__(TopicAuthorizationRuleArgs)

            __props__.__dict__["listen"] = listen
            __props__.__dict__["manage"] = manage
            __props__.__dict__["name"] = name
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__["namespace_name"] = namespace_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["send"] = send
            if topic_name is None and not opts.urn:
                raise TypeError("Missing required property 'topic_name'")
            __props__.__dict__["topic_name"] = topic_name
            __props__.__dict__["primary_connection_string"] = None
            __props__.__dict__["primary_key"] = None
            __props__.__dict__["secondary_connection_string"] = None
            __props__.__dict__["secondary_key"] = None
        super(TopicAuthorizationRule, __self__).__init__(
            'azure:eventhub/topicAuthorizationRule:TopicAuthorizationRule',
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
            resource_group_name: Optional[pulumi.Input[str]] = None,
            secondary_connection_string: Optional[pulumi.Input[str]] = None,
            secondary_key: Optional[pulumi.Input[str]] = None,
            send: Optional[pulumi.Input[bool]] = None,
            topic_name: Optional[pulumi.Input[str]] = None) -> 'TopicAuthorizationRule':
        """
        Get an existing TopicAuthorizationRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] listen: Grants listen access to this this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[bool] manage: Grants manage access to this this Authorization Rule. When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        :param pulumi.Input[str] name: Specifies the name of the ServiceBus Topic Authorization Rule resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the ServiceBus Namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] primary_connection_string: The Primary Connection String for the ServiceBus Topic authorization Rule.
        :param pulumi.Input[str] primary_key: The Primary Key for the ServiceBus Topic authorization Rule.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] secondary_connection_string: The Secondary Connection String for the ServiceBus Topic authorization Rule.
        :param pulumi.Input[str] secondary_key: The Secondary Key for the ServiceBus Topic authorization Rule.
        :param pulumi.Input[bool] send: Grants send access to this this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[str] topic_name: Specifies the name of the ServiceBus Topic. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TopicAuthorizationRuleState.__new__(_TopicAuthorizationRuleState)

        __props__.__dict__["listen"] = listen
        __props__.__dict__["manage"] = manage
        __props__.__dict__["name"] = name
        __props__.__dict__["namespace_name"] = namespace_name
        __props__.__dict__["primary_connection_string"] = primary_connection_string
        __props__.__dict__["primary_key"] = primary_key
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["secondary_connection_string"] = secondary_connection_string
        __props__.__dict__["secondary_key"] = secondary_key
        __props__.__dict__["send"] = send
        __props__.__dict__["topic_name"] = topic_name
        return TopicAuthorizationRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def listen(self) -> pulumi.Output[Optional[bool]]:
        """
        Grants listen access to this this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, "listen")

    @property
    @pulumi.getter
    def manage(self) -> pulumi.Output[Optional[bool]]:
        """
        Grants manage access to this this Authorization Rule. When this property is `true` - both `listen` and `send` must be too. Defaults to `false`.
        """
        return pulumi.get(self, "manage")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the ServiceBus Topic Authorization Rule resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the ServiceBus Namespace. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "namespace_name")

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> pulumi.Output[str]:
        """
        The Primary Connection String for the ServiceBus Topic authorization Rule.
        """
        return pulumi.get(self, "primary_connection_string")

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> pulumi.Output[str]:
        """
        The Primary Key for the ServiceBus Topic authorization Rule.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which the ServiceBus Namespace exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> pulumi.Output[str]:
        """
        The Secondary Connection String for the ServiceBus Topic authorization Rule.
        """
        return pulumi.get(self, "secondary_connection_string")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> pulumi.Output[str]:
        """
        The Secondary Key for the ServiceBus Topic authorization Rule.
        """
        return pulumi.get(self, "secondary_key")

    @property
    @pulumi.getter
    def send(self) -> pulumi.Output[Optional[bool]]:
        """
        Grants send access to this this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, "send")

    @property
    @pulumi.getter(name="topicName")
    def topic_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the ServiceBus Topic. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "topic_name")

