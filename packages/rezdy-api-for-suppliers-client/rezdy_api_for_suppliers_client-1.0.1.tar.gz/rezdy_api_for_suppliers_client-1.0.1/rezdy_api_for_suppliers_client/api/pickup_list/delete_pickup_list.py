from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_no_data import ResponseNoData
from ...types import Response


def _get_kwargs(
    pickup_list_id: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/pickups/{pickupListId}".format(client.base_url, pickupListId=pickup_list_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseNoData]:
    if response.status_code == 200:
        response_200 = ResponseNoData.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseNoData]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    pickup_list_id: int,
    *,
    client: Client,
) -> Response[ResponseNoData]:
    """Delete pickup list

     Deletes a pickup list

    Args:
        pickup_list_id (int):

    Returns:
        Response[ResponseNoData]
    """

    kwargs = _get_kwargs(
        pickup_list_id=pickup_list_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    pickup_list_id: int,
    *,
    client: Client,
) -> Optional[ResponseNoData]:
    """Delete pickup list

     Deletes a pickup list

    Args:
        pickup_list_id (int):

    Returns:
        Response[ResponseNoData]
    """

    return sync_detailed(
        pickup_list_id=pickup_list_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    pickup_list_id: int,
    *,
    client: Client,
) -> Response[ResponseNoData]:
    """Delete pickup list

     Deletes a pickup list

    Args:
        pickup_list_id (int):

    Returns:
        Response[ResponseNoData]
    """

    kwargs = _get_kwargs(
        pickup_list_id=pickup_list_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    pickup_list_id: int,
    *,
    client: Client,
) -> Optional[ResponseNoData]:
    """Delete pickup list

     Deletes a pickup list

    Args:
        pickup_list_id (int):

    Returns:
        Response[ResponseNoData]
    """

    return (
        await asyncio_detailed(
            pickup_list_id=pickup_list_id,
            client=client,
        )
    ).parsed
