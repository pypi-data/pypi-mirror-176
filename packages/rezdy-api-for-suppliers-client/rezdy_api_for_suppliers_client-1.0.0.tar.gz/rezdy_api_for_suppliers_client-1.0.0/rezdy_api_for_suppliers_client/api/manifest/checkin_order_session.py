from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    order_number: Union[Unset, None, str] = UNSET,
    product_code: str,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    checkin: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/manifest/checkinOrderSession".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["orderNumber"] = order_number

    params["productCode"] = product_code

    params["startTime"] = start_time

    params["startTimeLocal"] = start_time_local

    params["checkin"] = checkin

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
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
    *,
    client: Client,
    order_number: Union[Unset, None, str] = UNSET,
    product_code: str,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    checkin: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Check-in order item

     Place Check-in a / No show flag for the specified order item. The order item is identified by order
    number, product code and start time (or start time local).<br>
    Only available for the supplier API.<br>

    Args:
        order_number (Union[Unset, None, str]):
        product_code (str):
        start_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        checkin (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        order_number=order_number,
        product_code=product_code,
        start_time=start_time,
        start_time_local=start_time_local,
        checkin=checkin,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    order_number: Union[Unset, None, str] = UNSET,
    product_code: str,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    checkin: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Check-in order item

     Place Check-in a / No show flag for the specified order item. The order item is identified by order
    number, product code and start time (or start time local).<br>
    Only available for the supplier API.<br>

    Args:
        order_number (Union[Unset, None, str]):
        product_code (str):
        start_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        checkin (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        order_number=order_number,
        product_code=product_code,
        start_time=start_time,
        start_time_local=start_time_local,
        checkin=checkin,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
