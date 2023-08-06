from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.check_in import CheckIn
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseCheckIn")


@attr.s(auto_attribs=True)
class ResponseCheckIn:
    """
    Attributes:
        request_status (RequestStatus):
        checkin (Union[Unset, CheckIn]): Check-in information.
    """

    request_status: RequestStatus
    checkin: Union[Unset, CheckIn] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        checkin: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.checkin, Unset):
            checkin = self.checkin.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if checkin is not UNSET:
            field_dict["checkin"] = checkin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _checkin = d.pop("checkin", UNSET)
        checkin: Union[Unset, CheckIn]
        if isinstance(_checkin, Unset):
            checkin = UNSET
        else:
            checkin = CheckIn.from_dict(_checkin)

        response_check_in = cls(
            request_status=request_status,
            checkin=checkin,
        )

        response_check_in.additional_properties = d
        return response_check_in

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
