from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.booking import Booking
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseBooking")


@attr.s(auto_attribs=True)
class ResponseBooking:
    """
    Attributes:
        request_status (RequestStatus):
        booking (Union[Unset, Booking]): Booking object. Lists all the possible fields for all product types and
            scenarios. Most of them are not required when sending a new booking.<br>A single Booking can be used to book
            multiple products, each of them being a BookingItem. All the products of one booking have to be from the same
            supplier.
    """

    request_status: RequestStatus
    booking: Union[Unset, Booking] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        booking: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.booking, Unset):
            booking = self.booking.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if booking is not UNSET:
            field_dict["booking"] = booking

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _booking = d.pop("booking", UNSET)
        booking: Union[Unset, Booking]
        if isinstance(_booking, Unset):
            booking = UNSET
        else:
            booking = Booking.from_dict(_booking)

        response_booking = cls(
            request_status=request_status,
            booking=booking,
        )

        response_booking.additional_properties = d
        return response_booking

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
