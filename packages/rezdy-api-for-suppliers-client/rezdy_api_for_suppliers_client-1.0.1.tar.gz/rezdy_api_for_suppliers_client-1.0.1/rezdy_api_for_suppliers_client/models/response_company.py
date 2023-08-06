from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.company import Company
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseCompany")


@attr.s(auto_attribs=True)
class ResponseCompany:
    """
    Attributes:
        request_status (RequestStatus):
        company (Union[Unset, Company]): Company object. Holds general details and information about a specific company.
    """

    request_status: RequestStatus
    company: Union[Unset, Company] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        company: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.company, Unset):
            company = self.company.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if company is not UNSET:
            field_dict["company"] = company

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _company = d.pop("company", UNSET)
        company: Union[Unset, Company]
        if isinstance(_company, Unset):
            company = UNSET
        else:
            company = Company.from_dict(_company)

        response_company = cls(
            request_status=request_status,
            company=company,
        )

        response_company.additional_properties = d
        return response_company

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
