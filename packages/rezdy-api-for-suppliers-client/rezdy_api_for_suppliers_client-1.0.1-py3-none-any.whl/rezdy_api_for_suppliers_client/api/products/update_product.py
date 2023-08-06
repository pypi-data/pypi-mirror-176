from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.product_update_request import ProductUpdateRequest
from ...models.response_product import ResponseProduct
from ...types import Response


def _get_kwargs(
    product_code: str,
    *,
    client: Client,
    json_body: ProductUpdateRequest,
) -> Dict[str, Any]:
    url = "{}/products/{productCode}".format(client.base_url, productCode=product_code)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
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
    product_code: str,
    *,
    client: Client,
    json_body: ProductUpdateRequest,
) -> Response[ResponseProduct]:
    """Update product

     Updates a product.

    When updating price options, the full list of existing price options must be supplied in the update.
    Otherwise the system will remove any missing price options in the request from the product.

    For instance, if a product has 2 price options Adult and Child but the update request only contains
    Adult, the Child price option will be removed from the product.<br>
    Adding a price option works the same way. If the update request contains an extra price option, it
    will be added to the product.

    When price option values are updated via API, this will override all existing price in availability
    (session) to reflect the product price.
    If a different price in calendar/session is required to the product price, please make the changes
    to the product directly in your Rezdy account and select `do not change session price` in the page
    that follows after saving your changes.,


    Args:
        product_code (str):
        json_body (ProductUpdateRequest): Partial product model containing all fields which are
            currently supported in product create via API.

    Returns:
        Response[ResponseProduct]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        client=client,
        json_body=json_body,
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
    json_body: ProductUpdateRequest,
) -> Optional[ResponseProduct]:
    """Update product

     Updates a product.

    When updating price options, the full list of existing price options must be supplied in the update.
    Otherwise the system will remove any missing price options in the request from the product.

    For instance, if a product has 2 price options Adult and Child but the update request only contains
    Adult, the Child price option will be removed from the product.<br>
    Adding a price option works the same way. If the update request contains an extra price option, it
    will be added to the product.

    When price option values are updated via API, this will override all existing price in availability
    (session) to reflect the product price.
    If a different price in calendar/session is required to the product price, please make the changes
    to the product directly in your Rezdy account and select `do not change session price` in the page
    that follows after saving your changes.,


    Args:
        product_code (str):
        json_body (ProductUpdateRequest): Partial product model containing all fields which are
            currently supported in product create via API.

    Returns:
        Response[ResponseProduct]
    """

    return sync_detailed(
        product_code=product_code,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    product_code: str,
    *,
    client: Client,
    json_body: ProductUpdateRequest,
) -> Response[ResponseProduct]:
    """Update product

     Updates a product.

    When updating price options, the full list of existing price options must be supplied in the update.
    Otherwise the system will remove any missing price options in the request from the product.

    For instance, if a product has 2 price options Adult and Child but the update request only contains
    Adult, the Child price option will be removed from the product.<br>
    Adding a price option works the same way. If the update request contains an extra price option, it
    will be added to the product.

    When price option values are updated via API, this will override all existing price in availability
    (session) to reflect the product price.
    If a different price in calendar/session is required to the product price, please make the changes
    to the product directly in your Rezdy account and select `do not change session price` in the page
    that follows after saving your changes.,


    Args:
        product_code (str):
        json_body (ProductUpdateRequest): Partial product model containing all fields which are
            currently supported in product create via API.

    Returns:
        Response[ResponseProduct]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    product_code: str,
    *,
    client: Client,
    json_body: ProductUpdateRequest,
) -> Optional[ResponseProduct]:
    """Update product

     Updates a product.

    When updating price options, the full list of existing price options must be supplied in the update.
    Otherwise the system will remove any missing price options in the request from the product.

    For instance, if a product has 2 price options Adult and Child but the update request only contains
    Adult, the Child price option will be removed from the product.<br>
    Adding a price option works the same way. If the update request contains an extra price option, it
    will be added to the product.

    When price option values are updated via API, this will override all existing price in availability
    (session) to reflect the product price.
    If a different price in calendar/session is required to the product price, please make the changes
    to the product directly in your Rezdy account and select `do not change session price` in the page
    that follows after saving your changes.,


    Args:
        product_code (str):
        json_body (ProductUpdateRequest): Partial product model containing all fields which are
            currently supported in product create via API.

    Returns:
        Response[ResponseProduct]
    """

    return (
        await asyncio_detailed(
            product_code=product_code,
            client=client,
            json_body=json_body,
        )
    ).parsed
