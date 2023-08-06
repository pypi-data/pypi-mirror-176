from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.product import Product
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseProduct")


@attr.s(auto_attribs=True)
class ResponseProduct:
    """
    Attributes:
        request_status (RequestStatus):
        product (Union[Unset, Product]): Product object. Holds general details and settings of a specific tour, activity
            or event.
    """

    request_status: RequestStatus
    product: Union[Unset, Product] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        product: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.product, Unset):
            product = self.product.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if product is not UNSET:
            field_dict["product"] = product

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _product = d.pop("product", UNSET)
        product: Union[Unset, Product]
        if isinstance(_product, Unset):
            product = UNSET
        else:
            product = Product.from_dict(_product)

        response_product = cls(
            request_status=request_status,
            product=product,
        )

        response_product.additional_properties = d
        return response_product

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
