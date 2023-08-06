from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.response_resource import ResponseResource
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


def _parse_response(*, response: httpx.Response) -> Optional[ResponseResource]:
    if response.status_code == 200:
        response_200 = ResponseResource.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseResource]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
    resource_order: Union[Unset, None, int] = UNSET,
) -> Response[ResponseResource]:
    """Add session resource

     Add the resource to the session.

    Args:
        resource_id (int):
        session_id (int):
        resource_order (Union[Unset, None, int]):

    Returns:
        Response[ResponseResource]
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


def sync(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
    resource_order: Union[Unset, None, int] = UNSET,
) -> Optional[ResponseResource]:
    """Add session resource

     Add the resource to the session.

    Args:
        resource_id (int):
        session_id (int):
        resource_order (Union[Unset, None, int]):

    Returns:
        Response[ResponseResource]
    """

    return sync_detailed(
        resource_id=resource_id,
        session_id=session_id,
        client=client,
        resource_order=resource_order,
    ).parsed


async def asyncio_detailed(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
    resource_order: Union[Unset, None, int] = UNSET,
) -> Response[ResponseResource]:
    """Add session resource

     Add the resource to the session.

    Args:
        resource_id (int):
        session_id (int):
        resource_order (Union[Unset, None, int]):

    Returns:
        Response[ResponseResource]
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


async def asyncio(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
    resource_order: Union[Unset, None, int] = UNSET,
) -> Optional[ResponseResource]:
    """Add session resource

     Add the resource to the session.

    Args:
        resource_id (int):
        session_id (int):
        resource_order (Union[Unset, None, int]):

    Returns:
        Response[ResponseResource]
    """

    return (
        await asyncio_detailed(
            resource_id=resource_id,
            session_id=session_id,
            client=client,
            resource_order=resource_order,
        )
    ).parsed
