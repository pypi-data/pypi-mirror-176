from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_booking import ResponseBooking
from ...types import Response


def _get_kwargs(
    order_number: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/bookings/{orderNumber}".format(client.base_url, orderNumber=order_number)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    order_number: str,
    *,
    client: Client,
) -> Response[ResponseBooking]:
    """Get booking

     Load an existing booking by Order Number

    Args:
        order_number (str):

    Returns:
        Response[ResponseBooking]
    """

    kwargs = _get_kwargs(
        order_number=order_number,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    order_number: str,
    *,
    client: Client,
) -> Optional[ResponseBooking]:
    """Get booking

     Load an existing booking by Order Number

    Args:
        order_number (str):

    Returns:
        Response[ResponseBooking]
    """

    return sync_detailed(
        order_number=order_number,
        client=client,
    ).parsed


async def asyncio_detailed(
    order_number: str,
    *,
    client: Client,
) -> Response[ResponseBooking]:
    """Get booking

     Load an existing booking by Order Number

    Args:
        order_number (str):

    Returns:
        Response[ResponseBooking]
    """

    kwargs = _get_kwargs(
        order_number=order_number,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    order_number: str,
    *,
    client: Client,
) -> Optional[ResponseBooking]:
    """Get booking

     Load an existing booking by Order Number

    Args:
        order_number (str):

    Returns:
        Response[ResponseBooking]
    """

    return (
        await asyncio_detailed(
            order_number=order_number,
            client=client,
        )
    ).parsed
