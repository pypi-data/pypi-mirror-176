from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.net_rate import NetRate
from ..models.product_rate_commission_type import ProductRateCommissionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProductRate")


@attr.s(auto_attribs=True)
class ProductRate:
    """A ProductRate is used to map a product and its associated value commission

    Attributes:
        commission_type (Union[Unset, ProductRateCommissionType]): Commission type: PERCENTAGE, NET_RATE
        net_rates (Union[Unset, List[NetRate]]): List of Net rates with its associated price option label e.g. Adult
            $20, Child $10 etc. This is mandatory if Commission Type is NET_RATE
        percentage_commission (Union[Unset, float]): Percentage value of the commission. This should be mandatory if
            Commission Type is PERCENTAGE
        percentage_include_extras (Union[Unset, bool]): Includes extras, This is mandatory if Commission Type is
            PERCENTAGE. If true, the product's extras will be included in the agent commission, otherwise the commission
            will be calculated based on the product price only.
        product_code (Union[Unset, str]): Product's product code
    """

    commission_type: Union[Unset, ProductRateCommissionType] = UNSET
    net_rates: Union[Unset, List[NetRate]] = UNSET
    percentage_commission: Union[Unset, float] = UNSET
    percentage_include_extras: Union[Unset, bool] = UNSET
    product_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        commission_type: Union[Unset, str] = UNSET
        if not isinstance(self.commission_type, Unset):
            commission_type = self.commission_type.value

        net_rates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.net_rates, Unset):
            net_rates = []
            for net_rates_item_data in self.net_rates:
                net_rates_item = net_rates_item_data.to_dict()

                net_rates.append(net_rates_item)

        percentage_commission = self.percentage_commission
        percentage_include_extras = self.percentage_include_extras
        product_code = self.product_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if commission_type is not UNSET:
            field_dict["commissionType"] = commission_type
        if net_rates is not UNSET:
            field_dict["netRates"] = net_rates
        if percentage_commission is not UNSET:
            field_dict["percentageCommission"] = percentage_commission
        if percentage_include_extras is not UNSET:
            field_dict["percentageIncludeExtras"] = percentage_include_extras
        if product_code is not UNSET:
            field_dict["productCode"] = product_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _commission_type = d.pop("commissionType", UNSET)
        commission_type: Union[Unset, ProductRateCommissionType]
        if isinstance(_commission_type, Unset):
            commission_type = UNSET
        else:
            commission_type = ProductRateCommissionType(_commission_type)

        net_rates = []
        _net_rates = d.pop("netRates", UNSET)
        for net_rates_item_data in _net_rates or []:
            net_rates_item = NetRate.from_dict(net_rates_item_data)

            net_rates.append(net_rates_item)

        percentage_commission = d.pop("percentageCommission", UNSET)

        percentage_include_extras = d.pop("percentageIncludeExtras", UNSET)

        product_code = d.pop("productCode", UNSET)

        product_rate = cls(
            commission_type=commission_type,
            net_rates=net_rates,
            percentage_commission=percentage_commission,
            percentage_include_extras=percentage_include_extras,
            product_code=product_code,
        )

        product_rate.additional_properties = d
        return product_rate

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
