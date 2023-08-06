from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.booking_field import BookingField
from ..types import UNSET, Unset

T = TypeVar("T", bound="Participant")


@attr.s(auto_attribs=True)
class Participant:
    """Details about a single participant for a single BookingItem.<br>The participant is a person attending a tour. It
    differs from the Customer, who is the person making the booking and most of the time paying for it.

        Attributes:
            fields (Union[Unset, List[BookingField]]): List of BookingField for this participant
    """

    fields: Union[Unset, List[BookingField]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        fields: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()

                fields.append(fields_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = []
        _fields = d.pop("fields", UNSET)
        for fields_item_data in _fields or []:
            fields_item = BookingField.from_dict(fields_item_data)

            fields.append(fields_item)

        participant = cls(
            fields=fields,
        )

        participant.additional_properties = d
        return participant

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
