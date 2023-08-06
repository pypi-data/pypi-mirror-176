from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.resource_type import ResourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Resource")


@attr.s(auto_attribs=True)
class Resource:
    """Supplier resource - e.g. raft, bus, tour guide, venue which has a limited capacity. The resources can be shared
    between different supplier's products. If the resource does not have any spare availability, the booking of any of
    the product sessions, where the resource is used will not be possible.

        Attributes:
            id (Union[Unset, int]): Rezdy internal id of the resource.
            name (Union[Unset, str]): Resource name
            seats (Union[Unset, int]): Availability of the resource
            type (Union[Unset, ResourceType]): Resource type
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    seats: Union[Unset, int] = UNSET
    type: Union[Unset, ResourceType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        seats = self.seats
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if seats is not UNSET:
            field_dict["seats"] = seats
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        seats = d.pop("seats", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ResourceType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ResourceType(_type)

        resource = cls(
            id=id,
            name=name,
            seats=seats,
            type=type,
        )

        resource.additional_properties = d
        return resource

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
