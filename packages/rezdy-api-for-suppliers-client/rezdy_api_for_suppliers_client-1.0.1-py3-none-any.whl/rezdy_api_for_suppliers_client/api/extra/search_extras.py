from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_extra_list import ResponseExtraList
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    search_string: str,
) -> Dict[str, Any]:
    url = "{}/extra".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["searchString"] = search_string

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseExtraList]:
    if response.status_code == 200:
        response_200 = ResponseExtraList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseExtraList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    search_string: str,
) -> Response[ResponseExtraList]:
    """Search extra

     Searches extra. To retrieve all extras, omit the searchString parameter

    Args:
        search_string (str):

    Returns:
        Response[ResponseExtraList]
    """

    kwargs = _get_kwargs(
        client=client,
        search_string=search_string,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    search_string: str,
) -> Optional[ResponseExtraList]:
    """Search extra

     Searches extra. To retrieve all extras, omit the searchString parameter

    Args:
        search_string (str):

    Returns:
        Response[ResponseExtraList]
    """

    return sync_detailed(
        client=client,
        search_string=search_string,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    search_string: str,
) -> Response[ResponseExtraList]:
    """Search extra

     Searches extra. To retrieve all extras, omit the searchString parameter

    Args:
        search_string (str):

    Returns:
        Response[ResponseExtraList]
    """

    kwargs = _get_kwargs(
        client=client,
        search_string=search_string,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    search_string: str,
) -> Optional[ResponseExtraList]:
    """Search extra

     Searches extra. To retrieve all extras, omit the searchString parameter

    Args:
        search_string (str):

    Returns:
        Response[ResponseExtraList]
    """

    return (
        await asyncio_detailed(
            client=client,
            search_string=search_string,
        )
    ).parsed
