import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.price_option import PriceOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionCreateRequest")


@attr.s(auto_attribs=True)
class SessionCreateRequest:
    """Create session request data.

    Attributes:
        product_code (str): Rezdy unique productCode linked to this session
        seats (int): Total number of seats for this session. Does not change after a booking is made
        all_day (Union[Unset, bool]): If true, this session lasts all day and no time should be shown to customers.
            Technically the session will be from midnight to midnight.
        end_time (Union[Unset, datetime.datetime]): End time of this session. Used to show the customer how long that
            tour will last
        end_time_local (Union[Unset, str]): End time of this session in supplier's local timezone. Used to show the
            customer how long that tour will last
        price_options (Union[Unset, List[PriceOption]]): List of price options attached to this session. Most of the
            time they'll match the product's price options, but they can be used to change the price of specific dates/times
            (I.e. high/low season, weekday/weekend, etc.)
        start_time (Union[Unset, datetime.datetime]): Start Time of this session. This time should be used when showing
            customers the booking date/time. It should be sent in BookingItem.startTime when making new bookings
        start_time_local (Union[Unset, str]): Start Time of this session in supplier's local timezone. This time should
            be used when showing customers the booking date/time. It should be sent in BookingItem.startTimeLocal when
            making new bookings
    """

    product_code: str
    seats: int
    all_day: Union[Unset, bool] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    end_time_local: Union[Unset, str] = UNSET
    price_options: Union[Unset, List[PriceOption]] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    start_time_local: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        product_code = self.product_code
        seats = self.seats
        all_day = self.all_day
        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        end_time_local = self.end_time_local
        price_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.price_options, Unset):
            price_options = []
            for price_options_item_data in self.price_options:
                price_options_item = price_options_item_data.to_dict()

                price_options.append(price_options_item)

        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        start_time_local = self.start_time_local

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "productCode": product_code,
                "seats": seats,
            }
        )
        if all_day is not UNSET:
            field_dict["allDay"] = all_day
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if end_time_local is not UNSET:
            field_dict["endTimeLocal"] = end_time_local
        if price_options is not UNSET:
            field_dict["priceOptions"] = price_options
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if start_time_local is not UNSET:
            field_dict["startTimeLocal"] = start_time_local

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        product_code = d.pop("productCode")

        seats = d.pop("seats")

        all_day = d.pop("allDay", UNSET)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, datetime.datetime]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        end_time_local = d.pop("endTimeLocal", UNSET)

        price_options = []
        _price_options = d.pop("priceOptions", UNSET)
        for price_options_item_data in _price_options or []:
            price_options_item = PriceOption.from_dict(price_options_item_data)

            price_options.append(price_options_item)

        _start_time = d.pop("startTime", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        start_time_local = d.pop("startTimeLocal", UNSET)

        session_create_request = cls(
            product_code=product_code,
            seats=seats,
            all_day=all_day,
            end_time=end_time,
            end_time_local=end_time_local,
            price_options=price_options,
            start_time=start_time,
            start_time_local=start_time_local,
        )

        session_create_request.additional_properties = d
        return session_create_request

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
