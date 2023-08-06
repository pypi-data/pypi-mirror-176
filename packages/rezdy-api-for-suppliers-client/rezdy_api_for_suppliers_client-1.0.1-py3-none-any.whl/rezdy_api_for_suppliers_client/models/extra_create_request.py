from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extra_create_request_extra_price_type import ExtraCreateRequestExtraPriceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtraCreateRequest")


@attr.s(auto_attribs=True)
class ExtraCreateRequest:
    """Partial optional service or item that can be purchased when booking a specific product

    Attributes:
        description (Union[Unset, str]): Description of the extra
        extra_price_type (Union[Unset, ExtraCreateRequestExtraPriceType]): Price type for this extra. Defines what
            quantities are allowed and how their price is calculated
        name (Union[Unset, str]): Name of the extra
        price (Union[Unset, float]): Price for a single quantity of this extra
    """

    description: Union[Unset, str] = UNSET
    extra_price_type: Union[Unset, ExtraCreateRequestExtraPriceType] = UNSET
    name: Union[Unset, str] = UNSET
    price: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        extra_price_type: Union[Unset, str] = UNSET
        if not isinstance(self.extra_price_type, Unset):
            extra_price_type = self.extra_price_type.value

        name = self.name
        price = self.price

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if extra_price_type is not UNSET:
            field_dict["extraPriceType"] = extra_price_type
        if name is not UNSET:
            field_dict["name"] = name
        if price is not UNSET:
            field_dict["price"] = price

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        _extra_price_type = d.pop("extraPriceType", UNSET)
        extra_price_type: Union[Unset, ExtraCreateRequestExtraPriceType]
        if isinstance(_extra_price_type, Unset):
            extra_price_type = UNSET
        else:
            extra_price_type = ExtraCreateRequestExtraPriceType(_extra_price_type)

        name = d.pop("name", UNSET)

        price = d.pop("price", UNSET)

        extra_create_request = cls(
            description=description,
            extra_price_type=extra_price_type,
            name=name,
            price=price,
        )

        extra_create_request.additional_properties = d
        return extra_create_request

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
