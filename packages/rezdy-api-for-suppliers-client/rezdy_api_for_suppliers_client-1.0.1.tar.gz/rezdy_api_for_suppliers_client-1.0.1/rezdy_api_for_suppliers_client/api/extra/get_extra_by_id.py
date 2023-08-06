from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_extra import ResponseExtra
from ...types import Response


def _get_kwargs(
    extra_id: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/extra/{extraId}".format(client.base_url, extraId=extra_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    extra_id: int,
    *,
    client: Client,
) -> Response[ResponseExtra]:
    """Retrieve an extra

     Retrieve an extra by Id

    Args:
        extra_id (int):

    Returns:
        Response[ResponseExtra]
    """

    kwargs = _get_kwargs(
        extra_id=extra_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    extra_id: int,
    *,
    client: Client,
) -> Optional[ResponseExtra]:
    """Retrieve an extra

     Retrieve an extra by Id

    Args:
        extra_id (int):

    Returns:
        Response[ResponseExtra]
    """

    return sync_detailed(
        extra_id=extra_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    extra_id: int,
    *,
    client: Client,
) -> Response[ResponseExtra]:
    """Retrieve an extra

     Retrieve an extra by Id

    Args:
        extra_id (int):

    Returns:
        Response[ResponseExtra]
    """

    kwargs = _get_kwargs(
        extra_id=extra_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    extra_id: int,
    *,
    client: Client,
) -> Optional[ResponseExtra]:
    """Retrieve an extra

     Retrieve an extra by Id

    Args:
        extra_id (int):

    Returns:
        Response[ResponseExtra]
    """

    return (
        await asyncio_detailed(
            extra_id=extra_id,
            client=client,
        )
    ).parsed
