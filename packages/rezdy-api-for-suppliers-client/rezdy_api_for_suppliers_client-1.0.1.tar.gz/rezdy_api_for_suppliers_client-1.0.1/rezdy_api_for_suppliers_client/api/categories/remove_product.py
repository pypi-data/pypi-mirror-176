from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_rate import ResponseRate
from ...types import Response


def _get_kwargs(
    category_id: int,
    product_code: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/categories/{categoryId}/products/{productCode}".format(
        client.base_url, categoryId=category_id, productCode=product_code
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseRate]:
    if response.status_code == 200:
        response_200 = ResponseRate.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseRate]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    category_id: int,
    product_code: str,
    *,
    client: Client,
) -> Response[ResponseRate]:
    """Remove product from category

     Removes a product from an existing category

    Args:
        category_id (int):
        product_code (str):

    Returns:
        Response[ResponseRate]
    """

    kwargs = _get_kwargs(
        category_id=category_id,
        product_code=product_code,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    category_id: int,
    product_code: str,
    *,
    client: Client,
) -> Optional[ResponseRate]:
    """Remove product from category

     Removes a product from an existing category

    Args:
        category_id (int):
        product_code (str):

    Returns:
        Response[ResponseRate]
    """

    return sync_detailed(
        category_id=category_id,
        product_code=product_code,
        client=client,
    ).parsed


async def asyncio_detailed(
    category_id: int,
    product_code: str,
    *,
    client: Client,
) -> Response[ResponseRate]:
    """Remove product from category

     Removes a product from an existing category

    Args:
        category_id (int):
        product_code (str):

    Returns:
        Response[ResponseRate]
    """

    kwargs = _get_kwargs(
        category_id=category_id,
        product_code=product_code,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    category_id: int,
    product_code: str,
    *,
    client: Client,
) -> Optional[ResponseRate]:
    """Remove product from category

     Removes a product from an existing category

    Args:
        category_id (int):
        product_code (str):

    Returns:
        Response[ResponseRate]
    """

    return (
        await asyncio_detailed(
            category_id=category_id,
            product_code=product_code,
            client=client,
        )
    ).parsed
