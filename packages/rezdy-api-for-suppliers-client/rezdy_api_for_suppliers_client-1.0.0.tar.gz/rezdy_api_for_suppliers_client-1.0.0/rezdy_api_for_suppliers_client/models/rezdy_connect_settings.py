from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.rezdy_connect_settings_external_api_format import RezdyConnectSettingsExternalApiFormat
from ..models.rezdy_connect_settings_external_booking_strategy import RezdyConnectSettingsExternalBookingStrategy
from ..types import UNSET, Unset

T = TypeVar("T", bound="RezdyConnectSettings")


@attr.s(auto_attribs=True)
class RezdyConnectSettings:
    """Extended product model to support advanced product configuration, including RezdyConnect settings

    Attributes:
        product_code (str): Rezdy-generated unique Product code. Used by agents and for API calls
        external_api_format (Union[Unset, RezdyConnectSettingsExternalApiFormat]): Data format for an external inventory
            mode product. Use it to specifya payload data format for RezdyConnect calls, when creating a product.
        external_availability_api (Union[Unset, str]): External availability endpoint for an external inventory mode
            product. Use it to specify an availability endpoint for RezdyConnect calls, when creating a product.
        external_booking_api (Union[Unset, str]): External booking endpoint for an external inventory mode product. Use
            it to specify a booking endpoint for RezdyConnect calls, when creating a product.
        external_booking_strategy (Union[Unset, RezdyConnectSettingsExternalBookingStrategy]): Booking strategy for an
            external inventory mode product. Use it to specify a booking strategy for RezdyConnect calls, when creating a
            product.
        external_cancellation_api (Union[Unset, str]): External booking cancellation endpoint for an external inventory
            mode product. Use it to specify a cancellation endpoint for RezdyConnect calls, when creating a product.
        external_reservation_api (Union[Unset, str]): External reservation endpoint for an external inventory mode
            product. Use it to specify a reservation endpoint for RezdyConnect calls, when creating a product.
    """

    product_code: str
    external_api_format: Union[Unset, RezdyConnectSettingsExternalApiFormat] = UNSET
    external_availability_api: Union[Unset, str] = UNSET
    external_booking_api: Union[Unset, str] = UNSET
    external_booking_strategy: Union[Unset, RezdyConnectSettingsExternalBookingStrategy] = UNSET
    external_cancellation_api: Union[Unset, str] = UNSET
    external_reservation_api: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        product_code = self.product_code
        external_api_format: Union[Unset, str] = UNSET
        if not isinstance(self.external_api_format, Unset):
            external_api_format = self.external_api_format.value

        external_availability_api = self.external_availability_api
        external_booking_api = self.external_booking_api
        external_booking_strategy: Union[Unset, str] = UNSET
        if not isinstance(self.external_booking_strategy, Unset):
            external_booking_strategy = self.external_booking_strategy.value

        external_cancellation_api = self.external_cancellation_api
        external_reservation_api = self.external_reservation_api

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "productCode": product_code,
            }
        )
        if external_api_format is not UNSET:
            field_dict["externalApiFormat"] = external_api_format
        if external_availability_api is not UNSET:
            field_dict["externalAvailabilityApi"] = external_availability_api
        if external_booking_api is not UNSET:
            field_dict["externalBookingApi"] = external_booking_api
        if external_booking_strategy is not UNSET:
            field_dict["externalBookingStrategy"] = external_booking_strategy
        if external_cancellation_api is not UNSET:
            field_dict["externalCancellationApi"] = external_cancellation_api
        if external_reservation_api is not UNSET:
            field_dict["externalReservationApi"] = external_reservation_api

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        product_code = d.pop("productCode")

        _external_api_format = d.pop("externalApiFormat", UNSET)
        external_api_format: Union[Unset, RezdyConnectSettingsExternalApiFormat]
        if isinstance(_external_api_format, Unset):
            external_api_format = UNSET
        else:
            external_api_format = RezdyConnectSettingsExternalApiFormat(_external_api_format)

        external_availability_api = d.pop("externalAvailabilityApi", UNSET)

        external_booking_api = d.pop("externalBookingApi", UNSET)

        _external_booking_strategy = d.pop("externalBookingStrategy", UNSET)
        external_booking_strategy: Union[Unset, RezdyConnectSettingsExternalBookingStrategy]
        if isinstance(_external_booking_strategy, Unset):
            external_booking_strategy = UNSET
        else:
            external_booking_strategy = RezdyConnectSettingsExternalBookingStrategy(_external_booking_strategy)

        external_cancellation_api = d.pop("externalCancellationApi", UNSET)

        external_reservation_api = d.pop("externalReservationApi", UNSET)

        rezdy_connect_settings = cls(
            product_code=product_code,
            external_api_format=external_api_format,
            external_availability_api=external_availability_api,
            external_booking_api=external_booking_api,
            external_booking_strategy=external_booking_strategy,
            external_cancellation_api=external_cancellation_api,
            external_reservation_api=external_reservation_api,
        )

        rezdy_connect_settings.additional_properties = d
        return rezdy_connect_settings

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
