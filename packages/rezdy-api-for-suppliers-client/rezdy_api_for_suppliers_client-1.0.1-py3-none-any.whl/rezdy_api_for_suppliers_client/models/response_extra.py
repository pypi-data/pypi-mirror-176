from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extra_request import ExtraRequest
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseExtra")


@attr.s(auto_attribs=True)
class ResponseExtra:
    """
    Attributes:
        request_status (RequestStatus):
        extra (Union[Unset, ExtraRequest]): Partial optional service or item that can be purchased when booking a
            specific product
    """

    request_status: RequestStatus
    extra: Union[Unset, ExtraRequest] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        extra: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra, Unset):
            extra = self.extra.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _extra = d.pop("extra", UNSET)
        extra: Union[Unset, ExtraRequest]
        if isinstance(_extra, Unset):
            extra = UNSET
        else:
            extra = ExtraRequest.from_dict(_extra)

        response_extra = cls(
            request_status=request_status,
            extra=extra,
        )

        response_extra.additional_properties = d
        return response_extra

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
