from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_resource import ResponseResource
from ...types import Response


def _get_kwargs(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/resources/{resourceId}/session/{sessionId}".format(
        client.base_url, resourceId=resource_id, sessionId=session_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
) -> Response[ResponseResource]:
    """Remove session resource

     Removes the resource from the session.

    Args:
        resource_id (int):
        session_id (int):

    Returns:
        Response[ResponseResource]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        session_id=session_id,
        client=client,
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
) -> Optional[ResponseResource]:
    """Remove session resource

     Removes the resource from the session.

    Args:
        resource_id (int):
        session_id (int):

    Returns:
        Response[ResponseResource]
    """

    return sync_detailed(
        resource_id=resource_id,
        session_id=session_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
) -> Response[ResponseResource]:
    """Remove session resource

     Removes the resource from the session.

    Args:
        resource_id (int):
        session_id (int):

    Returns:
        Response[ResponseResource]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        session_id=session_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    resource_id: int,
    session_id: int,
    *,
    client: Client,
) -> Optional[ResponseResource]:
    """Remove session resource

     Removes the resource from the session.

    Args:
        resource_id (int):
        session_id (int):

    Returns:
        Response[ResponseResource]
    """

    return (
        await asyncio_detailed(
            resource_id=resource_id,
            session_id=session_id,
            client=client,
        )
    ).parsed
