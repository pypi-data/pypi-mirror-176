from typing import Any, Dict

import httpx

from ...client import Client
from ...models.session_update_request import SessionUpdateRequest
from ...types import Response


def _get_kwargs(
    product_code: str,
    start_time_local: str,
    *,
    client: Client,
    json_body: SessionUpdateRequest,
) -> Dict[str, Any]:
    url = "{}/availability/product/{productCode}/startTimeLocal/{startTimeLocal}".format(
        client.base_url, productCode=product_code, startTimeLocal=start_time_local
    )

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
    product_code: str,
    start_time_local: str,
    *,
    client: Client,
    json_body: SessionUpdateRequest,
) -> Response[Any]:
    """Update availability

     Update availability a session starting at a specific local date time

    Args:
        product_code (str):
        start_time_local (str):
        json_body (SessionUpdateRequest): Updates session request data.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        start_time_local=start_time_local,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    product_code: str,
    start_time_local: str,
    *,
    client: Client,
    json_body: SessionUpdateRequest,
) -> Response[Any]:
    """Update availability

     Update availability a session starting at a specific local date time

    Args:
        product_code (str):
        start_time_local (str):
        json_body (SessionUpdateRequest): Updates session request data.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        start_time_local=start_time_local,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
