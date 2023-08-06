from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pickup_list import PickupList
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponsePickupList")


@attr.s(auto_attribs=True)
class ResponsePickupList:
    """
    Attributes:
        request_status (RequestStatus):
        pickup_list (Union[Unset, PickupList]): PickupList object. Contains a list of pickup locations.
    """

    request_status: RequestStatus
    pickup_list: Union[Unset, PickupList] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        pickup_list: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pickup_list, Unset):
            pickup_list = self.pickup_list.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if pickup_list is not UNSET:
            field_dict["pickupList"] = pickup_list

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _pickup_list = d.pop("pickupList", UNSET)
        pickup_list: Union[Unset, PickupList]
        if isinstance(_pickup_list, Unset):
            pickup_list = UNSET
        else:
            pickup_list = PickupList.from_dict(_pickup_list)

        response_pickup_list = cls(
            request_status=request_status,
            pickup_list=pickup_list,
        )

        response_pickup_list.additional_properties = d
        return response_pickup_list

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
