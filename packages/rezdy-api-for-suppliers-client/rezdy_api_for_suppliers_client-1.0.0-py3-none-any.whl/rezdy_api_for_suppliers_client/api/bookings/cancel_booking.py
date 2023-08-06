from typing import Any, Dict, Union

import httpx

from ...client import Client
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


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    order_number: str,
    *,
    client: Client,
    send_notifications: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Cancel booking

     Cancel an existing booking and send notifications about the cancellation. In case of an Automated
    Payment booking, will also refund payment.

    Args:
        order_number (str):
        send_notifications (Union[Unset, None, bool]):

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    order_number: str,
    *,
    client: Client,
    send_notifications: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Cancel booking

     Cancel an existing booking and send notifications about the cancellation. In case of an Automated
    Payment booking, will also refund payment.

    Args:
        order_number (str):
        send_notifications (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        order_number=order_number,
        client=client,
        send_notifications=send_notifications,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
