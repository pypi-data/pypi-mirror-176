from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    resource_id: int,
    *,
    client: Client,
    start_time: Union[Unset, None, str] = UNSET,
    end_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    end_time_local: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    url = "{}/resources/{resourceId}/sessions".format(client.base_url, resourceId=resource_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["startTime"] = start_time

    params["endTime"] = end_time

    params["startTimeLocal"] = start_time_local

    params["endTimeLocal"] = end_time_local

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
    resource_id: int,
    *,
    client: Client,
    start_time: Union[Unset, None, str] = UNSET,
    end_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    end_time_local: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[Any]:
    """Get resource sessions

     Retrieves all sessions for the specified resource within the start/end datetime range. Pagination
    using limit and offset is applied to the result list.

    Args:
        resource_id (int):
        start_time (Union[Unset, None, str]):
        end_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        end_time_local (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        client=client,
        start_time=start_time,
        end_time=end_time,
        start_time_local=start_time_local,
        end_time_local=end_time_local,
        limit=limit,
        offset=offset,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    resource_id: int,
    *,
    client: Client,
    start_time: Union[Unset, None, str] = UNSET,
    end_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    end_time_local: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[Any]:
    """Get resource sessions

     Retrieves all sessions for the specified resource within the start/end datetime range. Pagination
    using limit and offset is applied to the result list.

    Args:
        resource_id (int):
        start_time (Union[Unset, None, str]):
        end_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        end_time_local (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        client=client,
        start_time=start_time,
        end_time=end_time,
        start_time_local=start_time_local,
        end_time_local=end_time_local,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
