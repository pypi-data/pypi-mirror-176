from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.booking import Booking
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseBookingList")


@attr.s(auto_attribs=True)
class ResponseBookingList:
    """
    Attributes:
        request_status (RequestStatus):
        bookings (Union[Unset, List[Booking]]):
    """

    request_status: RequestStatus
    bookings: Union[Unset, List[Booking]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        bookings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.bookings, Unset):
            bookings = []
            for bookings_item_data in self.bookings:
                bookings_item = bookings_item_data.to_dict()

                bookings.append(bookings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if bookings is not UNSET:
            field_dict["bookings"] = bookings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        bookings = []
        _bookings = d.pop("bookings", UNSET)
        for bookings_item_data in _bookings or []:
            bookings_item = Booking.from_dict(bookings_item_data)

            bookings.append(bookings_item)

        response_booking_list = cls(
            request_status=request_status,
            bookings=bookings,
        )

        response_booking_list.additional_properties = d
        return response_booking_list

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
