from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckIn")


@attr.s(auto_attribs=True)
class CheckIn:
    """Check-in information.

    Attributes:
        is_checke_in (Union[Unset, bool]):
        is_checked_in (Union[Unset, bool]): Check-in status. True if the specified order item / everyone in a session
            (based on the request query), was checked in, false otherwise.
    """

    is_checke_in: Union[Unset, bool] = UNSET
    is_checked_in: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_checke_in = self.is_checke_in
        is_checked_in = self.is_checked_in

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_checke_in is not UNSET:
            field_dict["isCheckeIn"] = is_checke_in
        if is_checked_in is not UNSET:
            field_dict["isCheckedIn"] = is_checked_in

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_checke_in = d.pop("isCheckeIn", UNSET)

        is_checked_in = d.pop("isCheckedIn", UNSET)

        check_in = cls(
            is_checke_in=is_checke_in,
            is_checked_in=is_checked_in,
        )

        check_in.additional_properties = d
        return check_in

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
