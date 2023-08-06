import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.booking_payment_currency import BookingPaymentCurrency
from ..models.booking_payment_recipient import BookingPaymentRecipient
from ..models.booking_payment_type import BookingPaymentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BookingPayment")


@attr.s(auto_attribs=True)
class BookingPayment:
    """Record of an already processed payment.

    Attributes:
        amount (Union[Unset, float]): Payment amount
        currency (Union[Unset, BookingPaymentCurrency]): Currency for this payment<br>Payments must be in the same
            currency than the order's totalCurrency.
        date (Union[Unset, datetime.datetime]): Date this payment was processed
        label (Union[Unset, str]): Reference or transaction code
        recipient (Union[Unset, BookingPaymentRecipient]): Payment recipient.
        type (Union[Unset, BookingPaymentType]): Type of payment
    """

    amount: Union[Unset, float] = UNSET
    currency: Union[Unset, BookingPaymentCurrency] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET
    label: Union[Unset, str] = UNSET
    recipient: Union[Unset, BookingPaymentRecipient] = UNSET
    type: Union[Unset, BookingPaymentType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        currency: Union[Unset, str] = UNSET
        if not isinstance(self.currency, Unset):
            currency = self.currency.value

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        label = self.label
        recipient: Union[Unset, str] = UNSET
        if not isinstance(self.recipient, Unset):
            recipient = self.recipient.value

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if currency is not UNSET:
            field_dict["currency"] = currency
        if date is not UNSET:
            field_dict["date"] = date
        if label is not UNSET:
            field_dict["label"] = label
        if recipient is not UNSET:
            field_dict["recipient"] = recipient
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        _currency = d.pop("currency", UNSET)
        currency: Union[Unset, BookingPaymentCurrency]
        if isinstance(_currency, Unset):
            currency = UNSET
        else:
            currency = BookingPaymentCurrency(_currency)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        label = d.pop("label", UNSET)

        _recipient = d.pop("recipient", UNSET)
        recipient: Union[Unset, BookingPaymentRecipient]
        if isinstance(_recipient, Unset):
            recipient = UNSET
        else:
            recipient = BookingPaymentRecipient(_recipient)

        _type = d.pop("type", UNSET)
        type: Union[Unset, BookingPaymentType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = BookingPaymentType(_type)

        booking_payment = cls(
            amount=amount,
            currency=currency,
            date=date,
            label=label,
            recipient=recipient,
            type=type,
        )

        booking_payment.additional_properties = d
        return booking_payment

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
