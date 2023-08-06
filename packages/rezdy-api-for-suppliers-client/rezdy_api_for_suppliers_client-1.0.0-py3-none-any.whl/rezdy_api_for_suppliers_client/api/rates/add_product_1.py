from typing import Any, Dict

import httpx

from ...client import Client
from ...models.product_rate import ProductRate
from ...types import Response


def _get_kwargs(
    rate_id: int,
    product_code: str,
    *,
    client: Client,
    json_body: ProductRate,
) -> Dict[str, Any]:
    url = "{}/rates/{rateId}/products/{productCode}".format(client.base_url, rateId=rate_id, productCode=product_code)

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


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    rate_id: int,
    product_code: str,
    *,
    client: Client,
    json_body: ProductRate,
) -> Response[Any]:
    """Add product

     Adds a product to the specified rate

    Args:
        rate_id (int):
        product_code (str):
        json_body (ProductRate): A ProductRate is used to map a product and its associated value
            commission

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        rate_id=rate_id,
        product_code=product_code,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    rate_id: int,
    product_code: str,
    *,
    client: Client,
    json_body: ProductRate,
) -> Response[Any]:
    """Add product

     Adds a product to the specified rate

    Args:
        rate_id (int):
        product_code (str):
        json_body (ProductRate): A ProductRate is used to map a product and its associated value
            commission

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        rate_id=rate_id,
        product_code=product_code,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
