from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.price_option_price_group_type import PriceOptionPriceGroupType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PriceOption")


@attr.s(auto_attribs=True)
class PriceOption:
    """A Price Option belongs to a product or products session. It holds the price details for a specific price
    type.Products can have one or many price options (I.e. Adult, Child, Family, etc.)

        Attributes:
            id (Union[Unset, int]):
            label (Union[Unset, str]): Label for this price (I.e. "Adult", "Child")
            max_quantity (Union[Unset, int]): Max booking quantity for the product price option. Can be specified, if the
                price option is fixed or a grouptype. For a successful booking of the product, the number of participants for
                this price option have to be lesser or equal than this value.
            min_quantity (Union[Unset, int]): Min booking quantity for the product price option. Can be specified, if the
                price option is fixed or a group type. For a successful booking of the product, the number of participants for
                this price option have to be greater or equal than this value.
            price (Union[Unset, float]): Price amount (I.e. "200.00")
            price_group_type (Union[Unset, PriceOptionPriceGroupType]): If this price is for a group, is the price for the
                whole group (TOTAL) or per quantity (EACH)
            product_code (Union[Unset, str]): Product code to which the price options belongs to. Since Rezdy introduced
                shared availability option for products, the product sessions can contain price overrides for all of the
                products, which share the sessions. Therefore it is necessary to filer only the price options matching the
                chosen product code on the client side, when processing /availability service responses.
            seats_used (Union[Unset, int]): How many seats one quantity of this price willuse. Used for availability
                calculations. For example 1 quantity of "Family of 4" will use 4 seats.
    """

    id: Union[Unset, int] = UNSET
    label: Union[Unset, str] = UNSET
    max_quantity: Union[Unset, int] = UNSET
    min_quantity: Union[Unset, int] = UNSET
    price: Union[Unset, float] = UNSET
    price_group_type: Union[Unset, PriceOptionPriceGroupType] = UNSET
    product_code: Union[Unset, str] = UNSET
    seats_used: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        label = self.label
        max_quantity = self.max_quantity
        min_quantity = self.min_quantity
        price = self.price
        price_group_type: Union[Unset, str] = UNSET
        if not isinstance(self.price_group_type, Unset):
            price_group_type = self.price_group_type.value

        product_code = self.product_code
        seats_used = self.seats_used

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if label is not UNSET:
            field_dict["label"] = label
        if max_quantity is not UNSET:
            field_dict["maxQuantity"] = max_quantity
        if min_quantity is not UNSET:
            field_dict["minQuantity"] = min_quantity
        if price is not UNSET:
            field_dict["price"] = price
        if price_group_type is not UNSET:
            field_dict["priceGroupType"] = price_group_type
        if product_code is not UNSET:
            field_dict["productCode"] = product_code
        if seats_used is not UNSET:
            field_dict["seatsUsed"] = seats_used

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        label = d.pop("label", UNSET)

        max_quantity = d.pop("maxQuantity", UNSET)

        min_quantity = d.pop("minQuantity", UNSET)

        price = d.pop("price", UNSET)

        _price_group_type = d.pop("priceGroupType", UNSET)
        price_group_type: Union[Unset, PriceOptionPriceGroupType]
        if isinstance(_price_group_type, Unset):
            price_group_type = UNSET
        else:
            price_group_type = PriceOptionPriceGroupType(_price_group_type)

        product_code = d.pop("productCode", UNSET)

        seats_used = d.pop("seatsUsed", UNSET)

        price_option = cls(
            id=id,
            label=label,
            max_quantity=max_quantity,
            min_quantity=min_quantity,
            price=price,
            price_group_type=price_group_type,
            product_code=product_code,
            seats_used=seats_used,
        )

        price_option.additional_properties = d
        return price_option

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
