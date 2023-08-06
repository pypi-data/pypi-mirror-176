from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Quantity")


@attr.s(auto_attribs=True)
class Quantity:
    """Quantity of a single price option attached to a BookingItem.<ul><li>If the product only has 1 price option, only
    "Quantity.value" is required.</li><li>If the product has multiple price options, "Quantity.optionLabel" is also
    required.</li><li>It is recommended to use "Quantity.optionLabel" and optionally "Quantity.optionPrice" instead of
    "Quantity.optionId" because the latter can vary depending on the session booked.</li></ul>I.e. enter optionLabel =
    "Adult", optionPrice = 100 and value = "2" to book for 2 x Adults ticket for 100

        Attributes:
            value (int): Quantity actually booked
            option_id (Union[Unset, int]): Price option ID
            option_label (Union[Unset, str]): Price option label
            option_price (Union[Unset, float]): Price option price for a single quantity
    """

    value: int
    option_id: Union[Unset, int] = UNSET
    option_label: Union[Unset, str] = UNSET
    option_price: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        option_id = self.option_id
        option_label = self.option_label
        option_price = self.option_price

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if option_id is not UNSET:
            field_dict["optionId"] = option_id
        if option_label is not UNSET:
            field_dict["optionLabel"] = option_label
        if option_price is not UNSET:
            field_dict["optionPrice"] = option_price

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        option_id = d.pop("optionId", UNSET)

        option_label = d.pop("optionLabel", UNSET)

        option_price = d.pop("optionPrice", UNSET)

        quantity = cls(
            value=value,
            option_id=option_id,
            option_label=option_label,
            option_price=option_price,
        )

        quantity.additional_properties = d
        return quantity

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
