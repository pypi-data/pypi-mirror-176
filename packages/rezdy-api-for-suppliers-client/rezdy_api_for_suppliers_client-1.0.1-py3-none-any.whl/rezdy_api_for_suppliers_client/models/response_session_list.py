from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.request_status import RequestStatus
from ..models.session import Session
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseSessionList")


@attr.s(auto_attribs=True)
class ResponseSessionList:
    """
    Attributes:
        request_status (RequestStatus):
        sessions (Union[Unset, List[Session]]):
    """

    request_status: RequestStatus
    sessions: Union[Unset, List[Session]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_status = self.request_status.to_dict()

        sessions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sessions, Unset):
            sessions = []
            for sessions_item_data in self.sessions:
                sessions_item = sessions_item_data.to_dict()

                sessions.append(sessions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestStatus": request_status,
            }
        )
        if sessions is not UNSET:
            field_dict["sessions"] = sessions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_status = RequestStatus.from_dict(d.pop("requestStatus"))

        sessions = []
        _sessions = d.pop("sessions", UNSET)
        for sessions_item_data in _sessions or []:
            sessions_item = Session.from_dict(sessions_item_data)

            sessions.append(sessions_item)

        response_session_list = cls(
            request_status=request_status,
            sessions=sessions,
        )

        response_session_list.additional_properties = d
        return response_session_list

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
