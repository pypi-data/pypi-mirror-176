from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.product_create_request import ProductCreateRequest
from ...models.response_product import ResponseProduct
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ProductCreateRequest,
) -> Dict[str, Any]:
    url = "{}/products".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseProduct]:
    if response.status_code == 200:
        response_200 = ResponseProduct.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseProduct]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ProductCreateRequest,
) -> Response[ResponseProduct]:
    """Create product

    Args:
        json_body (ProductCreateRequest): Partial product model containing all fields which are
            currently supported in product create via API.

    Returns:
        Response[ResponseProduct]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: ProductCreateRequest,
) -> Optional[ResponseProduct]:
    """Create product

    Args:
        json_body (ProductCreateRequest): Partial product model containing all fields which are
            currently supported in product create via API.

    Returns:
        Response[ResponseProduct]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ProductCreateRequest,
) -> Response[ResponseProduct]:
    """Create product

    Args:
        json_body (ProductCreateRequest): Partial product model containing all fields which are
            currently supported in product create via API.

    Returns:
        Response[ResponseProduct]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: ProductCreateRequest,
) -> Optional[ResponseProduct]:
    """Create product

    Args:
        json_body (ProductCreateRequest): Partial product model containing all fields which are
            currently supported in product create via API.

    Returns:
        Response[ResponseProduct]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
