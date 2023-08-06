from typing import Any, Dict

import httpx

from ...client import Client
from ...models.session_update_batch_request import SessionUpdateBatchRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: SessionUpdateBatchRequest,
) -> Dict[str, Any]:
    url = "{}/availability/batch".format(client.base_url)

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


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: Client,
    json_body: SessionUpdateBatchRequest,
) -> Response[Any]:
    """Update availability batch

     Batch Update availability for a specific product and time period.
    This will update availability for all the sessions that start in that time range. <br>
    Product code is optional, all sessions for all products will be updated if it is empty.
    You can use this service to blackout periods (I.e. set availability to 0 for a full day).

    Maximum range is one week.

    This can only update sessions from products with InventoryMode = SESSION_SEATS.
    ```
    {
        startTime: 2014-11-11T00:00:00Z,
        endTime: 2014-11-11T23:59:59Z,
        productCode: P123456,
        seatsAvailable: 0
    }
    ```
    OR
    ```
    {
        startTime: 2014-11-11T00:00:00Z,
        endTime: 2014-11-11T23:59:59Z,
        productCode: P123456,
        seats: 30
    }
    ```
    OR
    ```
    {
        startTime: 2014-11-11T00:00:00Z,
        endTime: 2014-11-11T23:59:59Z,
        productCode: P123456,
        priceOptions: [
           {
             price: 90,
             label: Adult
           }
         ]
    }
    ```

    If you send `seatsAvailable`, sessions will be updated for the current availability to become this
    number. <br>

    If you send `seats`, the total seats capacity of sessions will be updated, regardless of how many
    are already booked. <br>

    If you send both, only `seatsAvailable` will be used. <br>
    If you send priceOptions, they will override the default price options of the existing session.

    Args:
        json_body (SessionUpdateBatchRequest): Batch update session request data.

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    *,
    client: Client,
    json_body: SessionUpdateBatchRequest,
) -> Response[Any]:
    """Update availability batch

     Batch Update availability for a specific product and time period.
    This will update availability for all the sessions that start in that time range. <br>
    Product code is optional, all sessions for all products will be updated if it is empty.
    You can use this service to blackout periods (I.e. set availability to 0 for a full day).

    Maximum range is one week.

    This can only update sessions from products with InventoryMode = SESSION_SEATS.
    ```
    {
        startTime: 2014-11-11T00:00:00Z,
        endTime: 2014-11-11T23:59:59Z,
        productCode: P123456,
        seatsAvailable: 0
    }
    ```
    OR
    ```
    {
        startTime: 2014-11-11T00:00:00Z,
        endTime: 2014-11-11T23:59:59Z,
        productCode: P123456,
        seats: 30
    }
    ```
    OR
    ```
    {
        startTime: 2014-11-11T00:00:00Z,
        endTime: 2014-11-11T23:59:59Z,
        productCode: P123456,
        priceOptions: [
           {
             price: 90,
             label: Adult
           }
         ]
    }
    ```

    If you send `seatsAvailable`, sessions will be updated for the current availability to become this
    number. <br>

    If you send `seats`, the total seats capacity of sessions will be updated, regardless of how many
    are already booked. <br>

    If you send both, only `seatsAvailable` will be used. <br>
    If you send priceOptions, they will override the default price options of the existing session.

    Args:
        json_body (SessionUpdateBatchRequest): Batch update session request data.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
