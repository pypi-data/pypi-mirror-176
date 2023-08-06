from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.request_status import RequestStatus
from ..models.rezdy_connect_settings import RezdyConnectSettings
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseRezdyConnectSettings")


@attr.s(auto_attribs=True)
class ResponseRezdyConnectSettings:
    """
    Attributes:
        request_status (RequestStatus):
        rezdy_connect_settings (Union[Unset, RezdyConnectSettings]): Extended product model to support advanced product
            configuration, including RezdyConnect settings
    """

    request_status: RequestStatus
    rezdy_connect_settings: Union[Unset, RezdyConnectSettings] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        rezdy_connect_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rezdy_connect_settings, Unset):
            rezdy_connect_settings = self.rezdy_connect_settings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if rezdy_connect_settings is not UNSET:
            field_dict["rezdyConnectSettings"] = rezdy_connect_settings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _rezdy_connect_settings = d.pop("rezdyConnectSettings", UNSET)
        rezdy_connect_settings: Union[Unset, RezdyConnectSettings]
        if isinstance(_rezdy_connect_settings, Unset):
            rezdy_connect_settings = UNSET
        else:
            rezdy_connect_settings = RezdyConnectSettings.from_dict(_rezdy_connect_settings)

        response_rezdy_connect_settings = cls(
            request_status=request_status,
            rezdy_connect_settings=rezdy_connect_settings,
        )

        response_rezdy_connect_settings.additional_properties = d
        return response_rezdy_connect_settings

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
