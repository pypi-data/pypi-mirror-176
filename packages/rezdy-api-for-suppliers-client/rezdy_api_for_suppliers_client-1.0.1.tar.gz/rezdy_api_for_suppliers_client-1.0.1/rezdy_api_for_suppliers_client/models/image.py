from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Image")


@attr.s(auto_attribs=True)
class Image:
    """Image links.

    Attributes:
        id (Union[Unset, int]): Id of the image. Can be used for DELETE /{productCode}/image/{mediaId} service
        item_url (Union[Unset, str]): Full size image link
        large_size_url (Union[Unset, str]): Large size image link (1280px)
        medium_size_url (Union[Unset, str]): Medium size image link (480px)
        thumbnail_url (Union[Unset, str]): Thumbnail image link (240px)
    """

    id: Union[Unset, int] = UNSET
    item_url: Union[Unset, str] = UNSET
    large_size_url: Union[Unset, str] = UNSET
    medium_size_url: Union[Unset, str] = UNSET
    thumbnail_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        item_url = self.item_url
        large_size_url = self.large_size_url
        medium_size_url = self.medium_size_url
        thumbnail_url = self.thumbnail_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if item_url is not UNSET:
            field_dict["itemUrl"] = item_url
        if large_size_url is not UNSET:
            field_dict["largeSizeUrl"] = large_size_url
        if medium_size_url is not UNSET:
            field_dict["mediumSizeUrl"] = medium_size_url
        if thumbnail_url is not UNSET:
            field_dict["thumbnailUrl"] = thumbnail_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        item_url = d.pop("itemUrl", UNSET)

        large_size_url = d.pop("largeSizeUrl", UNSET)

        medium_size_url = d.pop("mediumSizeUrl", UNSET)

        thumbnail_url = d.pop("thumbnailUrl", UNSET)

        image = cls(
            id=id,
            item_url=item_url,
            large_size_url=large_size_url,
            medium_size_url=medium_size_url,
            thumbnail_url=thumbnail_url,
        )

        image.additional_properties = d
        return image

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
