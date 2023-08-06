from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.category_seo_tag import CategorySeoTag
from ..models.image import Image
from ..types import UNSET, Unset

T = TypeVar("T", bound="Category")


@attr.s(auto_attribs=True)
class Category:
    """A Category is used to group products

    Attributes:
        category_seo_tags (Union[Unset, List[CategorySeoTag]]): This will store category meta data such as description
        description (Union[Unset, str]): Category description
        id (Union[Unset, int]): Category ID
        image (Union[Unset, Image]): Image links.
        name (Union[Unset, str]): Category name
        visible (Union[Unset, bool]): Flag used to determine if the category is public or private.<br>Public categories
            appear as tabs on the company booking form
    """

    category_seo_tags: Union[Unset, List[CategorySeoTag]] = UNSET
    description: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    image: Union[Unset, Image] = UNSET
    name: Union[Unset, str] = UNSET
    visible: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        category_seo_tags: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.category_seo_tags, Unset):
            category_seo_tags = []
            for category_seo_tags_item_data in self.category_seo_tags:
                category_seo_tags_item = category_seo_tags_item_data.to_dict()

                category_seo_tags.append(category_seo_tags_item)

        description = self.description
        id = self.id
        image: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        name = self.name
        visible = self.visible

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if category_seo_tags is not UNSET:
            field_dict["categorySeoTags"] = category_seo_tags
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if image is not UNSET:
            field_dict["image"] = image
        if name is not UNSET:
            field_dict["name"] = name
        if visible is not UNSET:
            field_dict["visible"] = visible

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        category_seo_tags = []
        _category_seo_tags = d.pop("categorySeoTags", UNSET)
        for category_seo_tags_item_data in _category_seo_tags or []:
            category_seo_tags_item = CategorySeoTag.from_dict(category_seo_tags_item_data)

            category_seo_tags.append(category_seo_tags_item)

        description = d.pop("description", UNSET)

        id = d.pop("id", UNSET)

        _image = d.pop("image", UNSET)
        image: Union[Unset, Image]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = Image.from_dict(_image)

        name = d.pop("name", UNSET)

        visible = d.pop("visible", UNSET)

        category = cls(
            category_seo_tags=category_seo_tags,
            description=description,
            id=id,
            image=image,
            name=name,
            visible=visible,
        )

        category.additional_properties = d
        return category

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
