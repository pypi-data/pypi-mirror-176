from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.response_resource_list import ResponseResourceList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    url = "{}/resources".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
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


def _parse_response(*, response: httpx.Response) -> Optional[ResponseResourceList]:
    if response.status_code == 200:
        response_200 = ResponseResourceList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseResourceList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponseResourceList]:
    """List resources

     Retrieve all supplier resources. Pagination using limit and offset is applied to the result list.

    Args:
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseResourceList]
    """

    kwargs = _get_kwargs(
        client=client,
        limit=limit,
        offset=offset,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponseResourceList]:
    """List resources

     Retrieve all supplier resources. Pagination using limit and offset is applied to the result list.

    Args:
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseResourceList]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponseResourceList]:
    """List resources

     Retrieve all supplier resources. Pagination using limit and offset is applied to the result list.

    Args:
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseResourceList]
    """

    kwargs = _get_kwargs(
        client=client,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponseResourceList]:
    """List resources

     Retrieve all supplier resources. Pagination using limit and offset is applied to the result list.

    Args:
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseResourceList]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
