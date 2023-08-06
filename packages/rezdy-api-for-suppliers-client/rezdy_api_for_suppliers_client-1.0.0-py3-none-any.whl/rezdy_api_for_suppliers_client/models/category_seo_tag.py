from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.category_seo_tag_meta_type import CategorySeoTagMetaType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CategorySeoTag")


@attr.s(auto_attribs=True)
class CategorySeoTag:
    """Category Seo tags.

    Attributes:
        attr_key (Union[Unset, str]): Value to put in the "key" attribute (depending on type it could be name, property
            or rel)
        attr_value (Union[Unset, str]): Value to put in the "value" attribute (depending on type it could be content or
            href)
        category_id (Union[Unset, int]): Category ID this seo tag belongs to
        id (Union[Unset, int]): ID of Tag
        meta_type (Union[Unset, CategorySeoTagMetaType]): Type of Tag
    """

    attr_key: Union[Unset, str] = UNSET
    attr_value: Union[Unset, str] = UNSET
    category_id: Union[Unset, int] = UNSET
    id: Union[Unset, int] = UNSET
    meta_type: Union[Unset, CategorySeoTagMetaType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        attr_key = self.attr_key
        attr_value = self.attr_value
        category_id = self.category_id
        id = self.id
        meta_type: Union[Unset, str] = UNSET
        if not isinstance(self.meta_type, Unset):
            meta_type = self.meta_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attr_key is not UNSET:
            field_dict["attrKey"] = attr_key
        if attr_value is not UNSET:
            field_dict["attrValue"] = attr_value
        if category_id is not UNSET:
            field_dict["categoryId"] = category_id
        if id is not UNSET:
            field_dict["id"] = id
        if meta_type is not UNSET:
            field_dict["metaType"] = meta_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        attr_key = d.pop("attrKey", UNSET)

        attr_value = d.pop("attrValue", UNSET)

        category_id = d.pop("categoryId", UNSET)

        id = d.pop("id", UNSET)

        _meta_type = d.pop("metaType", UNSET)
        meta_type: Union[Unset, CategorySeoTagMetaType]
        if isinstance(_meta_type, Unset):
            meta_type = UNSET
        else:
            meta_type = CategorySeoTagMetaType(_meta_type)

        category_seo_tag = cls(
            attr_key=attr_key,
            attr_value=attr_value,
            category_id=category_id,
            id=id,
            meta_type=meta_type,
        )

        category_seo_tag.additional_properties = d
        return category_seo_tag

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
