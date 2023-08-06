from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.request_status import RequestStatus
from ..models.session import Session
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseSession")


@attr.s(auto_attribs=True)
class ResponseSession:
    """
    Attributes:
        request_status (RequestStatus):
        session (Union[Unset, Session]): A Session holds availability for a unique product / start time combination and
            also the rates for the session booking.
    """

    request_status: RequestStatus
    session: Union[Unset, Session] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        session: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.session, Unset):
            session = self.session.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if session is not UNSET:
            field_dict["session"] = session

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        _session = d.pop("session", UNSET)
        session: Union[Unset, Session]
        if isinstance(_session, Unset):
            session = UNSET
        else:
            session = Session.from_dict(_session)

        response_session = cls(
            request_status=request_status,
            session=session,
        )

        response_session.additional_properties = d
        return response_session

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
