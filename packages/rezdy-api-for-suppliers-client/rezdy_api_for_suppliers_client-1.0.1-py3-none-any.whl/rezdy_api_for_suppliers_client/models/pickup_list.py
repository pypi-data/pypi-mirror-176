from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pickup_location import PickupLocation
from ..types import UNSET, Unset

T = TypeVar("T", bound="PickupList")


@attr.s(auto_attribs=True)
class PickupList:
    """PickupList object. Contains a list of pickup locations.

    Attributes:
        additional_notes (Union[Unset, str]): Global additional instructions for this pick up list
        id (Union[Unset, int]): ID of this pickup
        name (Union[Unset, str]): Name of the pickup location list
        other_location_instructions (Union[Unset, str]): Instructions for other locations that are not available in the
            pickupLocations list. E.g. For customer pick up location requests, a sample instruction for this field would be:
            'We will contact you to confirm your pickup location'
        pickup_locations (Union[Unset, List[PickupLocation]]): List of all associated pickup locations for this list
    """

    additional_notes: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    other_location_instructions: Union[Unset, str] = UNSET
    pickup_locations: Union[Unset, List[PickupLocation]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        additional_notes = self.additional_notes
        id = self.id
        name = self.name
        other_location_instructions = self.other_location_instructions
        pickup_locations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pickup_locations, Unset):
            pickup_locations = []
            for pickup_locations_item_data in self.pickup_locations:
                pickup_locations_item = pickup_locations_item_data.to_dict()

                pickup_locations.append(pickup_locations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if additional_notes is not UNSET:
            field_dict["additionalNotes"] = additional_notes
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if other_location_instructions is not UNSET:
            field_dict["otherLocationInstructions"] = other_location_instructions
        if pickup_locations is not UNSET:
            field_dict["pickupLocations"] = pickup_locations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        additional_notes = d.pop("additionalNotes", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        other_location_instructions = d.pop("otherLocationInstructions", UNSET)

        pickup_locations = []
        _pickup_locations = d.pop("pickupLocations", UNSET)
        for pickup_locations_item_data in _pickup_locations or []:
            pickup_locations_item = PickupLocation.from_dict(pickup_locations_item_data)

            pickup_locations.append(pickup_locations_item)

        pickup_list = cls(
            additional_notes=additional_notes,
            id=id,
            name=name,
            other_location_instructions=other_location_instructions,
            pickup_locations=pickup_locations,
        )

        pickup_list.additional_properties = d
        return pickup_list

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
