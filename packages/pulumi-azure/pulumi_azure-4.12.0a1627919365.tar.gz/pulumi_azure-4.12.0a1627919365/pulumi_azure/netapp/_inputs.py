# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'AccountActiveDirectoryArgs',
    'VolumeDataProtectionReplicationArgs',
    'VolumeExportPolicyRuleArgs',
]

@pulumi.input_type
class AccountActiveDirectoryArgs:
    def __init__(__self__, *,
                 dns_servers: pulumi.Input[Sequence[pulumi.Input[str]]],
                 domain: pulumi.Input[str],
                 password: pulumi.Input[str],
                 smb_server_name: pulumi.Input[str],
                 username: pulumi.Input[str],
                 organizational_unit: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of DNS server IP addresses for the Active Directory domain. Only allows `IPv4` address.
        :param pulumi.Input[str] domain: The name of the Active Directory domain.
        :param pulumi.Input[str] password: The password associated with the `username`.
        :param pulumi.Input[str] smb_server_name: The NetBIOS name which should be used for the NetApp SMB Server, which will be registered as a computer account in the AD and used to mount volumes.
        :param pulumi.Input[str] username: The Username of Active Directory Domain Administrator.
        :param pulumi.Input[str] organizational_unit: The Organizational Unit (OU) within the Active Directory Domain.
        """
        pulumi.set(__self__, "dns_servers", dns_servers)
        pulumi.set(__self__, "domain", domain)
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "smb_server_name", smb_server_name)
        pulumi.set(__self__, "username", username)
        if organizational_unit is not None:
            pulumi.set(__self__, "organizational_unit", organizational_unit)

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of DNS server IP addresses for the Active Directory domain. Only allows `IPv4` address.
        """
        return pulumi.get(self, "dns_servers")

    @dns_servers.setter
    def dns_servers(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "dns_servers", value)

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Input[str]:
        """
        The name of the Active Directory domain.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        """
        The password associated with the `username`.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="smbServerName")
    def smb_server_name(self) -> pulumi.Input[str]:
        """
        The NetBIOS name which should be used for the NetApp SMB Server, which will be registered as a computer account in the AD and used to mount volumes.
        """
        return pulumi.get(self, "smb_server_name")

    @smb_server_name.setter
    def smb_server_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "smb_server_name", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The Username of Active Directory Domain Administrator.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter(name="organizationalUnit")
    def organizational_unit(self) -> Optional[pulumi.Input[str]]:
        """
        The Organizational Unit (OU) within the Active Directory Domain.
        """
        return pulumi.get(self, "organizational_unit")

    @organizational_unit.setter
    def organizational_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organizational_unit", value)


