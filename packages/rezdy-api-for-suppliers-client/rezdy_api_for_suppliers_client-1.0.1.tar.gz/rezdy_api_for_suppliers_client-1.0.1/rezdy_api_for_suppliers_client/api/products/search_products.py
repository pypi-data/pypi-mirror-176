from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.response_product_list import ResponseProductList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    search: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    url = "{}/products".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["search"] = search

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


def _parse_response(*, response: httpx.Response) -> Optional[ResponseProductList]:
    if response.status_code == 200:
        response_200 = ResponseProductList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseProductList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    search: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponseProductList]:
    """Search products

     Searches a product that matches a search string.<br> Load all products matching a search string. If
    the search string is empty, all your products will be returned.<br>
    Use this service when acting as a supplier, to load your own products.<br>
    If you're acting as an agent, use the /products/marketplace service<br>

    Args:
        search (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseProductList]
    """

    kwargs = _get_kwargs(
        client=client,
        search=search,
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
    search: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponseProductList]:
    """Search products

     Searches a product that matches a search string.<br> Load all products matching a search string. If
    the search string is empty, all your products will be returned.<br>
    Use this service when acting as a supplier, to load your own products.<br>
    If you're acting as an agent, use the /products/marketplace service<br>

    Args:
        search (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseProductList]
    """

    return sync_detailed(
        client=client,
        search=search,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    search: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponseProductList]:
    """Search products

     Searches a product that matches a search string.<br> Load all products matching a search string. If
    the search string is empty, all your products will be returned.<br>
    Use this service when acting as a supplier, to load your own products.<br>
    If you're acting as an agent, use the /products/marketplace service<br>

    Args:
        search (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseProductList]
    """

    kwargs = _get_kwargs(
        client=client,
        search=search,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    search: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponseProductList]:
    """Search products

     Searches a product that matches a search string.<br> Load all products matching a search string. If
    the search string is empty, all your products will be returned.<br>
    Use this service when acting as a supplier, to load your own products.<br>
    If you're acting as an agent, use the /products/marketplace service<br>

    Args:
        search (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseProductList]
    """

    return (
        await asyncio_detailed(
            client=client,
            search=search,
            limit=limit,
            offset=offset,
        )
    ).parsed
