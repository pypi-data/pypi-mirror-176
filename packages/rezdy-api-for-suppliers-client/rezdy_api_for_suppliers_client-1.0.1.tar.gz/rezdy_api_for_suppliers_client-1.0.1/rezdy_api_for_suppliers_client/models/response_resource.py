from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.request_status import RequestStatus
from ..models.resource import Resource
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseResource")


@attr.s(auto_attribs=True)
class ResponseResource:
    """
    Attributes:
        request_status (RequestStatus):
        resource (Union[Unset, Resource]): Supplier resource - e.g. raft, bus, tour guide, venue which has a limited
            capacity. The resources can be shared between different supplier's products. If the resource does not have any
            spare availability, the booking of any of the product sessions, where the resource is used will not be possible.
    """

    request_status: RequestStatus
    resource: Union[Unset, Resource] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        resource: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource, Unset):
            resource = self.resource.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if resource is not UNSET:
            field_dict["resource"] = resource

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _resource = d.pop("resource", UNSET)
        resource: Union[Unset, Resource]
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = Resource.from_dict(_resource)

        response_resource = cls(
            request_status=request_status,
            resource=resource,
        )

        response_resource.additional_properties = d
        return response_resource

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
