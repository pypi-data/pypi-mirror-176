from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.rate import Rate
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseRate")


@attr.s(auto_attribs=True)
class ResponseRate:
    """
    Attributes:
        request_status (RequestStatus):
        rate (Union[Unset, Rate]): A Rate is used to group products with its corresponding shared rate
    """

    request_status: RequestStatus
    rate: Union[Unset, Rate] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        rate: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rate, Unset):
            rate = self.rate.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if rate is not UNSET:
            field_dict["rate"] = rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _rate = d.pop("rate", UNSET)
        rate: Union[Unset, Rate]
        if isinstance(_rate, Unset):
            rate = UNSET
        else:
            rate = Rate.from_dict(_rate)

        response_rate = cls(
            request_status=request_status,
            rate=rate,
        )

        response_rate.additional_properties = d
        return response_rate

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
