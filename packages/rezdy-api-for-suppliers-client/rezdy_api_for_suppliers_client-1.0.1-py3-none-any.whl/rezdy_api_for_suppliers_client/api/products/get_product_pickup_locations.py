from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.response_pickup_location_list import ResponsePickupLocationList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    product_code: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    url = "{}/products/{productCode}/pickups".format(client.base_url, productCode=product_code)

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


def _parse_response(*, response: httpx.Response) -> Optional[ResponsePickupLocationList]:
    if response.status_code == 200:
        response_200 = ResponsePickupLocationList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponsePickupLocationList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    product_code: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponsePickupLocationList]:
    """Get product pickups

     Gets a list of pickup locations configured for this product.

    Args:
        product_code (str):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponsePickupLocationList]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
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
    product_code: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponsePickupLocationList]:
    """Get product pickups

     Gets a list of pickup locations configured for this product.

    Args:
        product_code (str):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponsePickupLocationList]
    """

    return sync_detailed(
        product_code=product_code,
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    product_code: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponsePickupLocationList]:
    """Get product pickups

     Gets a list of pickup locations configured for this product.

    Args:
        product_code (str):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponsePickupLocationList]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        client=client,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    product_code: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponsePickupLocationList]:
    """Get product pickups

     Gets a list of pickup locations configured for this product.

    Args:
        product_code (str):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponsePickupLocationList]
    """

    return (
        await asyncio_detailed(
            product_code=product_code,
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
