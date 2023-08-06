import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.extra import Extra
from ..models.participant import Participant
from ..models.pickup_location import PickupLocation
from ..models.quantity import Quantity
from ..models.voucher import Voucher
from ..types import UNSET, Unset

T = TypeVar("T", bound="BookingItem")


@attr.s(auto_attribs=True)
class BookingItem:
    """A BookingItem is a unique product/startTime combination in a booking

    Attributes:
        amount (Union[Unset, float]): Amount charged for this BookingItem. This is automatically generated based on
            quantities, but you can override the amount by entering a value. If automated payment method is used for the
            booked product, the Amount of the booked item<br>has to be grater than Net Rate sum of the booked quantities and
            Rezdy processing fee.
        end_time (Union[Unset, datetime.datetime]): End time of the session for this BookingItem
        end_time_local (Union[Unset, str]): End time of the session for this BookingItem in supplier's local timezone.
        extras (Union[Unset, List[Extra]]): List of Extras booked with this product
        participants (Union[Unset, List[Participant]]): List of participants. Each participant object contains all the
            booking fields for a single participant.
        pickup_location (Union[Unset, PickupLocation]): PickupLocation object. Holds information about the a pickup
            location from the pickup list configured for the product.
        product_code (Union[Unset, str]): Unique Rezdy code of the product in this BookingItem
        product_name (Union[Unset, str]): Name of the product in this BookingItem
        quantities (Union[Unset, List[Quantity]]): List of quantities booked by this item. Each Quantity must be linked
            to a Product price option via its label or ID.If the product only has one price option, only 'Quantity.value' is
            required.
        start_time (Union[Unset, datetime.datetime]): Start time of the session for this BookingItem
        start_time_local (Union[Unset, str]): Start time of the session for this BookingItem in supplier's local
            timezone.
        subtotal (Union[Unset, float]): Subtotal is the BookingItem.amount plus extras costs plus taxes and fees
        total_item_tax (Union[Unset, float]): Total tax applied to this booking item.
        total_quantity (Union[Unset, int]): Total quantity booked by all the Quantity. For example if the booking is for
            2 Adults and 1 Child, totalQuantity will be 3.
        transfer_from (Union[Unset, str]): From location. Only used by Shuttle and Transfer products
        transfer_return (Union[Unset, bool]): Is this a one-way (false) or a return trip (true)? Only used by Shuttle
            and Transfer products
        transfer_to (Union[Unset, str]): To location. Only used by Shuttle and Transfer products
        vouchers (Union[Unset, List[Voucher]]): List of vouchers created by this booking item - when the product is
            bought as a gift or is a gift card
    """

    amount: Union[Unset, float] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    end_time_local: Union[Unset, str] = UNSET
    extras: Union[Unset, List[Extra]] = UNSET
    participants: Union[Unset, List[Participant]] = UNSET
    pickup_location: Union[Unset, PickupLocation] = UNSET
    product_code: Union[Unset, str] = UNSET
    product_name: Union[Unset, str] = UNSET
    quantities: Union[Unset, List[Quantity]] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    start_time_local: Union[Unset, str] = UNSET
    subtotal: Union[Unset, float] = UNSET
    total_item_tax: Union[Unset, float] = UNSET
    total_quantity: Union[Unset, int] = UNSET
    transfer_from: Union[Unset, str] = UNSET
    transfer_return: Union[Unset, bool] = UNSET
    transfer_to: Union[Unset, str] = UNSET
    vouchers: Union[Unset, List[Voucher]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        end_time_local = self.end_time_local
        extras: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.extras, Unset):
            extras = []
            for extras_item_data in self.extras:
                extras_item = extras_item_data.to_dict()

                extras.append(extras_item)

        participants: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.participants, Unset):
            participants = []
            for participants_item_data in self.participants:
                participants_item = participants_item_data.to_dict()

                participants.append(participants_item)

        pickup_location: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pickup_location, Unset):
            pickup_location = self.pickup_location.to_dict()

        product_code = self.product_code
        product_name = self.product_name
        quantities: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.quantities, Unset):
            quantities = []
            for quantities_item_data in self.quantities:
                quantities_item = quantities_item_data.to_dict()

                quantities.append(quantities_item)

        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        start_time_local = self.start_time_local
        subtotal = self.subtotal
        total_item_tax = self.total_item_tax
        total_quantity = self.total_quantity
        transfer_from = self.transfer_from
        transfer_return = self.transfer_return
        transfer_to = self.transfer_to
        vouchers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vouchers, Unset):
            vouchers = []
            for vouchers_item_data in self.vouchers:
                vouchers_item = vouchers_item_data.to_dict()

                vouchers.append(vouchers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if end_time_local is not UNSET:
            field_dict["endTimeLocal"] = end_time_local
        if extras is not UNSET:
            field_dict["extras"] = extras
        if participants is not UNSET:
            field_dict["participants"] = participants
        if pickup_location is not UNSET:
            field_dict["pickupLocation"] = pickup_location
        if product_code is not UNSET:
            field_dict["productCode"] = product_code
        if product_name is not UNSET:
            field_dict["productName"] = product_name
        if quantities is not UNSET:
            field_dict["quantities"] = quantities
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if start_time_local is not UNSET:
            field_dict["startTimeLocal"] = start_time_local
        if subtotal is not UNSET:
            field_dict["subtotal"] = subtotal
        if total_item_tax is not UNSET:
            field_dict["totalItemTax"] = total_item_tax
        if total_quantity is not UNSET:
            field_dict["totalQuantity"] = total_quantity
        if transfer_from is not UNSET:
            field_dict["transferFrom"] = transfer_from
        if transfer_return is not UNSET:
            field_dict["transferReturn"] = transfer_return
        if transfer_to is not UNSET:
            field_dict["transferTo"] = transfer_to
        if vouchers is not UNSET:
            field_dict["vouchers"] = vouchers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, datetime.datetime]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        end_time_local = d.pop("endTimeLocal", UNSET)

        extras = []
        _extras = d.pop("extras", UNSET)
        for extras_item_data in _extras or []:
            extras_item = Extra.from_dict(extras_item_data)

            extras.append(extras_item)

        participants = []
        _participants = d.pop("participants", UNSET)
        for participants_item_data in _participants or []:
            participants_item = Participant.from_dict(participants_item_data)

            participants.append(participants_item)

        _pickup_location = d.pop("pickupLocation", UNSET)
        pickup_location: Union[Unset, PickupLocation]
        if isinstance(_pickup_location, Unset):
            pickup_location = UNSET
        else:
            pickup_location = PickupLocation.from_dict(_pickup_location)

        product_code = d.pop("productCode", UNSET)

        product_name = d.pop("productName", UNSET)

        quantities = []
        _quantities = d.pop("quantities", UNSET)
        for quantities_item_data in _quantities or []:
            quantities_item = Quantity.from_dict(quantities_item_data)

            quantities.append(quantities_item)

        _start_time = d.pop("startTime", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        start_time_local = d.pop("startTimeLocal", UNSET)

        subtotal = d.pop("subtotal", UNSET)

        total_item_tax = d.pop("totalItemTax", UNSET)

        total_quantity = d.pop("totalQuantity", UNSET)

        transfer_from = d.pop("transferFrom", UNSET)

        transfer_return = d.pop("transferReturn", UNSET)

        transfer_to = d.pop("transferTo", UNSET)

        vouchers = []
        _vouchers = d.pop("vouchers", UNSET)
        for vouchers_item_data in _vouchers or []:
            vouchers_item = Voucher.from_dict(vouchers_item_data)

            vouchers.append(vouchers_item)

        booking_item = cls(
            amount=amount,
            end_time=end_time,
            end_time_local=end_time_local,
            extras=extras,
            participants=participants,
            pickup_location=pickup_location,
            product_code=product_code,
            product_name=product_name,
            quantities=quantities,
            start_time=start_time,
            start_time_local=start_time_local,
            subtotal=subtotal,
            total_item_tax=total_item_tax,
            total_quantity=total_quantity,
            transfer_from=transfer_from,
            transfer_return=transfer_return,
            transfer_to=transfer_to,
            vouchers=vouchers,
        )

        booking_item.additional_properties = d
        return booking_item

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