@pulumi.input_type
class VolumeDataProtectionReplicationArgs:
    def __init__(__self__, *,
                 remote_volume_location: pulumi.Input[str],
                 remote_volume_resource_id: pulumi.Input[str],
                 replication_frequency: pulumi.Input[str],
                 endpoint_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] remote_volume_location: Location of the primary volume.
        :param pulumi.Input[str] remote_volume_resource_id: Resource ID of the primary volume.
        :param pulumi.Input[str] replication_frequency: Replication frequency, supported values are '10minutes', 'hourly', 'daily', values are case sensitive.
        :param pulumi.Input[str] endpoint_type: The endpoint type, default value is `dst` for destination.
        """
        pulumi.set(__self__, "remote_volume_location", remote_volume_location)
        pulumi.set(__self__, "remote_volume_resource_id", remote_volume_resource_id)
        pulumi.set(__self__, "replication_frequency", replication_frequency)
        if endpoint_type is not None:
            pulumi.set(__self__, "endpoint_type", endpoint_type)

    @property
    @pulumi.getter(name="remoteVolumeLocation")
    def remote_volume_location(self) -> pulumi.Input[str]:
        """
        Location of the primary volume.
        """
        return pulumi.get(self, "remote_volume_location")

    @remote_volume_location.setter
    def remote_volume_location(self, value: pulumi.Input[str]):
        pulumi.set(self, "remote_volume_location", value)

    @property
    @pulumi.getter(name="remoteVolumeResourceId")
    def remote_volume_resource_id(self) -> pulumi.Input[str]:
        """
        Resource ID of the primary volume.
        """
        return pulumi.get(self, "remote_volume_resource_id")

    @remote_volume_resource_id.setter
    def remote_volume_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "remote_volume_resource_id", value)

    @property
    @pulumi.getter(name="replicationFrequency")
    def replication_frequency(self) -> pulumi.Input[str]:
        """
        Replication frequency, supported values are '10minutes', 'hourly', 'daily', values are case sensitive.
        """
        return pulumi.get(self, "replication_frequency")

    @replication_frequency.setter
    def replication_frequency(self, value: pulumi.Input[str]):
        pulumi.set(self, "replication_frequency", value)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> Optional[pulumi.Input[str]]:
        """
        The endpoint type, default value is `dst` for destination.
        """
        return pulumi.get(self, "endpoint_type")

    @endpoint_type.setter
    def endpoint_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_type", value)


@pulumi.input_type
class VolumeExportPolicyRuleArgs:
    def __init__(__self__, *,
                 allowed_clients: pulumi.Input[Sequence[pulumi.Input[str]]],
                 rule_index: pulumi.Input[int],
                 cifs_enabled: Optional[pulumi.Input[bool]] = None,
                 nfsv3_enabled: Optional[pulumi.Input[bool]] = None,
                 nfsv4_enabled: Optional[pulumi.Input[bool]] = None,
                 protocols_enabled: Optional[pulumi.Input[str]] = None,
                 root_access_enabled: Optional[pulumi.Input[bool]] = None,
                 unix_read_only: Optional[pulumi.Input[bool]] = None,
                 unix_read_write: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_clients: A list of allowed clients IPv4 addresses.
        :param pulumi.Input[int] rule_index: The index number of the rule.
        :param pulumi.Input[bool] cifs_enabled: Is the CIFS protocol allowed?
        :param pulumi.Input[bool] nfsv3_enabled: Is the NFSv3 protocol allowed?
        :param pulumi.Input[bool] nfsv4_enabled: Is the NFSv4 protocol allowed?
        :param pulumi.Input[str] protocols_enabled: A list of allowed protocols. Valid values include `CIFS`, `NFSv3`, or `NFSv4.1`. Only one value is supported at this time. This replaces the previous arguments: `cifs_enabled`, `nfsv3_enabled` and `nfsv4_enabled`.
        :param pulumi.Input[bool] root_access_enabled: Is root access permitted to this volume?
        :param pulumi.Input[bool] unix_read_only: Is the file system on unix read only?
        :param pulumi.Input[bool] unix_read_write: Is the file system on unix read and write?
        """
        pulumi.set(__self__, "allowed_clients", allowed_clients)
        pulumi.set(__self__, "rule_index", rule_index)
        if cifs_enabled is not None:
            warnings.warn("""Deprecated in favour of `protocols_enabled`""", DeprecationWarning)
            pulumi.log.warn("""cifs_enabled is deprecated: Deprecated in favour of `protocols_enabled`""")
        if cifs_enabled is not None:
            pulumi.set(__self__, "cifs_enabled", cifs_enabled)
        if nfsv3_enabled is not None:
            warnings.warn("""Deprecated in favour of `protocols_enabled`""", DeprecationWarning)
            pulumi.log.warn("""nfsv3_enabled is deprecated: Deprecated in favour of `protocols_enabled`""")
        if nfsv3_enabled is not None:
            pulumi.set(__self__, "nfsv3_enabled", nfsv3_enabled)
        if nfsv4_enabled is not None:
            warnings.warn("""Deprecated in favour of `protocols_enabled`""", DeprecationWarning)
            pulumi.log.warn("""nfsv4_enabled is deprecated: Deprecated in favour of `protocols_enabled`""")
        if nfsv4_enabled is not None:
            pulumi.set(__self__, "nfsv4_enabled", nfsv4_enabled)
        if protocols_enabled is not None:
            pulumi.set(__self__, "protocols_enabled", protocols_enabled)
        if root_access_enabled is not None:
            pulumi.set(__self__, "root_access_enabled", root_access_enabled)
        if unix_read_only is not None:
            pulumi.set(__self__, "unix_read_only", unix_read_only)
        if unix_read_write is not None:
            pulumi.set(__self__, "unix_read_write", unix_read_write)

    @property
    @pulumi.getter(name="allowedClients")
    def allowed_clients(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of allowed clients IPv4 addresses.
        """
        return pulumi.get(self, "allowed_clients")

    @allowed_clients.setter
    def allowed_clients(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "allowed_clients", value)

    @property
    @pulumi.getter(name="ruleIndex")
    def rule_index(self) -> pulumi.Input[int]:
        """
        The index number of the rule.
        """
        return pulumi.get(self, "rule_index")

    @rule_index.setter
    def rule_index(self, value: pulumi.Input[int]):
        pulumi.set(self, "rule_index", value)

    @property
    @pulumi.getter(name="cifsEnabled")
    def cifs_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the CIFS protocol allowed?
        """
        return pulumi.get(self, "cifs_enabled")

    @cifs_enabled.setter
    def cifs_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cifs_enabled", value)

    @property
    @pulumi.getter(name="nfsv3Enabled")
    def nfsv3_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the NFSv3 protocol allowed?
        """
        return pulumi.get(self, "nfsv3_enabled")

    @nfsv3_enabled.setter
    def nfsv3_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "nfsv3_enabled", value)

    @property
    @pulumi.getter(name="nfsv4Enabled")
    def nfsv4_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the NFSv4 protocol allowed?
        """
        return pulumi.get(self, "nfsv4_enabled")

    @nfsv4_enabled.setter
    def nfsv4_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "nfsv4_enabled", value)

    @property
    @pulumi.getter(name="protocolsEnabled")
    def protocols_enabled(self) -> Optional[pulumi.Input[str]]:
        """
        A list of allowed protocols. Valid values include `CIFS`, `NFSv3`, or `NFSv4.1`. Only one value is supported at this time. This replaces the previous arguments: `cifs_enabled`, `nfsv3_enabled` and `nfsv4_enabled`.
        """
        return pulumi.get(self, "protocols_enabled")

    @protocols_enabled.setter
    def protocols_enabled(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocols_enabled", value)

    @property
    @pulumi.getter(name="rootAccessEnabled")
    def root_access_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is root access permitted to this volume?
        """
        return pulumi.get(self, "root_access_enabled")

    @root_access_enabled.setter
    def root_access_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "root_access_enabled", value)

    @property
    @pulumi.getter(name="unixReadOnly")
    def unix_read_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the file system on unix read only?
        """
        return pulumi.get(self, "unix_read_only")

    @unix_read_only.setter
    def unix_read_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "unix_read_only", value)

    @property
    @pulumi.getter(name="unixReadWrite")
    def unix_read_write(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the file system on unix read and write?
        """
        return pulumi.get(self, "unix_read_write")

    @unix_read_write.setter
    def unix_read_write(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "unix_read_write", value)


