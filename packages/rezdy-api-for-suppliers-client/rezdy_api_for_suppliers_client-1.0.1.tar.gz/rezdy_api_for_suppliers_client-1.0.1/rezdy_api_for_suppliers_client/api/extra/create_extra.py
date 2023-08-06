from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.extra_create_request import ExtraCreateRequest
from ...models.response_extra import ResponseExtra
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ExtraCreateRequest,
) -> Dict[str, Any]:
    url = "{}/extra".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[ResponseExtra]:
    if response.status_code == 200:
        response_200 = ResponseExtra.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseExtra]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ExtraCreateRequest,
) -> Response[ResponseExtra]:
    """Create extra

     Creates a new extra

    Args:
        json_body (ExtraCreateRequest): Partial optional service or item that can be purchased
            when booking a specific product

    Returns:
        Response[ResponseExtra]
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
    json_body: ExtraCreateRequest,
) -> Optional[ResponseExtra]:
    """Create extra

     Creates a new extra

    Args:
        json_body (ExtraCreateRequest): Partial optional service or item that can be purchased
            when booking a specific product

    Returns:
        Response[ResponseExtra]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ExtraCreateRequest,
) -> Response[ResponseExtra]:
    """Create extra

     Creates a new extra

    Args:
        json_body (ExtraCreateRequest): Partial optional service or item that can be purchased
            when booking a specific product

    Returns:
        Response[ResponseExtra]
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
    json_body: ExtraCreateRequest,
) -> Optional[ResponseExtra]:
    """Create extra

     Creates a new extra

    Args:
        json_body (ExtraCreateRequest): Partial optional service or item that can be purchased
            when booking a specific product

    Returns:
        Response[ResponseExtra]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
