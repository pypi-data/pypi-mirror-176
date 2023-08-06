from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
    resource_order: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/resources/{resourceId}/session/{sessionId}".format(
        client.base_url, resourceId=resource_id, sessionId=session_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["resourceOrder"] = resource_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
    resource_order: Union[Unset, None, int] = UNSET,
) -> Response[Any]:
    """Add session resource

     Add the resource to the session.

    Args:
        resource_id (int):
        session_id (int):
        resource_order (Union[Unset, None, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        session_id=session_id,
        client=client,
        resource_order=resource_order,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
    resource_order: Union[Unset, None, int] = UNSET,
) -> Response[Any]:
    """Add session resource

     Add the resource to the session.

    Args:
        resource_id (int):
        session_id (int):
        resource_order (Union[Unset, None, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        session_id=session_id,
        client=client,
        resource_order=resource_order,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
