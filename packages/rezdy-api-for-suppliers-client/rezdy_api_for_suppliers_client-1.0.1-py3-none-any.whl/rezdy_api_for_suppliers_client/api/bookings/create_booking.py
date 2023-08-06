from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.booking_create import BookingCreate
from ...models.response_booking import ResponseBooking
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: BookingCreate,
) -> Dict[str, Any]:
    url = "{}/bookings".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseBooking]:
    if response.status_code == 200:
        response_200 = ResponseBooking.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseBooking]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: BookingCreate,
) -> Response[ResponseBooking]:
    """Create booking

     Create a new booking. Many of payload fields are not required and will be calculated if not
    specified. Please check the example request payloads for different booking scenarios.

    Args:
        json_body (BookingCreate): Booking create object used to create a booking in Rezdy's
            system. Lists all the possible fields for all product types and scenarios. Most of them
            are not required when sending a new booking.<br>A single Booking can be used to book
            multiple products, each of them being a BookingItem. All the products of one booking have
            to be from the same supplier.

    Returns:
        Response[ResponseBooking]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: BookingCreate,
) -> Optional[ResponseBooking]:
    """Create booking

     Create a new booking. Many of payload fields are not required and will be calculated if not
    specified. Please check the example request payloads for different booking scenarios.

    Args:
        json_body (BookingCreate): Booking create object used to create a booking in Rezdy's
            system. Lists all the possible fields for all product types and scenarios. Most of them
            are not required when sending a new booking.<br>A single Booking can be used to book
            multiple products, each of them being a BookingItem. All the products of one booking have
            to be from the same supplier.

    Returns:
        Response[ResponseBooking]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: BookingCreate,
) -> Response[ResponseBooking]:
    """Create booking

     Create a new booking. Many of payload fields are not required and will be calculated if not
    specified. Please check the example request payloads for different booking scenarios.

    Args:
        json_body (BookingCreate): Booking create object used to create a booking in Rezdy's
            system. Lists all the possible fields for all product types and scenarios. Most of them
            are not required when sending a new booking.<br>A single Booking can be used to book
            multiple products, each of them being a BookingItem. All the products of one booking have
            to be from the same supplier.

    Returns:
        Response[ResponseBooking]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: BookingCreate,
) -> Optional[ResponseBooking]:
    """Create booking

     Create a new booking. Many of payload fields are not required and will be calculated if not
    specified. Please check the example request payloads for different booking scenarios.

    Args:
        json_body (BookingCreate): Booking create object used to create a booking in Rezdy's
            system. Lists all the possible fields for all product types and scenarios. Most of them
            are not required when sending a new booking.<br>A single Booking can be used to book
            multiple products, each of them being a BookingItem. All the products of one booking have
            to be from the same supplier.

    Returns:
        Response[ResponseBooking]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
