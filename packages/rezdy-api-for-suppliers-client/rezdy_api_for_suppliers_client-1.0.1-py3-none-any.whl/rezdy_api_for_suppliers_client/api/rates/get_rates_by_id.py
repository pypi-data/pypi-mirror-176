from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_rate import ResponseRate
from ...types import Response


def _get_kwargs(
    rate_id: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/rates/{rateId}".format(client.base_url, rateId=rate_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
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
    rate_id: int,
    *,
    client: Client,
) -> Response[ResponseRate]:
    """Get rate

     Retrieves a rate based on its ID

    Args:
        rate_id (int):

    Returns:
        Response[ResponseRate]
    """

    kwargs = _get_kwargs(
        rate_id=rate_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    rate_id: int,
    *,
    client: Client,
) -> Optional[ResponseRate]:
    """Get rate

     Retrieves a rate based on its ID

    Args:
        rate_id (int):

    Returns:
        Response[ResponseRate]
    """

    return sync_detailed(
        rate_id=rate_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    rate_id: int,
    *,
    client: Client,
) -> Response[ResponseRate]:
    """Get rate

     Retrieves a rate based on its ID

    Args:
        rate_id (int):

    Returns:
        Response[ResponseRate]
    """

    kwargs = _get_kwargs(
        rate_id=rate_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    rate_id: int,
    *,
    client: Client,
) -> Optional[ResponseRate]:
    """Get rate

     Retrieves a rate based on its ID

    Args:
        rate_id (int):

    Returns:
        Response[ResponseRate]
    """

    return (
        await asyncio_detailed(
            rate_id=rate_id,
            client=client,
        )
    ).parsed
