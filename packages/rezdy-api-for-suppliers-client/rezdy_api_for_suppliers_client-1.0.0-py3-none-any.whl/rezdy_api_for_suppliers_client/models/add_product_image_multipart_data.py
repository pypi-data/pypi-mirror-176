import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.form_data_content_disposition import FormDataContentDisposition
from ..types import UNSET, Unset

T = TypeVar("T", bound="AddProductImageMultipartData")


@attr.s(auto_attribs=True)
class AddProductImageMultipartData:
    """
    Attributes:
        file (FormDataContentDisposition):
        filename (Union[Unset, str]):
    """

    file: FormDataContentDisposition
    filename: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_dict()

        filename = self.filename

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )
        if filename is not UNSET:
            field_dict["filename"] = filename

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file = (None, json.dumps(self.file.to_dict()).encode(), "application/json")

        filename = (
            self.filename if isinstance(self.filename, Unset) else (None, str(self.filename).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "file": file,
            }
        )
        if filename is not UNSET:
            field_dict["filename"] = filename

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file = FormDataContentDisposition.from_dict(d.pop("file"))

        filename = d.pop("filename", UNSET)

        add_product_image_multipart_data = cls(
            file=file,
            filename=filename,
        )

        add_product_image_multipart_data.additional_properties = d
        return add_product_image_multipart_data

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
