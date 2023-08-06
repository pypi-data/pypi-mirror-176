from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.pickup_list import PickupList
from ...models.response_pickup_list import ResponsePickupList
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: PickupList,
) -> Dict[str, Any]:
    url = "{}/pickups".format(client.base_url)

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
    *,
    client: Client,
    json_body: PickupList,
) -> Response[ResponsePickupList]:
    """Create pickup list

     Creates a new pickup list

    Args:
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[ResponsePickupList]
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
    json_body: PickupList,
) -> Optional[ResponsePickupList]:
    """Create pickup list

     Creates a new pickup list

    Args:
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[ResponsePickupList]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: PickupList,
) -> Response[ResponsePickupList]:
    """Create pickup list

     Creates a new pickup list

    Args:
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[ResponsePickupList]
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
    json_body: PickupList,
) -> Optional[ResponsePickupList]:
    """Create pickup list

     Creates a new pickup list

    Args:
        json_body (PickupList): PickupList object. Contains a list of pickup locations.

    Returns:
        Response[ResponsePickupList]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
