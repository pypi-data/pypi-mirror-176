import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.price_option import PriceOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="Session")


@attr.s(auto_attribs=True)
class Session:
    """A Session holds availability for a unique product / start time combination and also the rates for the session
    booking.

        Attributes:
            all_day (Union[Unset, bool]): If true, this session lasts all day and no time should be shown to customers.
                Technically the session will be from midnight to midnight.
            end_time (Union[Unset, datetime.datetime]): End time of this session. Used to show the customer how long that
                tour will last
            end_time_local (Union[Unset, str]): End time of this session in supplier's local timezone. Used to show the
                customer how long that tour will last
            id (Union[Unset, int]): Rezdy internal ID for this session
            price_options (Union[Unset, List[PriceOption]]): List of price options attached to this session. Most of the
                time they'll match the product's price options, but they can be used to change the price of specific dates/times
                (I.e. high/low season, weekday/weekend, etc.)
            product_code (Union[Unset, str]): Rezdy unique productCode linked to this session
            seats (Union[Unset, int]): Total number of seats for this session. Does not change after a booking is made
            seats_available (Union[Unset, int]): Current availability for this session.
            start_time (Union[Unset, datetime.datetime]): Start Time of this session. This time should be used when showing
                customers the booking date/time. It should be sent in BookingItem.startTime when making new bookings
            start_time_local (Union[Unset, str]): Start Time of this session in supplier's local timezone. This time should
                be used when showing customers the booking date/time. It should be sent in BookingItem.startTimeLocal when
                making new bookings
    """

    all_day: Union[Unset, bool] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    end_time_local: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    price_options: Union[Unset, List[PriceOption]] = UNSET
    product_code: Union[Unset, str] = UNSET
    seats: Union[Unset, int] = UNSET
    seats_available: Union[Unset, int] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    start_time_local: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        all_day = self.all_day
        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        end_time_local = self.end_time_local
        id = self.id
        price_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.price_options, Unset):
            price_options = []
            for price_options_item_data in self.price_options:
                price_options_item = price_options_item_data.to_dict()

                price_options.append(price_options_item)

        product_code = self.product_code
        seats = self.seats
        seats_available = self.seats_available
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        start_time_local = self.start_time_local

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if all_day is not UNSET:
            field_dict["allDay"] = all_day
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if end_time_local is not UNSET:
            field_dict["endTimeLocal"] = end_time_local
        if id is not UNSET:
            field_dict["id"] = id
        if price_options is not UNSET:
            field_dict["priceOptions"] = price_options
        if product_code is not UNSET:
            field_dict["productCode"] = product_code
        if seats is not UNSET:
            field_dict["seats"] = seats
        if seats_available is not UNSET:
            field_dict["seatsAvailable"] = seats_available
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if start_time_local is not UNSET:
            field_dict["startTimeLocal"] = start_time_local

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        all_day = d.pop("allDay", UNSET)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, datetime.datetime]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        end_time_local = d.pop("endTimeLocal", UNSET)

        id = d.pop("id", UNSET)

        price_options = []
        _price_options = d.pop("priceOptions", UNSET)
        for price_options_item_data in _price_options or []:
            price_options_item = PriceOption.from_dict(price_options_item_data)

            price_options.append(price_options_item)

        product_code = d.pop("productCode", UNSET)

        seats = d.pop("seats", UNSET)

        seats_available = d.pop("seatsAvailable", UNSET)

        _start_time = d.pop("startTime", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        start_time_local = d.pop("startTimeLocal", UNSET)

        session = cls(
            all_day=all_day,
            end_time=end_time,
            end_time_local=end_time_local,
            id=id,
            price_options=price_options,
            product_code=product_code,
            seats=seats,
            seats_available=seats_available,
            start_time=start_time,
            start_time_local=start_time_local,
        )

        session.additional_properties = d
        return session

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
