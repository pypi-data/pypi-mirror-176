from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.error import Error
from ..models.warning import Warning_
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestStatus")


@attr.s(auto_attribs=True)
class RequestStatus:
    """
    Attributes:
        success (bool):
        error (Union[Unset, Error]):
        version (Union[Unset, str]):
        warning (Union[Unset, Warning_]):
    """

    success: bool
    error: Union[Unset, Error] = UNSET
    version: Union[Unset, str] = UNSET
    warning: Union[Unset, Warning_] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        success = self.success
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        version = self.version
        warning: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.warning, Unset):
            warning = self.warning.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if version is not UNSET:
            field_dict["version"] = version
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        success = d.pop("success")

        _error = d.pop("error", UNSET)
        error: Union[Unset, Error]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = Error.from_dict(_error)

        version = d.pop("version", UNSET)

        _warning = d.pop("warning", UNSET)
        warning: Union[Unset, Warning_]
        if isinstance(_warning, Unset):
            warning = UNSET
        else:
            warning = Warning_.from_dict(_warning)

        request_status = cls(
            success=success,
            error=error,
            version=version,
            warning=warning,
        )

        request_status.additional_properties = d
        return request_status

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
