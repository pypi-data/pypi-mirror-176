import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.price_option import PriceOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionUpdateBatchRequest")


@attr.s(auto_attribs=True)
class SessionUpdateBatchRequest:
    """Batch update session request data.

    Attributes:
        rezdy_unique_product_code_linked_to_this_session (str):
        all_day (Union[Unset, bool]): If true, this session lasts all day and no time should be shown to customers.
            Technically the session will be from midnight to midnight.
        end_time (Union[Unset, datetime.datetime]): Batch update end interval
        end_time_local (Union[Unset, str]): Batch update end interval in supplier's local timezone.
        price_options (Union[Unset, List[PriceOption]]): List of price options, which will override the product level
            price. Price options have to be a subset of the product price options, thus you can not create new price
            options, use product update service to do so.
        seats (Union[Unset, int]): Update the total number of seats for this session. The total seats does not change
            after a booking is made. The total number of seats can not be less than 0.
        seats_available (Union[Unset, int]): Update the current availability for this session. The session total number
            of seats after updating the seats available can not be less than 0.
        start_time (Union[Unset, datetime.datetime]): Batch update start interval
        start_time_local (Union[Unset, str]): Batch update start interval in supplier's local timezone.
    """

    rezdy_unique_product_code_linked_to_this_session: str
    all_day: Union[Unset, bool] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    end_time_local: Union[Unset, str] = UNSET
    price_options: Union[Unset, List[PriceOption]] = UNSET
    seats: Union[Unset, int] = UNSET
    seats_available: Union[Unset, int] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    start_time_local: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rezdy_unique_product_code_linked_to_this_session = self.rezdy_unique_product_code_linked_to_this_session
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

        seats = self.seats
        seats_available = self.seats_available
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        start_time_local = self.start_time_local

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Rezdy unique productCode linked to this session": rezdy_unique_product_code_linked_to_this_session,
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
        rezdy_unique_product_code_linked_to_this_session = d.pop("Rezdy unique productCode linked to this session")

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

        seats = d.pop("seats", UNSET)

        seats_available = d.pop("seatsAvailable", UNSET)

        _start_time = d.pop("startTime", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        start_time_local = d.pop("startTimeLocal", UNSET)

        session_update_batch_request = cls(
            rezdy_unique_product_code_linked_to_this_session=rezdy_unique_product_code_linked_to_this_session,
            all_day=all_day,
            end_time=end_time,
            end_time_local=end_time_local,
            price_options=price_options,
            seats=seats,
            seats_available=seats_available,
            start_time=start_time,
            start_time_local=start_time_local,
        )

        session_update_batch_request.additional_properties = d
        return session_update_batch_request

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
