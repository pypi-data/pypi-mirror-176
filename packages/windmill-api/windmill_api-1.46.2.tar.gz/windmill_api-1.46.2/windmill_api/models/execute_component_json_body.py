from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.execute_component_json_body_raw_code import ExecuteComponentJsonBodyRawCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExecuteComponentJsonBody")


@attr.s(auto_attribs=True)
class ExecuteComponentJsonBody:
    """
    Attributes:
        args (Any):
        path (Union[Unset, str]):
        raw_code (Union[Unset, ExecuteComponentJsonBodyRawCode]):
    """

    args: Any
    path: Union[Unset, str] = UNSET
    raw_code: Union[Unset, ExecuteComponentJsonBodyRawCode] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        args = self.args
        path = self.path
        raw_code: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.raw_code, Unset):
            raw_code = self.raw_code.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "args": args,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if raw_code is not UNSET:
            field_dict["raw_code"] = raw_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        args = d.pop("args")

        path = d.pop("path", UNSET)

        _raw_code = d.pop("raw_code", UNSET)
        raw_code: Union[Unset, ExecuteComponentJsonBodyRawCode]
        if isinstance(_raw_code, Unset):
            raw_code = UNSET
        else:
            raw_code = ExecuteComponentJsonBodyRawCode.from_dict(_raw_code)

        execute_component_json_body = cls(
            args=args,
            path=path,
            raw_code=raw_code,
        )

        execute_component_json_body.additional_properties = d
        return execute_component_json_body

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
