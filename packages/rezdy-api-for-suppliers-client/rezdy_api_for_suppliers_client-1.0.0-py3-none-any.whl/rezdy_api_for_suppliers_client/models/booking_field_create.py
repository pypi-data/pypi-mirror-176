from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.booking_field_create_field_type import BookingFieldCreateFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BookingFieldCreate")


@attr.s(auto_attribs=True)
class BookingFieldCreate:
    """An information about a booking or a participant.

    Attributes:
        field_type (Union[Unset, BookingFieldCreateFieldType]): Type of a custom booking field. This type does not apply
            on the Rezdy build-in booking fields. See the section <a
            href="/guides/API%20Related%20Articles/Create%20products">Product booking fields</a>
        label (Union[Unset, str]): Field label that can be shown to customers
        list_options (Union[Unset, str]): If this field only allows limited values to be selected from a list, they'll
            be included in this string, separated by \r\n
        required_per_booking (Union[Unset, bool]): true if this field must be populated once per booking, regardless of
            the number of items or participants. It should be in Booking.fields<p><i>Currently, required fields are not
            validated when a booking is created though public API, however it's a good practice to support them on in your
            client code <b>However, soon the required fields will be enforced for public API booking.</b>.</i></p>
        required_per_participant (Union[Unset, bool]): true if this field must be populated for each participant. It
            should be in Booking.BookingItem.Participant.fields.<p><i>Currently, required fields are not validated when a
            booking is created though public API, however it's a good practice to support them on in your client code.
            <b>However, soon the required fields will be enforced for public API booking.</b></i></p>
        visible_per_booking (Union[Unset, bool]): true if this field should be asked once per booking, regardless of the
            number of items or participants. It should be in Booking.fields
        visible_per_participant (Union[Unset, bool]): true if this field should be asked for each participant when doing
            a booking. It should be in Booking.BookingItem.Participant.fields.
    """

    field_type: Union[Unset, BookingFieldCreateFieldType] = UNSET
    label: Union[Unset, str] = UNSET
    list_options: Union[Unset, str] = UNSET
    required_per_booking: Union[Unset, bool] = UNSET
    required_per_participant: Union[Unset, bool] = UNSET
    visible_per_booking: Union[Unset, bool] = UNSET
    visible_per_participant: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_type: Union[Unset, str] = UNSET
        if not isinstance(self.field_type, Unset):
            field_type = self.field_type.value

        label = self.label
        list_options = self.list_options
        required_per_booking = self.required_per_booking
        required_per_participant = self.required_per_participant
        visible_per_booking = self.visible_per_booking
        visible_per_participant = self.visible_per_participant

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_type is not UNSET:
            field_dict["fieldType"] = field_type
        if label is not UNSET:
            field_dict["label"] = label
        if list_options is not UNSET:
            field_dict["listOptions"] = list_options
        if required_per_booking is not UNSET:
            field_dict["requiredPerBooking"] = required_per_booking
        if required_per_participant is not UNSET:
            field_dict["requiredPerParticipant"] = required_per_participant
        if visible_per_booking is not UNSET:
            field_dict["visiblePerBooking"] = visible_per_booking
        if visible_per_participant is not UNSET:
            field_dict["visiblePerParticipant"] = visible_per_participant

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _field_type = d.pop("fieldType", UNSET)
        field_type: Union[Unset, BookingFieldCreateFieldType]
        if isinstance(_field_type, Unset):
            field_type = UNSET
        else:
            field_type = BookingFieldCreateFieldType(_field_type)

        label = d.pop("label", UNSET)

        list_options = d.pop("listOptions", UNSET)

        required_per_booking = d.pop("requiredPerBooking", UNSET)

        required_per_participant = d.pop("requiredPerParticipant", UNSET)

        visible_per_booking = d.pop("visiblePerBooking", UNSET)

        visible_per_participant = d.pop("visiblePerParticipant", UNSET)

        booking_field_create = cls(
            field_type=field_type,
            label=label,
            list_options=list_options,
            required_per_booking=required_per_booking,
            required_per_participant=required_per_participant,
            visible_per_booking=visible_per_booking,
            visible_per_participant=visible_per_participant,
        )

        booking_field_create.additional_properties = d
        return booking_field_create

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
