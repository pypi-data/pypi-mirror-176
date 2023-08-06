from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PickupLocation")


@attr.s(auto_attribs=True)
class PickupLocation:
    """PickupLocation object. Holds information about the a pickup location from the pickup list configured for the
    product.

        Attributes:
            additional_instructions (Union[Unset, str]): Additional instructions for the pickup location.
            address (Union[Unset, str]): Address of the pickup location<br>In a booking item object, it represents a chosen
                pickup address for the booked item.
            latitude (Union[Unset, float]): google maps calculated latitude of the pickup address
            location_name (Union[Unset, str]): <p>Pickup location name - free text name for the location.</p>In a booking
                item object, it represents customer's pickup location name (if configured on product). It can be one name from
                pickup locations list of the booked product, or free text in case of the other pickup location option.<p>The
                value will be ignored, if the product does not allow pickups or if the location name does not match one of the
                product's pickup locations and 'other' pickup option is not enabled for the product pickup.</p>
            longitude (Union[Unset, float]): google maps calculated latitude of the pickup address
            minutes_prior (Union[Unset, int]): Pickup time in minutes, prior to the tour start time.
            pickup_instructions (Union[Unset, str]): <p>Present only in booking service response</p>Chosen pickup
                instructions (general and location specific). Shown when the pickup was chosen for the booked item.
            pickup_time (Union[Unset, str]): <p>Present only in booking service response</p>In a booking item object, it
                represents a calculated pickup time, in supplier's local timezone. Shown when the pickup was chosen for the
                booked item and pickup location contains duration.
    """

    additional_instructions: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    latitude: Union[Unset, float] = UNSET
    location_name: Union[Unset, str] = UNSET
    longitude: Union[Unset, float] = UNSET
    minutes_prior: Union[Unset, int] = UNSET
    pickup_instructions: Union[Unset, str] = UNSET
    pickup_time: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        additional_instructions = self.additional_instructions
        address = self.address
        latitude = self.latitude
        location_name = self.location_name
        longitude = self.longitude
        minutes_prior = self.minutes_prior
        pickup_instructions = self.pickup_instructions
        pickup_time = self.pickup_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if additional_instructions is not UNSET:
            field_dict["additionalInstructions"] = additional_instructions
        if address is not UNSET:
            field_dict["address"] = address
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if location_name is not UNSET:
            field_dict["locationName"] = location_name
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if minutes_prior is not UNSET:
            field_dict["minutesPrior"] = minutes_prior
        if pickup_instructions is not UNSET:
            field_dict["pickupInstructions"] = pickup_instructions
        if pickup_time is not UNSET:
            field_dict["pickupTime"] = pickup_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        additional_instructions = d.pop("additionalInstructions", UNSET)

        address = d.pop("address", UNSET)

        latitude = d.pop("latitude", UNSET)

        location_name = d.pop("locationName", UNSET)

        longitude = d.pop("longitude", UNSET)

        minutes_prior = d.pop("minutesPrior", UNSET)

        pickup_instructions = d.pop("pickupInstructions", UNSET)

        pickup_time = d.pop("pickupTime", UNSET)

        pickup_location = cls(
            additional_instructions=additional_instructions,
            address=address,
            latitude=latitude,
            location_name=location_name,
            longitude=longitude,
            minutes_prior=minutes_prior,
            pickup_instructions=pickup_instructions,
            pickup_time=pickup_time,
        )

        pickup_location.additional_properties = d
        return pickup_location

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
