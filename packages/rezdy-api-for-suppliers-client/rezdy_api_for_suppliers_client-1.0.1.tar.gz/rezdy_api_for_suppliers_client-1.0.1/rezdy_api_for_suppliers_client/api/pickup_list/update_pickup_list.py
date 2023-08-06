from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.pickup_list import PickupList
from ...models.response_pickup_list import ResponsePickupList
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


def _parse_response(*, response: httpx.Response) -> Optional[ResponsePickupList]:
    if response.status_code == 200:
        response_200 = ResponsePickupList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponsePickupList]:
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
    json_body: PickupList,
) -> Response[ResponsePickupList]:
    """Update pickup list

     Updates a pickup list. This service should not be used for partial updates. A full pickup list
    object with the desired pick up locations should be passed as input

    Args:
        pickup_list_id (int):
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[ResponsePickupList]
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


def sync(
    pickup_list_id: int,
    *,
    client: Client,
    json_body: PickupList,
) -> Optional[ResponsePickupList]:
    """Update pickup list

     Updates a pickup list. This service should not be used for partial updates. A full pickup list
    object with the desired pick up locations should be passed as input

    Args:
        pickup_list_id (int):
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[ResponsePickupList]
    """

    return sync_detailed(
        pickup_list_id=pickup_list_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    pickup_list_id: int,
    *,
    client: Client,
    json_body: PickupList,
) -> Response[ResponsePickupList]:
    """Update pickup list

     Updates a pickup list. This service should not be used for partial updates. A full pickup list
    object with the desired pick up locations should be passed as input

    Args:
        pickup_list_id (int):
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[ResponsePickupList]
    """

    kwargs = _get_kwargs(
        pickup_list_id=pickup_list_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    pickup_list_id: int,
    *,
    client: Client,
    json_body: PickupList,
) -> Optional[ResponsePickupList]:
    """Update pickup list

     Updates a pickup list. This service should not be used for partial updates. A full pickup list
    object with the desired pick up locations should be passed as input

    Args:
        pickup_list_id (int):
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[ResponsePickupList]
    """

    return (
        await asyncio_detailed(
            pickup_list_id=pickup_list_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
