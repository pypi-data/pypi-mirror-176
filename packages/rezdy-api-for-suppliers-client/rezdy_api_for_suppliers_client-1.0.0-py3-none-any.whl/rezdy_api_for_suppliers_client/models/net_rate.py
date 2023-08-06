from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NetRate")


@attr.s(auto_attribs=True)
class NetRate:
    """A Product with its associated price options net rates

    Attributes:
        net_price (Union[Unset, float]): Value of the rate for the given price option label
        price_option_label (Union[Unset, str]): Label of the price option e.g. Adult, Child etc
    """

    net_price: Union[Unset, float] = UNSET
    price_option_label: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        net_price = self.net_price
        price_option_label = self.price_option_label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if net_price is not UNSET:
            field_dict["netPrice"] = net_price
        if price_option_label is not UNSET:
            field_dict["priceOptionLabel"] = price_option_label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        net_price = d.pop("netPrice", UNSET)

        price_option_label = d.pop("priceOptionLabel", UNSET)

        net_rate = cls(
            net_price=net_price,
            price_option_label=price_option_label,
        )

        net_rate.additional_properties = d
        return net_rate

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
