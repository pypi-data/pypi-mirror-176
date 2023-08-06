import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.app_with_last_version_execution_mode import AppWithLastVersionExecutionMode
from ..models.app_with_last_version_extra_perms import AppWithLastVersionExtraPerms
from ..models.app_with_last_version_policy import AppWithLastVersionPolicy
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppWithLastVersion")


@attr.s(auto_attribs=True)
class AppWithLastVersion:
    """
    Attributes:
        id (Union[Unset, int]):
        workspace_id (Union[Unset, str]):
        path (Union[Unset, str]):
        summary (Union[Unset, str]):
        versions (Union[Unset, List[int]]):
        created_by (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        value (Union[Unset, Any]):
        policy (Union[Unset, AppWithLastVersionPolicy]):
        execution_mode (Union[Unset, AppWithLastVersionExecutionMode]):
        extra_perms (Union[Unset, AppWithLastVersionExtraPerms]):
    """

    id: Union[Unset, int] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    summary: Union[Unset, str] = UNSET
    versions: Union[Unset, List[int]] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    value: Union[Unset, Any] = UNSET
    policy: Union[Unset, AppWithLastVersionPolicy] = UNSET
    execution_mode: Union[Unset, AppWithLastVersionExecutionMode] = UNSET
    extra_perms: Union[Unset, AppWithLastVersionExtraPerms] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id
        path = self.path
        summary = self.summary
        versions: Union[Unset, List[int]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = self.versions

        created_by = self.created_by
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        value = self.value
        policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.to_dict()

        execution_mode: Union[Unset, str] = UNSET
        if not isinstance(self.execution_mode, Unset):
            execution_mode = self.execution_mode.value

        extra_perms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_perms, Unset):
            extra_perms = self.extra_perms.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if path is not UNSET:
            field_dict["path"] = path
        if summary is not UNSET:
            field_dict["summary"] = summary
        if versions is not UNSET:
            field_dict["versions"] = versions
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if value is not UNSET:
            field_dict["value"] = value
        if policy is not UNSET:
            field_dict["policy"] = policy
        if execution_mode is not UNSET:
            field_dict["execution_mode"] = execution_mode
        if extra_perms is not UNSET:
            field_dict["extra_perms"] = extra_perms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        path = d.pop("path", UNSET)

        summary = d.pop("summary", UNSET)

        versions = cast(List[int], d.pop("versions", UNSET))

        created_by = d.pop("created_by", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        value = d.pop("value", UNSET)

        _policy = d.pop("policy", UNSET)
        policy: Union[Unset, AppWithLastVersionPolicy]
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = AppWithLastVersionPolicy.from_dict(_policy)

        _execution_mode = d.pop("execution_mode", UNSET)
        execution_mode: Union[Unset, AppWithLastVersionExecutionMode]
        if isinstance(_execution_mode, Unset):
            execution_mode = UNSET
        else:
            execution_mode = AppWithLastVersionExecutionMode(_execution_mode)

        _extra_perms = d.pop("extra_perms", UNSET)
        extra_perms: Union[Unset, AppWithLastVersionExtraPerms]
        if isinstance(_extra_perms, Unset):
            extra_perms = UNSET
        else:
            extra_perms = AppWithLastVersionExtraPerms.from_dict(_extra_perms)

        app_with_last_version = cls(
            id=id,
            workspace_id=workspace_id,
            path=path,
            summary=summary,
            versions=versions,
            created_by=created_by,
            created_at=created_at,
            value=value,
            policy=policy,
            execution_mode=execution_mode,
            extra_perms=extra_perms,
        )

        app_with_last_version.additional_properties = d
        return app_with_last_version

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
