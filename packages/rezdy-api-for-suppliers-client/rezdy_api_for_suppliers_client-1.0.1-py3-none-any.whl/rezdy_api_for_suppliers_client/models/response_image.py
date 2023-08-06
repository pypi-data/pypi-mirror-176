from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.image import Image
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseImage")


@attr.s(auto_attribs=True)
class ResponseImage:
    """
    Attributes:
        request_status (RequestStatus):
        img (Union[Unset, Image]): Image links.
    """

    request_status: RequestStatus
    img: Union[Unset, Image] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        img: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.img, Unset):
            img = self.img.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if img is not UNSET:
            field_dict["img"] = img

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _img = d.pop("img", UNSET)
        img: Union[Unset, Image]
        if isinstance(_img, Unset):
            img = UNSET
        else:
            img = Image.from_dict(_img)

        response_image = cls(
            request_status=request_status,
            img=img,
        )

        response_image.additional_properties = d
        return response_image

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
