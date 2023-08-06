from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.customer import Customer
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseCustomer")


@attr.s(auto_attribs=True)
class ResponseCustomer:
    """
    Attributes:
        request_status (RequestStatus):
        customer (Union[Unset, Customer]): The customer is the person making the booking, and most of the time paying
            for it.<br>It differs from Participants, who are the people attending a tour
    """

    request_status: RequestStatus
    customer: Union[Unset, Customer] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        customer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.customer, Unset):
            customer = self.customer.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if customer is not UNSET:
            field_dict["customer"] = customer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _customer = d.pop("customer", UNSET)
        customer: Union[Unset, Customer]
        if isinstance(_customer, Unset):
            customer = UNSET
        else:
            customer = Customer.from_dict(_customer)

        response_customer = cls(
            request_status=request_status,
            customer=customer,
        )

        response_customer.additional_properties = d
        return response_customer

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
