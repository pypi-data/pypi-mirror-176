from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.response_booking import ResponseBooking
from ...types import UNSET, Response, Unset


def _get_kwargs(
    order_number: str,
    *,
    client: Client,
    send_notifications: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/bookings/{orderNumber}".format(client.base_url, orderNumber=order_number)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["sendNotifications"] = send_notifications

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    send_notifications: Union[Unset, None, bool] = UNSET,
) -> Response[ResponseBooking]:
    """Cancel booking

     Cancel an existing booking and send notifications about the cancellation. In case of an Automated
    Payment booking, will also refund payment.

    Args:
        order_number (str):
        send_notifications (Union[Unset, None, bool]):

    Returns:
        Response[ResponseBooking]
    """

    kwargs = _get_kwargs(
        order_number=order_number,
        client=client,
        send_notifications=send_notifications,
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
    send_notifications: Union[Unset, None, bool] = UNSET,
) -> Optional[ResponseBooking]:
    """Cancel booking

     Cancel an existing booking and send notifications about the cancellation. In case of an Automated
    Payment booking, will also refund payment.

    Args:
        order_number (str):
        send_notifications (Union[Unset, None, bool]):

    Returns:
        Response[ResponseBooking]
    """

    return sync_detailed(
        order_number=order_number,
        client=client,
        send_notifications=send_notifications,
    ).parsed


async def asyncio_detailed(
    order_number: str,
    *,
    client: Client,
    send_notifications: Union[Unset, None, bool] = UNSET,
) -> Response[ResponseBooking]:
    """Cancel booking

     Cancel an existing booking and send notifications about the cancellation. In case of an Automated
    Payment booking, will also refund payment.

    Args:
        order_number (str):
        send_notifications (Union[Unset, None, bool]):

    Returns:
        Response[ResponseBooking]
    """

    kwargs = _get_kwargs(
        order_number=order_number,
        client=client,
        send_notifications=send_notifications,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    order_number: str,
    *,
    client: Client,
    send_notifications: Union[Unset, None, bool] = UNSET,
) -> Optional[ResponseBooking]:
    """Cancel booking

     Cancel an existing booking and send notifications about the cancellation. In case of an Automated
    Payment booking, will also refund payment.

    Args:
        order_number (str):
        send_notifications (Union[Unset, None, bool]):

    Returns:
        Response[ResponseBooking]
    """

    return (
        await asyncio_detailed(
            order_number=order_number,
            client=client,
            send_notifications=send_notifications,
        )
    ).parsed
