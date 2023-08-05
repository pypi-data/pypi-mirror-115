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

__all__ = ['ScheduledQueryRulesAlertArgs', 'ScheduledQueryRulesAlert']

@pulumi.input_type
class ScheduledQueryRulesAlertArgs:
    def __init__(__self__, *,
                 action: pulumi.Input['ScheduledQueryRulesAlertActionArgs'],
                 data_source_id: pulumi.Input[str],
                 frequency: pulumi.Input[int],
                 query: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 time_window: pulumi.Input[int],
                 trigger: pulumi.Input['ScheduledQueryRulesAlertTriggerArgs'],
                 authorized_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query_type: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throttling: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a ScheduledQueryRulesAlert resource.
        :param pulumi.Input['ScheduledQueryRulesAlertActionArgs'] action: An `action` block as defined below.
        :param pulumi.Input[str] data_source_id: The resource URI over which log search query is to be run.
        :param pulumi.Input[int] frequency: Frequency (in minutes) at which rule condition should be evaluated.  Values must be between 5 and 1440 (inclusive).
        :param pulumi.Input[str] query: Log search query.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the scheduled query rule instance.
        :param pulumi.Input[int] time_window: Time window for which data needs to be fetched for query (must be greater than or equal to `frequency`).  Values must be between 5 and 2880 (inclusive).
        :param pulumi.Input['ScheduledQueryRulesAlertTriggerArgs'] trigger: The condition that results in the alert rule being run.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] authorized_resource_ids: List of Resource IDs referred into query.
        :param pulumi.Input[str] description: The description of the scheduled query rule.
        :param pulumi.Input[bool] enabled: Whether this scheduled query rule is enabled.  Default is `true`.
        :param pulumi.Input[str] name: The name of the scheduled query rule. Changing this forces a new resource to be created.
        :param pulumi.Input[int] severity: Severity of the alert. Possible values include: 0, 1, 2, 3, or 4.
        :param pulumi.Input[int] throttling: Time (in minutes) for which Alerts should be throttled or suppressed.  Values must be between 0 and 10000 (inclusive).
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "data_source_id", data_source_id)
        pulumi.set(__self__, "frequency", frequency)
        pulumi.set(__self__, "query", query)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "time_window", time_window)
        pulumi.set(__self__, "trigger", trigger)
        if authorized_resource_ids is not None:
            pulumi.set(__self__, "authorized_resource_ids", authorized_resource_ids)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if query_type is not None:
            pulumi.set(__self__, "query_type", query_type)
        if severity is not None:
            pulumi.set(__self__, "severity", severity)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if throttling is not None:
            pulumi.set(__self__, "throttling", throttling)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input['ScheduledQueryRulesAlertActionArgs']:
        """
        An `action` block as defined below.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input['ScheduledQueryRulesAlertActionArgs']):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> pulumi.Input[str]:
        """
        The resource URI over which log search query is to be run.
        """
        return pulumi.get(self, "data_source_id")

    @data_source_id.setter
    def data_source_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_source_id", value)

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Input[int]:
        """
        Frequency (in minutes) at which rule condition should be evaluated.  Values must be between 5 and 1440 (inclusive).
        """
        return pulumi.get(self, "frequency")

    @frequency.setter
    def frequency(self, value: pulumi.Input[int]):
        pulumi.set(self, "frequency", value)

    @property
    @pulumi.getter
    def query(self) -> pulumi.Input[str]:
        """
        Log search query.
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: pulumi.Input[str]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the scheduled query rule instance.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="timeWindow")
    def time_window(self) -> pulumi.Input[int]:
        """
        Time window for which data needs to be fetched for query (must be greater than or equal to `frequency`).  Values must be between 5 and 2880 (inclusive).
        """
        return pulumi.get(self, "time_window")

    @time_window.setter
    def time_window(self, value: pulumi.Input[int]):
        pulumi.set(self, "time_window", value)

    @property
    @pulumi.getter
    def trigger(self) -> pulumi.Input['ScheduledQueryRulesAlertTriggerArgs']:
        """
        The condition that results in the alert rule being run.
        """
        return pulumi.get(self, "trigger")

    @trigger.setter
    def trigger(self, value: pulumi.Input['ScheduledQueryRulesAlertTriggerArgs']):
        pulumi.set(self, "trigger", value)

    @property
    @pulumi.getter(name="authorizedResourceIds")
    def authorized_resource_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Resource IDs referred into query.
        """
        return pulumi.get(self, "authorized_resource_ids")

    @authorized_resource_ids.setter
    def authorized_resource_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "authorized_resource_ids", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the scheduled query rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether this scheduled query rule is enabled.  Default is `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the scheduled query rule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="queryType")
    def query_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "query_type")

    @query_type.setter
    def query_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query_type", value)

    @property
    @pulumi.getter
    def severity(self) -> Optional[pulumi.Input[int]]:
        """
        Severity of the alert. Possible values include: 0, 1, 2, 3, or 4.
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def throttling(self) -> Optional[pulumi.Input[int]]:
        """
        Time (in minutes) for which Alerts should be throttled or suppressed.  Values must be between 0 and 10000 (inclusive).
        """
        return pulumi.get(self, "throttling")

    @throttling.setter
    def throttling(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throttling", value)


@pulumi.input_type
class _ScheduledQueryRulesAlertState:
    def __init__(__self__, *,
                 action: Optional[pulumi.Input['ScheduledQueryRulesAlertActionArgs']] = None,
                 authorized_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_source_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 frequency: Optional[pulumi.Input[int]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 query_type: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throttling: Optional[pulumi.Input[int]] = None,
                 time_window: Optional[pulumi.Input[int]] = None,
                 trigger: Optional[pulumi.Input['ScheduledQueryRulesAlertTriggerArgs']] = None):
        """
        Input properties used for looking up and filtering ScheduledQueryRulesAlert resources.
        :param pulumi.Input['ScheduledQueryRulesAlertActionArgs'] action: An `action` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] authorized_resource_ids: List of Resource IDs referred into query.
        :param pulumi.Input[str] data_source_id: The resource URI over which log search query is to be run.
        :param pulumi.Input[str] description: The description of the scheduled query rule.
        :param pulumi.Input[bool] enabled: Whether this scheduled query rule is enabled.  Default is `true`.
        :param pulumi.Input[int] frequency: Frequency (in minutes) at which rule condition should be evaluated.  Values must be between 5 and 1440 (inclusive).
        :param pulumi.Input[str] name: The name of the scheduled query rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] query: Log search query.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the scheduled query rule instance.
        :param pulumi.Input[int] severity: Severity of the alert. Possible values include: 0, 1, 2, 3, or 4.
        :param pulumi.Input[int] throttling: Time (in minutes) for which Alerts should be throttled or suppressed.  Values must be between 0 and 10000 (inclusive).
        :param pulumi.Input[int] time_window: Time window for which data needs to be fetched for query (must be greater than or equal to `frequency`).  Values must be between 5 and 2880 (inclusive).
        :param pulumi.Input['ScheduledQueryRulesAlertTriggerArgs'] trigger: The condition that results in the alert rule being run.
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if authorized_resource_ids is not None:
            pulumi.set(__self__, "authorized_resource_ids", authorized_resource_ids)
        if data_source_id is not None:
            pulumi.set(__self__, "data_source_id", data_source_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if frequency is not None:
            pulumi.set(__self__, "frequency", frequency)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if query is not None:
            pulumi.set(__self__, "query", query)
        if query_type is not None:
            pulumi.set(__self__, "query_type", query_type)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if severity is not None:
            pulumi.set(__self__, "severity", severity)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if throttling is not None:
            pulumi.set(__self__, "throttling", throttling)
        if time_window is not None:
            pulumi.set(__self__, "time_window", time_window)
        if trigger is not None:
            pulumi.set(__self__, "trigger", trigger)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input['ScheduledQueryRulesAlertActionArgs']]:
        """
        An `action` block as defined below.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input['ScheduledQueryRulesAlertActionArgs']]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="authorizedResourceIds")
    def authorized_resource_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Resource IDs referred into query.
        """
        return pulumi.get(self, "authorized_resource_ids")

    @authorized_resource_ids.setter
    def authorized_resource_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "authorized_resource_ids", value)

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource URI over which log search query is to be run.
        """
        return pulumi.get(self, "data_source_id")

    @data_source_id.setter
    def data_source_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_source_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the scheduled query rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether this scheduled query rule is enabled.  Default is `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def frequency(self) -> Optional[pulumi.Input[int]]:
        """
        Frequency (in minutes) at which rule condition should be evaluated.  Values must be between 5 and 1440 (inclusive).
        """
        return pulumi.get(self, "frequency")

    @frequency.setter
    def frequency(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "frequency", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the scheduled query rule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def query(self) -> Optional[pulumi.Input[str]]:
        """
        Log search query.
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter(name="queryType")
    def query_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "query_type")

    @query_type.setter
    def query_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the scheduled query rule instance.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def severity(self) -> Optional[pulumi.Input[int]]:
        """
        Severity of the alert. Possible values include: 0, 1, 2, 3, or 4.
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def throttling(self) -> Optional[pulumi.Input[int]]:
        """
        Time (in minutes) for which Alerts should be throttled or suppressed.  Values must be between 0 and 10000 (inclusive).
        """
        return pulumi.get(self, "throttling")

    @throttling.setter
    def throttling(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throttling", value)

    @property
    @pulumi.getter(name="timeWindow")
    def time_window(self) -> Optional[pulumi.Input[int]]:
        """
        Time window for which data needs to be fetched for query (must be greater than or equal to `frequency`).  Values must be between 5 and 2880 (inclusive).
        """
        return pulumi.get(self, "time_window")

    @time_window.setter
    def time_window(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "time_window", value)

    @property
    @pulumi.getter
    def trigger(self) -> Optional[pulumi.Input['ScheduledQueryRulesAlertTriggerArgs']]:
        """
        The condition that results in the alert rule being run.
        """
        return pulumi.get(self, "trigger")

    @trigger.setter
    def trigger(self, value: Optional[pulumi.Input['ScheduledQueryRulesAlertTriggerArgs']]):
        pulumi.set(self, "trigger", value)


class ScheduledQueryRulesAlert(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertActionArgs']]] = None,
                 authorized_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_source_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 frequency: Optional[pulumi.Input[int]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 query_type: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throttling: Optional[pulumi.Input[int]] = None,
                 time_window: Optional[pulumi.Input[int]] = None,
                 trigger: Optional[pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertTriggerArgs']]] = None,
                 __props__=None):
        """
        Manages an AlertingAction Scheduled Query Rules resource within Azure Monitor.

        ## Import

        Scheduled Query Rule Alerts can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:monitoring/scheduledQueryRulesAlert:ScheduledQueryRulesAlert example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Insights/scheduledQueryRules/myrulename
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertActionArgs']] action: An `action` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] authorized_resource_ids: List of Resource IDs referred into query.
        :param pulumi.Input[str] data_source_id: The resource URI over which log search query is to be run.
        :param pulumi.Input[str] description: The description of the scheduled query rule.
        :param pulumi.Input[bool] enabled: Whether this scheduled query rule is enabled.  Default is `true`.
        :param pulumi.Input[int] frequency: Frequency (in minutes) at which rule condition should be evaluated.  Values must be between 5 and 1440 (inclusive).
        :param pulumi.Input[str] name: The name of the scheduled query rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] query: Log search query.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the scheduled query rule instance.
        :param pulumi.Input[int] severity: Severity of the alert. Possible values include: 0, 1, 2, 3, or 4.
        :param pulumi.Input[int] throttling: Time (in minutes) for which Alerts should be throttled or suppressed.  Values must be between 0 and 10000 (inclusive).
        :param pulumi.Input[int] time_window: Time window for which data needs to be fetched for query (must be greater than or equal to `frequency`).  Values must be between 5 and 2880 (inclusive).
        :param pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertTriggerArgs']] trigger: The condition that results in the alert rule being run.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ScheduledQueryRulesAlertArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an AlertingAction Scheduled Query Rules resource within Azure Monitor.

        ## Import

        Scheduled Query Rule Alerts can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:monitoring/scheduledQueryRulesAlert:ScheduledQueryRulesAlert example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Insights/scheduledQueryRules/myrulename
        ```

        :param str resource_name: The name of the resource.
        :param ScheduledQueryRulesAlertArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScheduledQueryRulesAlertArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertActionArgs']]] = None,
                 authorized_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_source_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 frequency: Optional[pulumi.Input[int]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 query_type: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throttling: Optional[pulumi.Input[int]] = None,
                 time_window: Optional[pulumi.Input[int]] = None,
                 trigger: Optional[pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertTriggerArgs']]] = None,
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
            __props__ = ScheduledQueryRulesAlertArgs.__new__(ScheduledQueryRulesAlertArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            __props__.__dict__["authorized_resource_ids"] = authorized_resource_ids
            if data_source_id is None and not opts.urn:
                raise TypeError("Missing required property 'data_source_id'")
            __props__.__dict__["data_source_id"] = data_source_id
            __props__.__dict__["description"] = description
            __props__.__dict__["enabled"] = enabled
            if frequency is None and not opts.urn:
                raise TypeError("Missing required property 'frequency'")
            __props__.__dict__["frequency"] = frequency
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if query is None and not opts.urn:
                raise TypeError("Missing required property 'query'")
            __props__.__dict__["query"] = query
            __props__.__dict__["query_type"] = query_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["severity"] = severity
            __props__.__dict__["tags"] = tags
            __props__.__dict__["throttling"] = throttling
            if time_window is None and not opts.urn:
                raise TypeError("Missing required property 'time_window'")
            __props__.__dict__["time_window"] = time_window
            if trigger is None and not opts.urn:
                raise TypeError("Missing required property 'trigger'")
            __props__.__dict__["trigger"] = trigger
        super(ScheduledQueryRulesAlert, __self__).__init__(
            'azure:monitoring/scheduledQueryRulesAlert:ScheduledQueryRulesAlert',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            action: Optional[pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertActionArgs']]] = None,
            authorized_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            data_source_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            frequency: Optional[pulumi.Input[int]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            query: Optional[pulumi.Input[str]] = None,
            query_type: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            severity: Optional[pulumi.Input[int]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            throttling: Optional[pulumi.Input[int]] = None,
            time_window: Optional[pulumi.Input[int]] = None,
            trigger: Optional[pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertTriggerArgs']]] = None) -> 'ScheduledQueryRulesAlert':
        """
        Get an existing ScheduledQueryRulesAlert resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertActionArgs']] action: An `action` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] authorized_resource_ids: List of Resource IDs referred into query.
        :param pulumi.Input[str] data_source_id: The resource URI over which log search query is to be run.
        :param pulumi.Input[str] description: The description of the scheduled query rule.
        :param pulumi.Input[bool] enabled: Whether this scheduled query rule is enabled.  Default is `true`.
        :param pulumi.Input[int] frequency: Frequency (in minutes) at which rule condition should be evaluated.  Values must be between 5 and 1440 (inclusive).
        :param pulumi.Input[str] name: The name of the scheduled query rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] query: Log search query.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the scheduled query rule instance.
        :param pulumi.Input[int] severity: Severity of the alert. Possible values include: 0, 1, 2, 3, or 4.
        :param pulumi.Input[int] throttling: Time (in minutes) for which Alerts should be throttled or suppressed.  Values must be between 0 and 10000 (inclusive).
        :param pulumi.Input[int] time_window: Time window for which data needs to be fetched for query (must be greater than or equal to `frequency`).  Values must be between 5 and 2880 (inclusive).
        :param pulumi.Input[pulumi.InputType['ScheduledQueryRulesAlertTriggerArgs']] trigger: The condition that results in the alert rule being run.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ScheduledQueryRulesAlertState.__new__(_ScheduledQueryRulesAlertState)

        __props__.__dict__["action"] = action
        __props__.__dict__["authorized_resource_ids"] = authorized_resource_ids
        __props__.__dict__["data_source_id"] = data_source_id
        __props__.__dict__["description"] = description
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["frequency"] = frequency
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["query"] = query
        __props__.__dict__["query_type"] = query_type
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["severity"] = severity
        __props__.__dict__["tags"] = tags
        __props__.__dict__["throttling"] = throttling
        __props__.__dict__["time_window"] = time_window
        __props__.__dict__["trigger"] = trigger
        return ScheduledQueryRulesAlert(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output['outputs.ScheduledQueryRulesAlertAction']:
        """
        An `action` block as defined below.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="authorizedResourceIds")
    def authorized_resource_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of Resource IDs referred into query.
        """
        return pulumi.get(self, "authorized_resource_ids")

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> pulumi.Output[str]:
        """
        The resource URI over which log search query is to be run.
        """
        return pulumi.get(self, "data_source_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the scheduled query rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether this scheduled query rule is enabled.  Default is `true`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Output[int]:
        """
        Frequency (in minutes) at which rule condition should be evaluated.  Values must be between 5 and 1440 (inclusive).
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the scheduled query rule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def query(self) -> pulumi.Output[str]:
        """
        Log search query.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter(name="queryType")
    def query_type(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "query_type")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the scheduled query rule instance.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Output[Optional[int]]:
        """
        Severity of the alert. Possible values include: 0, 1, 2, 3, or 4.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def throttling(self) -> pulumi.Output[Optional[int]]:
        """
        Time (in minutes) for which Alerts should be throttled or suppressed.  Values must be between 0 and 10000 (inclusive).
        """
        return pulumi.get(self, "throttling")

    @property
    @pulumi.getter(name="timeWindow")
    def time_window(self) -> pulumi.Output[int]:
        """
        Time window for which data needs to be fetched for query (must be greater than or equal to `frequency`).  Values must be between 5 and 2880 (inclusive).
        """
        return pulumi.get(self, "time_window")

    @property
    @pulumi.getter
    def trigger(self) -> pulumi.Output['outputs.ScheduledQueryRulesAlertTrigger']:
        """
        The condition that results in the alert rule being run.
        """
        return pulumi.get(self, "trigger")

