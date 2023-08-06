from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    search: Union[Unset, None, str] = UNSET,
    visible: Union[Unset, None, bool] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    url = "{}/categories".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["search"] = search

    params["visible"] = visible

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
    search: Union[Unset, None, str] = UNSET,
    visible: Union[Unset, None, bool] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[Any]:
    """Search categories

     Load all categories matching a search string. If the search string is empty, all categories will be
    returned.
    This will only return categories that belong to the company identified from the request's apiKey.

    Args:
        search (Union[Unset, None, str]):
        visible (Union[Unset, None, bool]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        search=search,
        visible=visible,
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
    search: Union[Unset, None, str] = UNSET,
    visible: Union[Unset, None, bool] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[Any]:
    """Search categories

     Load all categories matching a search string. If the search string is empty, all categories will be
    returned.
    This will only return categories that belong to the company identified from the request's apiKey.

    Args:
        search (Union[Unset, None, str]):
        visible (Union[Unset, None, bool]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        search=search,
        visible=visible,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
