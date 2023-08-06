from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    session_id: Union[Unset, None, int] = UNSET,
    product_code: Union[Unset, None, str] = UNSET,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    url = "{}/resources/session".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["sessionId"] = session_id

    params["productCode"] = product_code

    params["startTime"] = start_time

    params["startTimeLocal"] = start_time_local

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
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
    session_id: Union[Unset, None, int] = UNSET,
    product_code: Union[Unset, None, str] = UNSET,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[Any]:
    """Get session resources

     Retrieve resources assigned to the session. Session has to be specified either by sessionId or by
    product code and start time (or start time local).

    Args:
        session_id (Union[Unset, None, int]):
        product_code (Union[Unset, None, str]):
        start_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        session_id=session_id,
        product_code=product_code,
        start_time=start_time,
        start_time_local=start_time_local,
        limit=limit,
        offset=offset,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    session_id: Union[Unset, None, int] = UNSET,
    product_code: Union[Unset, None, str] = UNSET,
    start_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[Any]:
    """Get session resources

     Retrieve resources assigned to the session. Session has to be specified either by sessionId or by
    product code and start time (or start time local).

    Args:
        session_id (Union[Unset, None, int]):
        product_code (Union[Unset, None, str]):
        start_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        session_id=session_id,
        product_code=product_code,
        start_time=start_time,
        start_time_local=start_time_local,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
