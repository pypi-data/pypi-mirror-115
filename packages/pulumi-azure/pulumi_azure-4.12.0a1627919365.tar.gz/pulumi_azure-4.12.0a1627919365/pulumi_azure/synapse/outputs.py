# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'SparkPoolAutoPause',
    'SparkPoolAutoScale',
    'SparkPoolLibraryRequirement',
    'SqlPoolRestore',
    'WorkspaceAadAdmin',
    'WorkspaceAzureDevopsRepo',
    'WorkspaceGithubRepo',
    'WorkspaceIdentity',
    'GetWorkspaceIdentityResult',
]

@pulumi.output_type
class SparkPoolAutoPause(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "delayInMinutes":
            suggest = "delay_in_minutes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SparkPoolAutoPause. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SparkPoolAutoPause.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SparkPoolAutoPause.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 delay_in_minutes: int):
        """
        :param int delay_in_minutes: Number of minutes of idle time before the Spark Pool is automatically paused. Must be between `5` and `10080`.
        """
        pulumi.set(__self__, "delay_in_minutes", delay_in_minutes)

    @property
    @pulumi.getter(name="delayInMinutes")
    def delay_in_minutes(self) -> int:
        """
        Number of minutes of idle time before the Spark Pool is automatically paused. Must be between `5` and `10080`.
        """
        return pulumi.get(self, "delay_in_minutes")


@pulumi.output_type
class SparkPoolAutoScale(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "maxNodeCount":
            suggest = "max_node_count"
        elif key == "minNodeCount":
            suggest = "min_node_count"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SparkPoolAutoScale. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SparkPoolAutoScale.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SparkPoolAutoScale.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 max_node_count: int,
                 min_node_count: int):
        """
        :param int max_node_count: The maximum number of nodes the Spark Pool can support. Must be between `3` and `200`.
        :param int min_node_count: The minimum number of nodes the Spark Pool can support. Must be between `3` and `200`.
        """
        pulumi.set(__self__, "max_node_count", max_node_count)
        pulumi.set(__self__, "min_node_count", min_node_count)

    @property
    @pulumi.getter(name="maxNodeCount")
    def max_node_count(self) -> int:
        """
        The maximum number of nodes the Spark Pool can support. Must be between `3` and `200`.
        """
        return pulumi.get(self, "max_node_count")

    @property
    @pulumi.getter(name="minNodeCount")
    def min_node_count(self) -> int:
        """
        The minimum number of nodes the Spark Pool can support. Must be between `3` and `200`.
        """
        return pulumi.get(self, "min_node_count")


@pulumi.output_type
class SparkPoolLibraryRequirement(dict):
    def __init__(__self__, *,
                 content: str,
                 filename: str):
        """
        :param str content: The content of library requirements.
        :param str filename: The name of the library requirements file.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "filename", filename)

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        The content of library requirements.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter
    def filename(self) -> str:
        """
        The name of the library requirements file.
        """
        return pulumi.get(self, "filename")


@pulumi.output_type
class SqlPoolRestore(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "pointInTime":
            suggest = "point_in_time"
        elif key == "sourceDatabaseId":
            suggest = "source_database_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SqlPoolRestore. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SqlPoolRestore.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SqlPoolRestore.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 point_in_time: str,
                 source_database_id: str):
        """
        :param str point_in_time: Specifies the Snapshot time to restore. Changing this forces a new Synapse Sql Pool to be created.
        :param str source_database_id: The ID of the Synapse Sql Pool or Sql Database which is to restore. Changing this forces a new Synapse Sql Pool to be created.
        """
        pulumi.set(__self__, "point_in_time", point_in_time)
        pulumi.set(__self__, "source_database_id", source_database_id)

    @property
    @pulumi.getter(name="pointInTime")
    def point_in_time(self) -> str:
        """
        Specifies the Snapshot time to restore. Changing this forces a new Synapse Sql Pool to be created.
        """
        return pulumi.get(self, "point_in_time")

    @property
    @pulumi.getter(name="sourceDatabaseId")
    def source_database_id(self) -> str:
        """
        The ID of the Synapse Sql Pool or Sql Database which is to restore. Changing this forces a new Synapse Sql Pool to be created.
        """
        return pulumi.get(self, "source_database_id")


@pulumi.output_type
class WorkspaceAadAdmin(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "objectId":
            suggest = "object_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceAadAdmin. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceAadAdmin.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceAadAdmin.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 login: str,
                 object_id: str,
                 tenant_id: str):
        """
        :param str login: The login name of the Azure AD Administrator of this Synapse Workspace.
        :param str object_id: The object id of the Azure AD Administrator of this Synapse Workspace.
        :param str tenant_id: The tenant id of the Azure AD Administrator of this Synapse Workspace.
        """
        pulumi.set(__self__, "login", login)
        pulumi.set(__self__, "object_id", object_id)
        pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def login(self) -> str:
        """
        The login name of the Azure AD Administrator of this Synapse Workspace.
        """
        return pulumi.get(self, "login")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> str:
        """
        The object id of the Azure AD Administrator of this Synapse Workspace.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant id of the Azure AD Administrator of this Synapse Workspace.
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class WorkspaceAzureDevopsRepo(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accountName":
            suggest = "account_name"
        elif key == "branchName":
            suggest = "branch_name"
        elif key == "projectName":
            suggest = "project_name"
        elif key == "repositoryName":
            suggest = "repository_name"
        elif key == "rootFolder":
            suggest = "root_folder"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceAzureDevopsRepo. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceAzureDevopsRepo.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceAzureDevopsRepo.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 account_name: str,
                 branch_name: str,
                 project_name: str,
                 repository_name: str,
                 root_folder: str):
        """
        :param str account_name: Specifies the Azure DevOps account name.
        :param str branch_name: Specifies the collaboration branch of the repository to get code from.
        :param str project_name: Specifies the name of the Azure DevOps project.
        :param str repository_name: Specifies the name of the git repository.
        :param str root_folder: Specifies the root folder within the repository. Set to `/` for the top level.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "branch_name", branch_name)
        pulumi.set(__self__, "project_name", project_name)
        pulumi.set(__self__, "repository_name", repository_name)
        pulumi.set(__self__, "root_folder", root_folder)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> str:
        """
        Specifies the Azure DevOps account name.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> str:
        """
        Specifies the collaboration branch of the repository to get code from.
        """
        return pulumi.get(self, "branch_name")

    @property
    @pulumi.getter(name="projectName")
    def project_name(self) -> str:
        """
        Specifies the name of the Azure DevOps project.
        """
        return pulumi.get(self, "project_name")

    @property
    @pulumi.getter(name="repositoryName")
    def repository_name(self) -> str:
        """
        Specifies the name of the git repository.
        """
        return pulumi.get(self, "repository_name")

    @property
    @pulumi.getter(name="rootFolder")
    def root_folder(self) -> str:
        """
        Specifies the root folder within the repository. Set to `/` for the top level.
        """
        return pulumi.get(self, "root_folder")


@pulumi.output_type
class WorkspaceGithubRepo(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accountName":
            suggest = "account_name"
        elif key == "branchName":
            suggest = "branch_name"
        elif key == "repositoryName":
            suggest = "repository_name"
        elif key == "rootFolder":
            suggest = "root_folder"
        elif key == "gitUrl":
            suggest = "git_url"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceGithubRepo. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceGithubRepo.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceGithubRepo.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 account_name: str,
                 branch_name: str,
                 repository_name: str,
                 root_folder: str,
                 git_url: Optional[str] = None):
        """
        :param str account_name: Specifies the GitHub account name.
        :param str branch_name: Specifies the collaboration branch of the repository to get code from.
        :param str repository_name: Specifies the name of the git repository.
        :param str root_folder: Specifies the root folder within the repository. Set to `/` for the top level.
        :param str git_url: Specifies the GitHub Enterprise host name. For example: https://github.mydomain.com.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "branch_name", branch_name)
        pulumi.set(__self__, "repository_name", repository_name)
        pulumi.set(__self__, "root_folder", root_folder)
        if git_url is not None:
            pulumi.set(__self__, "git_url", git_url)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> str:
        """
        Specifies the GitHub account name.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> str:
        """
        Specifies the collaboration branch of the repository to get code from.
        """
        return pulumi.get(self, "branch_name")

    @property
    @pulumi.getter(name="repositoryName")
    def repository_name(self) -> str:
        """
        Specifies the name of the git repository.
        """
        return pulumi.get(self, "repository_name")

    @property
    @pulumi.getter(name="rootFolder")
    def root_folder(self) -> str:
        """
        Specifies the root folder within the repository. Set to `/` for the top level.
        """
        return pulumi.get(self, "root_folder")

    @property
    @pulumi.getter(name="gitUrl")
    def git_url(self) -> Optional[str]:
        """
        Specifies the GitHub Enterprise host name. For example: https://github.mydomain.com.
        """
        return pulumi.get(self, "git_url")


@pulumi.output_type
class WorkspaceIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None,
                 type: Optional[str] = None):
        """
        :param str principal_id: The Principal ID for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        :param str tenant_id: The tenant id of the Azure AD Administrator of this Synapse Workspace.
        :param str type: The Identity Type for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        """
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        """
        The Principal ID for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The tenant id of the Azure AD Administrator of this Synapse Workspace.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The Identity Type for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class GetWorkspaceIdentityResult(dict):
    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: str):
        """
        :param str principal_id: The Principal ID for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        :param str tenant_id: The Tenant ID for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        :param str type: The Identity Type for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The Principal ID for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The Tenant ID for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The Identity Type for the Service Principal associated with the Managed Service Identity of this Synapse Workspace.
        """
        return pulumi.get(self, "type")


