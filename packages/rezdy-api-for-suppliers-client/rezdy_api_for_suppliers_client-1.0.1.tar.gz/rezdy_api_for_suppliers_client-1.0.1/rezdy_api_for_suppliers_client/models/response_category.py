from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.category import Category
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseCategory")


@attr.s(auto_attribs=True)
class ResponseCategory:
    """
    Attributes:
        request_status (RequestStatus):
        category (Union[Unset, Category]): A Category is used to group products
    """

    request_status: RequestStatus
    category: Union[Unset, Category] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        category: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _category = d.pop("category", UNSET)
        category: Union[Unset, Category]
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = Category.from_dict(_category)

        response_category = cls(
            request_status=request_status,
            category=category,
        )

        response_category.additional_properties = d
        return response_category

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
