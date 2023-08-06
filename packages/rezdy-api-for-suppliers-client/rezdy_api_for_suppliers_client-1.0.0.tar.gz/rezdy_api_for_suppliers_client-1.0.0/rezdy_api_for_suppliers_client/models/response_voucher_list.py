from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.request_status import RequestStatus
from ..models.voucher import Voucher
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseVoucherList")


@attr.s(auto_attribs=True)
class ResponseVoucherList:
    """
    Attributes:
        request_status (RequestStatus):
        vouchers (Union[Unset, List[Voucher]]):
    """

    request_status: RequestStatus
    vouchers: Union[Unset, List[Voucher]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        vouchers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vouchers, Unset):
            vouchers = []
            for vouchers_item_data in self.vouchers:
                vouchers_item = vouchers_item_data.to_dict()

                vouchers.append(vouchers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if vouchers is not UNSET:
            field_dict["vouchers"] = vouchers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        vouchers = []
        _vouchers = d.pop("vouchers", UNSET)
        for vouchers_item_data in _vouchers or []:
            vouchers_item = Voucher.from_dict(vouchers_item_data)

            vouchers.append(vouchers_item)

        response_voucher_list = cls(
            request_status=request_status,
            vouchers=vouchers,
        )

        response_voucher_list.additional_properties = d
        return response_voucher_list

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
