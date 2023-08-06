from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.price_option import PriceOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionUpdateRequest")


@attr.s(auto_attribs=True)
class SessionUpdateRequest:
    """Updates session request data.

    Attributes:
        all_day (Union[Unset, bool]): If true, this session lasts all day and no time should be shown to customers.
            Technically the session will be from midnight to midnight.
        price_options (Union[Unset, List[PriceOption]]): List of price options, which will override the product level
            price. Price options have to be a subset of the product price options, thus you can not create new price
            options, use product update service to do so.
        seats (Union[Unset, int]): Update the total number of seats for this session. The total seats does not change
            after a booking is made. The total number of seats can not be less than 0.
        seats_available (Union[Unset, int]): Update the current availability for this session. The session total number
            of seats after updating the seats available can not be less than 0.
    """

    all_day: Union[Unset, bool] = UNSET
    price_options: Union[Unset, List[PriceOption]] = UNSET
    seats: Union[Unset, int] = UNSET
    seats_available: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        all_day = self.all_day
        price_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.price_options, Unset):
            price_options = []
            for price_options_item_data in self.price_options:
                price_options_item = price_options_item_data.to_dict()

                price_options.append(price_options_item)

        seats = self.seats
        seats_available = self.seats_available

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if all_day is not UNSET:
            field_dict["allDay"] = all_day
        if price_options is not UNSET:
            field_dict["priceOptions"] = price_options
        if seats is not UNSET:
            field_dict["seats"] = seats
        if seats_available is not UNSET:
            field_dict["seatsAvailable"] = seats_available

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        all_day = d.pop("allDay", UNSET)

        price_options = []
        _price_options = d.pop("priceOptions", UNSET)
        for price_options_item_data in _price_options or []:
            price_options_item = PriceOption.from_dict(price_options_item_data)

            price_options.append(price_options_item)

        seats = d.pop("seats", UNSET)

        seats_available = d.pop("seatsAvailable", UNSET)

        session_update_request = cls(
            all_day=all_day,
            price_options=price_options,
            seats=seats,
            seats_available=seats_available,
        )

        session_update_request.additional_properties = d
        return session_update_request

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
