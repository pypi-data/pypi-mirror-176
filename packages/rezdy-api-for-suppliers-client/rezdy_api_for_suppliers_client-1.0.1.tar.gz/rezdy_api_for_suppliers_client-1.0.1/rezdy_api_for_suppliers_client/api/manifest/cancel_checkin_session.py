from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.response_no_data import ResponseNoData
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    product_code: str,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/manifest/checkinSession".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["productCode"] = product_code

    params["startTime"] = start_time

    params["startTimeLocal"] = start_time_local

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseNoData]:
    if response.status_code == 200:
        response_200 = ResponseNoData.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseNoData]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    product_code: str,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
) -> Response[ResponseNoData]:
    """Remove session check-in

     Remove Check-in / No show flag from everyone in the whole session. The session is identified by
    product code and start time (or start time local).<br>
    Only available for the supplier API.<br>

    Args:
        product_code (str):
        start_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):

    Returns:
        Response[ResponseNoData]
    """

    kwargs = _get_kwargs(
        client=client,
        product_code=product_code,
        start_time=start_time,
        start_time_local=start_time_local,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    product_code: str,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
) -> Optional[ResponseNoData]:
    """Remove session check-in

     Remove Check-in / No show flag from everyone in the whole session. The session is identified by
    product code and start time (or start time local).<br>
    Only available for the supplier API.<br>

    Args:
        product_code (str):
        start_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):

    Returns:
        Response[ResponseNoData]
    """

    return sync_detailed(
        client=client,
        product_code=product_code,
        start_time=start_time,
        start_time_local=start_time_local,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    product_code: str,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
) -> Response[ResponseNoData]:
    """Remove session check-in

     Remove Check-in / No show flag from everyone in the whole session. The session is identified by
    product code and start time (or start time local).<br>
    Only available for the supplier API.<br>

    Args:
        product_code (str):
        start_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):

    Returns:
        Response[ResponseNoData]
    """

    kwargs = _get_kwargs(
        client=client,
        product_code=product_code,
        start_time=start_time,
        start_time_local=start_time_local,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    product_code: str,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
) -> Optional[ResponseNoData]:
    """Remove session check-in

     Remove Check-in / No show flag from everyone in the whole session. The session is identified by
    product code and start time (or start time local).<br>
    Only available for the supplier API.<br>

    Args:
        product_code (str):
        start_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):

    Returns:
        Response[ResponseNoData]
    """

    return (
        await asyncio_detailed(
            client=client,
            product_code=product_code,
            start_time=start_time,
            start_time_local=start_time_local,
        )
    ).parsed
