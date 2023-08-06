from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extra_request import ExtraRequest
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseExtraList")


@attr.s(auto_attribs=True)
class ResponseExtraList:
    """
    Attributes:
        request_status (RequestStatus):
        extras (Union[Unset, List[ExtraRequest]]):
    """

    request_status: RequestStatus
    extras: Union[Unset, List[ExtraRequest]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        extras: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.extras, Unset):
            extras = []
            for extras_item_data in self.extras:
                extras_item = extras_item_data.to_dict()

                extras.append(extras_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if extras is not UNSET:
            field_dict["extras"] = extras

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        extras = []
        _extras = d.pop("extras", UNSET)
        for extras_item_data in _extras or []:
            extras_item = ExtraRequest.from_dict(extras_item_data)

            extras.append(extras_item)

        response_extra_list = cls(
            request_status=request_status,
            extras=extras,
        )

        response_extra_list.additional_properties = d
        return response_extra_list

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
