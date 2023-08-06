from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pickup_location import PickupLocation
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponsePickupLocationList")


@attr.s(auto_attribs=True)
class ResponsePickupLocationList:
    """
    Attributes:
        request_status (RequestStatus):
        pickup_locations (Union[Unset, List[PickupLocation]]):
    """

    request_status: RequestStatus
    pickup_locations: Union[Unset, List[PickupLocation]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        pickup_locations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pickup_locations, Unset):
            pickup_locations = []
            for pickup_locations_item_data in self.pickup_locations:
                pickup_locations_item = pickup_locations_item_data.to_dict()

                pickup_locations.append(pickup_locations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if pickup_locations is not UNSET:
            field_dict["pickupLocations"] = pickup_locations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        pickup_locations = []
        _pickup_locations = d.pop("pickupLocations", UNSET)
        for pickup_locations_item_data in _pickup_locations or []:
            pickup_locations_item = PickupLocation.from_dict(pickup_locations_item_data)

            pickup_locations.append(pickup_locations_item)

        response_pickup_location_list = cls(
            request_status=request_status,
            pickup_locations=pickup_locations,
        )

        response_pickup_location_list.additional_properties = d
        return response_pickup_location_list

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
