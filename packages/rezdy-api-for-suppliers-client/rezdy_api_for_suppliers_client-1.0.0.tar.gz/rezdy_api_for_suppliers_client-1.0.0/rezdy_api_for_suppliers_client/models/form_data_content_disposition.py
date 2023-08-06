import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.form_data_content_disposition_parameters import FormDataContentDispositionParameters
from ..types import UNSET, Unset

T = TypeVar("T", bound="FormDataContentDisposition")


@attr.s(auto_attribs=True)
class FormDataContentDisposition:
    """
    Attributes:
        creation_date (Union[Unset, datetime.datetime]):
        file_name (Union[Unset, str]):
        modification_date (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        parameters (Union[Unset, FormDataContentDispositionParameters]):
        read_date (Union[Unset, datetime.datetime]):
        size (Union[Unset, int]):
        type (Union[Unset, str]):
    """

    creation_date: Union[Unset, datetime.datetime] = UNSET
    file_name: Union[Unset, str] = UNSET
    modification_date: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    parameters: Union[Unset, FormDataContentDispositionParameters] = UNSET
    read_date: Union[Unset, datetime.datetime] = UNSET
    size: Union[Unset, int] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        creation_date: Union[Unset, str] = UNSET
        if not isinstance(self.creation_date, Unset):
            creation_date = self.creation_date.isoformat()

        file_name = self.file_name
        modification_date: Union[Unset, str] = UNSET
        if not isinstance(self.modification_date, Unset):
            modification_date = self.modification_date.isoformat()

        name = self.name
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        read_date: Union[Unset, str] = UNSET
        if not isinstance(self.read_date, Unset):
            read_date = self.read_date.isoformat()

        size = self.size
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if modification_date is not UNSET:
            field_dict["modificationDate"] = modification_date
        if name is not UNSET:
            field_dict["name"] = name
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if read_date is not UNSET:
            field_dict["readDate"] = read_date
        if size is not UNSET:
            field_dict["size"] = size
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _creation_date = d.pop("creationDate", UNSET)
        creation_date: Union[Unset, datetime.datetime]
        if isinstance(_creation_date, Unset):
            creation_date = UNSET
        else:
            creation_date = isoparse(_creation_date)

        file_name = d.pop("fileName", UNSET)

        _modification_date = d.pop("modificationDate", UNSET)
        modification_date: Union[Unset, datetime.datetime]
        if isinstance(_modification_date, Unset):
            modification_date = UNSET
        else:
            modification_date = isoparse(_modification_date)

        name = d.pop("name", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, FormDataContentDispositionParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = FormDataContentDispositionParameters.from_dict(_parameters)

        _read_date = d.pop("readDate", UNSET)
        read_date: Union[Unset, datetime.datetime]
        if isinstance(_read_date, Unset):
            read_date = UNSET
        else:
            read_date = isoparse(_read_date)

        size = d.pop("size", UNSET)

        type = d.pop("type", UNSET)

        form_data_content_disposition = cls(
            creation_date=creation_date,
            file_name=file_name,
            modification_date=modification_date,
            name=name,
            parameters=parameters,
            read_date=read_date,
            size=size,
            type=type,
        )

        form_data_content_disposition.additional_properties = d
        return form_data_content_disposition

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
