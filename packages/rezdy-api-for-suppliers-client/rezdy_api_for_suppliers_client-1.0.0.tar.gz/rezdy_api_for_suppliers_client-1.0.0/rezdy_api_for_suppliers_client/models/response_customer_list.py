from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.customer import Customer
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseCustomerList")


@attr.s(auto_attribs=True)
class ResponseCustomerList:
    """
    Attributes:
        request_status (RequestStatus):
        customers (Union[Unset, List[Customer]]):
    """

    request_status: RequestStatus
    customers: Union[Unset, List[Customer]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        customers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.customers, Unset):
            customers = []
            for customers_item_data in self.customers:
                customers_item = customers_item_data.to_dict()

                customers.append(customers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if customers is not UNSET:
            field_dict["customers"] = customers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        customers = []
        _customers = d.pop("customers", UNSET)
        for customers_item_data in _customers or []:
            customers_item = Customer.from_dict(customers_item_data)

            customers.append(customers_item)

        response_customer_list = cls(
            request_status=request_status,
            customers=customers,
        )

        response_customer_list.additional_properties = d
        return response_customer_list

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
