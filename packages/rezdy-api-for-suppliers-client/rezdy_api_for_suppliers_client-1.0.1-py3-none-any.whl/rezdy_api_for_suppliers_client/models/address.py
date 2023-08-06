from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Address")


@attr.s(auto_attribs=True)
class Address:
    """Address of a company, customer or product location.

    Attributes:
        address_line (Union[Unset, str]): Address line
        address_line_2 (Union[Unset, str]): Address line 2
        city (Union[Unset, str]): City name
        country_code (Union[Unset, str]): Country code
        latitude (Union[Unset, float]): Geolocation - latitude
        longitude (Union[Unset, float]): Geolocation - longitude
        post_code (Union[Unset, str]): Post Code
        state (Union[Unset, str]): State name
    """

    address_line: Union[Unset, str] = UNSET
    address_line_2: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    country_code: Union[Unset, str] = UNSET
    latitude: Union[Unset, float] = UNSET
    longitude: Union[Unset, float] = UNSET
    post_code: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address_line = self.address_line
        address_line_2 = self.address_line_2
        city = self.city
        country_code = self.country_code
        latitude = self.latitude
        longitude = self.longitude
        post_code = self.post_code
        state = self.state

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if address_line is not UNSET:
            field_dict["addressLine"] = address_line
        if address_line_2 is not UNSET:
            field_dict["addressLine2"] = address_line_2
        if city is not UNSET:
            field_dict["city"] = city
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if post_code is not UNSET:
            field_dict["postCode"] = post_code
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address_line = d.pop("addressLine", UNSET)

        address_line_2 = d.pop("addressLine2", UNSET)

        city = d.pop("city", UNSET)

        country_code = d.pop("countryCode", UNSET)

        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        post_code = d.pop("postCode", UNSET)

        state = d.pop("state", UNSET)

        address = cls(
            address_line=address_line,
            address_line_2=address_line_2,
            city=city,
            country_code=country_code,
            latitude=latitude,
            longitude=longitude,
            post_code=post_code,
            state=state,
        )

        address.additional_properties = d
        return address

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
