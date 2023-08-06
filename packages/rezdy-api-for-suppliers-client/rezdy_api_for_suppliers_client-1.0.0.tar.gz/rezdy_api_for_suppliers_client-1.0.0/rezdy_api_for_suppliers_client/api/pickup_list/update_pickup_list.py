from typing import Any, Dict

import httpx

from ...client import Client
from ...models.pickup_list import PickupList
from ...types import Response


def _get_kwargs(
    pickup_list_id: int,
    *,
    client: Client,
    json_body: PickupList,
) -> Dict[str, Any]:
    url = "{}/pickups/{pickupListId}".format(client.base_url, pickupListId=pickup_list_id)

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
    pickup_list_id: int,
    *,
    client: Client,
    json_body: PickupList,
) -> Response[Any]:
    """Update pickup list

     Updates a pickup list. This service should not be used for partial updates. A full pickup list
    object with the desired pick up locations should be passed as input

    Args:
        pickup_list_id (int):
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        pickup_list_id=pickup_list_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    pickup_list_id: int,
    *,
    client: Client,
    json_body: PickupList,
) -> Response[Any]:
    """Update pickup list

     Updates a pickup list. This service should not be used for partial updates. A full pickup list
    object with the desired pick up locations should be passed as input

    Args:
        pickup_list_id (int):
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        pickup_list_id=pickup_list_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
