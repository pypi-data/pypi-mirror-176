from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.product_rate import ProductRate
from ..types import UNSET, Unset

T = TypeVar("T", bound="Rate")


@attr.s(auto_attribs=True)
class Rate:
    """A Rate is used to group products with its corresponding shared rate

    Attributes:
        name (Union[Unset, str]): Rate name
        product_rates (Union[Unset, List[ProductRate]]): Products associated with this Rate (Catalog)
        rate_id (Union[Unset, int]): Rate ID
    """

    name: Union[Unset, str] = UNSET
    product_rates: Union[Unset, List[ProductRate]] = UNSET
    rate_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        product_rates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.product_rates, Unset):
            product_rates = []
            for product_rates_item_data in self.product_rates:
                product_rates_item = product_rates_item_data.to_dict()

                product_rates.append(product_rates_item)

        rate_id = self.rate_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if product_rates is not UNSET:
            field_dict["productRates"] = product_rates
        if rate_id is not UNSET:
            field_dict["rateId"] = rate_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        product_rates = []
        _product_rates = d.pop("productRates", UNSET)
        for product_rates_item_data in _product_rates or []:
            product_rates_item = ProductRate.from_dict(product_rates_item_data)

            product_rates.append(product_rates_item)

        rate_id = d.pop("rateId", UNSET)

        rate = cls(
            name=name,
            product_rates=product_rates,
            rate_id=rate_id,
        )

        rate.additional_properties = d
        return rate

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
