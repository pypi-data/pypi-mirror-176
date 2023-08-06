from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.tax_tax_fee_type import TaxTaxFeeType
from ..models.tax_tax_type import TaxTaxType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Tax")


@attr.s(auto_attribs=True)
class Tax:
    """Tax object. Holds information such as the tax amount applied to an order

    Attributes:
        compound (Union[Unset, bool]): Whether a stacked tax with the specified percent is applied. <br> e.g. A $100
            item with an exclusive tax of %10 will result in the price being $110. If compound is true, then an addition %10
            of $110 will be added as tax.
        label (Union[Unset, str]): Name/description of the tax
        price_inclusive (Union[Unset, bool]): Whether the tax is included in the price or not. This field will be
            displayed if the taxType is PERCENT <br>E.g. A $100 item with price INCLUSIVE tax of 10% will result in a $10
            tax as part of the $100. A $100 item with price EXCLUSIVE tax of 10% will result in a $10 tax on top of the
            $100.
        supplier_id (Union[Unset, int]): Rezdy internal ID of the company applying this tax
        tax_amount (Union[Unset, float]): The tax amount. This field will only contain a value if the taxType is one of
            the following: FIXED_PER_QUANTITY, FIXED_PER_ORDER, FIXED_PER_DURATION
        tax_fee_type (Union[Unset, TaxTaxFeeType]): Indicate Fee or Tax
        tax_percent (Union[Unset, float]): Percentage value of the fee/tax. This field will only contain a value if the
            taxType is PERCENT
        tax_type (Union[Unset, TaxTaxType]): <b>PERCENT: </b>The tax will be a percentage of the order
            total.<br><b>FIXED_PER_QUANTITY: </b>The tax will be a fixed amount e.g. $10 per
            quantity.<br><b>FIXED_PER_ORDER: </b>The tax will be a fixed amount e.g. $10 per booking
            item.<br><b>FIXED_PER_DURATION: </b>The tax will be a fixed amount e.g. $10 per duration unit.<br>
    """

    compound: Union[Unset, bool] = UNSET
    label: Union[Unset, str] = UNSET
    price_inclusive: Union[Unset, bool] = UNSET
    supplier_id: Union[Unset, int] = UNSET
    tax_amount: Union[Unset, float] = UNSET
    tax_fee_type: Union[Unset, TaxTaxFeeType] = UNSET
    tax_percent: Union[Unset, float] = UNSET
    tax_type: Union[Unset, TaxTaxType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        compound = self.compound
        label = self.label
        price_inclusive = self.price_inclusive
        supplier_id = self.supplier_id
        tax_amount = self.tax_amount
        tax_fee_type: Union[Unset, str] = UNSET
        if not isinstance(self.tax_fee_type, Unset):
            tax_fee_type = self.tax_fee_type.value

        tax_percent = self.tax_percent
        tax_type: Union[Unset, str] = UNSET
        if not isinstance(self.tax_type, Unset):
            tax_type = self.tax_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if compound is not UNSET:
            field_dict["compound"] = compound
        if label is not UNSET:
            field_dict["label"] = label
        if price_inclusive is not UNSET:
            field_dict["priceInclusive"] = price_inclusive
        if supplier_id is not UNSET:
            field_dict["supplierId"] = supplier_id
        if tax_amount is not UNSET:
            field_dict["taxAmount"] = tax_amount
        if tax_fee_type is not UNSET:
            field_dict["taxFeeType"] = tax_fee_type
        if tax_percent is not UNSET:
            field_dict["taxPercent"] = tax_percent
        if tax_type is not UNSET:
            field_dict["taxType"] = tax_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        compound = d.pop("compound", UNSET)

        label = d.pop("label", UNSET)

        price_inclusive = d.pop("priceInclusive", UNSET)

        supplier_id = d.pop("supplierId", UNSET)

        tax_amount = d.pop("taxAmount", UNSET)

        _tax_fee_type = d.pop("taxFeeType", UNSET)
        tax_fee_type: Union[Unset, TaxTaxFeeType]
        if isinstance(_tax_fee_type, Unset):
            tax_fee_type = UNSET
        else:
            tax_fee_type = TaxTaxFeeType(_tax_fee_type)

        tax_percent = d.pop("taxPercent", UNSET)

        _tax_type = d.pop("taxType", UNSET)
        tax_type: Union[Unset, TaxTaxType]
        if isinstance(_tax_type, Unset):
            tax_type = UNSET
        else:
            tax_type = TaxTaxType(_tax_type)

        tax = cls(
            compound=compound,
            label=label,
            price_inclusive=price_inclusive,
            supplier_id=supplier_id,
            tax_amount=tax_amount,
            tax_fee_type=tax_fee_type,
            tax_percent=tax_percent,
            tax_type=tax_type,
        )

        tax.additional_properties = d
        return tax

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
