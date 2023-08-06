from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extra_extra_price_type import ExtraExtraPriceType
from ..models.image import Image
from ..types import UNSET, Unset

T = TypeVar("T", bound="Extra")


@attr.s(auto_attribs=True)
class Extra:
    """Optional service or item that can be purchased when booking a specific product

    Attributes:
        description (Union[Unset, str]): Description of the extra
        extra_price_type (Union[Unset, ExtraExtraPriceType]): Price type for this extra. Defines what quantities are
            allowed and how their price is calculated
        id (Union[Unset, int]): ID of the extra
        image (Union[Unset, Image]): Image links.
        name (Union[Unset, str]): Name of the extra
        price (Union[Unset, float]): Price for a single quantity of this extra
        quantity (Union[Unset, int]): Quantity booked
    """

    description: Union[Unset, str] = UNSET
    extra_price_type: Union[Unset, ExtraExtraPriceType] = UNSET
    id: Union[Unset, int] = UNSET
    image: Union[Unset, Image] = UNSET
    name: Union[Unset, str] = UNSET
    price: Union[Unset, float] = UNSET
    quantity: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        extra_price_type: Union[Unset, str] = UNSET
        if not isinstance(self.extra_price_type, Unset):
            extra_price_type = self.extra_price_type.value

        id = self.id
        image: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        name = self.name
        price = self.price
        quantity = self.quantity

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if extra_price_type is not UNSET:
            field_dict["extraPriceType"] = extra_price_type
        if id is not UNSET:
            field_dict["id"] = id
        if image is not UNSET:
            field_dict["image"] = image
        if name is not UNSET:
            field_dict["name"] = name
        if price is not UNSET:
            field_dict["price"] = price
        if quantity is not UNSET:
            field_dict["quantity"] = quantity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        _extra_price_type = d.pop("extraPriceType", UNSET)
        extra_price_type: Union[Unset, ExtraExtraPriceType]
        if isinstance(_extra_price_type, Unset):
            extra_price_type = UNSET
        else:
            extra_price_type = ExtraExtraPriceType(_extra_price_type)

        id = d.pop("id", UNSET)

        _image = d.pop("image", UNSET)
        image: Union[Unset, Image]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = Image.from_dict(_image)

        name = d.pop("name", UNSET)

        price = d.pop("price", UNSET)

        quantity = d.pop("quantity", UNSET)

        extra = cls(
            description=description,
            extra_price_type=extra_price_type,
            id=id,
            image=image,
            name=name,
            price=price,
            quantity=quantity,
        )

        extra.additional_properties = d
        return extra

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
