from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pickup_list import PickupList
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponsePickupListList")


@attr.s(auto_attribs=True)
class ResponsePickupListList:
    """
    Attributes:
        request_status (RequestStatus):
        pickup_list_list (Union[Unset, List[PickupList]]):
    """

    request_status: RequestStatus
    pickup_list_list: Union[Unset, List[PickupList]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        pickup_list_list: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pickup_list_list, Unset):
            pickup_list_list = []
            for pickup_list_list_item_data in self.pickup_list_list:
                pickup_list_list_item = pickup_list_list_item_data.to_dict()

                pickup_list_list.append(pickup_list_list_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if pickup_list_list is not UNSET:
            field_dict["pickupListList"] = pickup_list_list

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        pickup_list_list = []
        _pickup_list_list = d.pop("pickupListList", UNSET)
        for pickup_list_list_item_data in _pickup_list_list or []:
            pickup_list_list_item = PickupList.from_dict(pickup_list_list_item_data)

            pickup_list_list.append(pickup_list_list_item)

        response_pickup_list_list = cls(
            request_status=request_status,
            pickup_list_list=pickup_list_list,
        )

        response_pickup_list_list.additional_properties = d
        return response_pickup_list_list

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
