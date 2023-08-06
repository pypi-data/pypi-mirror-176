from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.response_booking_list import ResponseBookingList
from ...models.search_bookings_order_status import SearchBookingsOrderStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    order_status: Union[Unset, None, SearchBookingsOrderStatus] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    product_code: Union[Unset, None, List[str]] = UNSET,
    min_tour_start_time: Union[Unset, None, str] = UNSET,
    max_tour_start_time: Union[Unset, None, str] = UNSET,
    updated_since: Union[Unset, None, str] = UNSET,
    min_date_created: Union[Unset, None, str] = UNSET,
    max_date_created: Union[Unset, None, str] = UNSET,
    reseller_reference: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    url = "{}/bookings".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_order_status: Union[Unset, None, str] = UNSET
    if not isinstance(order_status, Unset):
        json_order_status = order_status.value if order_status else None

    params["orderStatus"] = json_order_status

    params["search"] = search

    json_product_code: Union[Unset, None, List[str]] = UNSET
    if not isinstance(product_code, Unset):
        if product_code is None:
            json_product_code = None
        else:
            json_product_code = product_code

    params["productCode"] = json_product_code

    params["minTourStartTime"] = min_tour_start_time

    params["maxTourStartTime"] = max_tour_start_time

    params["updatedSince"] = updated_since

    params["minDateCreated"] = min_date_created

    params["maxDateCreated"] = max_date_created

    params["resellerReference"] = reseller_reference

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseBookingList]:
    if response.status_code == 200:
        response_200 = ResponseBookingList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseBookingList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    order_status: Union[Unset, None, SearchBookingsOrderStatus] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    product_code: Union[Unset, None, List[str]] = UNSET,
    min_tour_start_time: Union[Unset, None, str] = UNSET,
    max_tour_start_time: Union[Unset, None, str] = UNSET,
    updated_since: Union[Unset, None, str] = UNSET,
    min_date_created: Union[Unset, None, str] = UNSET,
    max_date_created: Union[Unset, None, str] = UNSET,
    reseller_reference: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponseBookingList]:
    """Search bookings

     Search bookings in your account

    Args:
        order_status (Union[Unset, None, SearchBookingsOrderStatus]):
        search (Union[Unset, None, str]):
        product_code (Union[Unset, None, List[str]]):
        min_tour_start_time (Union[Unset, None, str]):
        max_tour_start_time (Union[Unset, None, str]):
        updated_since (Union[Unset, None, str]):
        min_date_created (Union[Unset, None, str]):
        max_date_created (Union[Unset, None, str]):
        reseller_reference (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseBookingList]
    """

    kwargs = _get_kwargs(
        client=client,
        order_status=order_status,
        search=search,
        product_code=product_code,
        min_tour_start_time=min_tour_start_time,
        max_tour_start_time=max_tour_start_time,
        updated_since=updated_since,
        min_date_created=min_date_created,
        max_date_created=max_date_created,
        reseller_reference=reseller_reference,
        limit=limit,
        offset=offset,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    order_status: Union[Unset, None, SearchBookingsOrderStatus] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    product_code: Union[Unset, None, List[str]] = UNSET,
    min_tour_start_time: Union[Unset, None, str] = UNSET,
    max_tour_start_time: Union[Unset, None, str] = UNSET,
    updated_since: Union[Unset, None, str] = UNSET,
    min_date_created: Union[Unset, None, str] = UNSET,
    max_date_created: Union[Unset, None, str] = UNSET,
    reseller_reference: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponseBookingList]:
    """Search bookings

     Search bookings in your account

    Args:
        order_status (Union[Unset, None, SearchBookingsOrderStatus]):
        search (Union[Unset, None, str]):
        product_code (Union[Unset, None, List[str]]):
        min_tour_start_time (Union[Unset, None, str]):
        max_tour_start_time (Union[Unset, None, str]):
        updated_since (Union[Unset, None, str]):
        min_date_created (Union[Unset, None, str]):
        max_date_created (Union[Unset, None, str]):
        reseller_reference (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseBookingList]
    """

    return sync_detailed(
        client=client,
        order_status=order_status,
        search=search,
        product_code=product_code,
        min_tour_start_time=min_tour_start_time,
        max_tour_start_time=max_tour_start_time,
        updated_since=updated_since,
        min_date_created=min_date_created,
        max_date_created=max_date_created,
        reseller_reference=reseller_reference,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    order_status: Union[Unset, None, SearchBookingsOrderStatus] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    product_code: Union[Unset, None, List[str]] = UNSET,
    min_tour_start_time: Union[Unset, None, str] = UNSET,
    max_tour_start_time: Union[Unset, None, str] = UNSET,
    updated_since: Union[Unset, None, str] = UNSET,
    min_date_created: Union[Unset, None, str] = UNSET,
    max_date_created: Union[Unset, None, str] = UNSET,
    reseller_reference: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponseBookingList]:
    """Search bookings

     Search bookings in your account

    Args:
        order_status (Union[Unset, None, SearchBookingsOrderStatus]):
        search (Union[Unset, None, str]):
        product_code (Union[Unset, None, List[str]]):
        min_tour_start_time (Union[Unset, None, str]):
        max_tour_start_time (Union[Unset, None, str]):
        updated_since (Union[Unset, None, str]):
        min_date_created (Union[Unset, None, str]):
        max_date_created (Union[Unset, None, str]):
        reseller_reference (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseBookingList]
    """

    kwargs = _get_kwargs(
        client=client,
        order_status=order_status,
        search=search,
        product_code=product_code,
        min_tour_start_time=min_tour_start_time,
        max_tour_start_time=max_tour_start_time,
        updated_since=updated_since,
        min_date_created=min_date_created,
        max_date_created=max_date_created,
        reseller_reference=reseller_reference,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    order_status: Union[Unset, None, SearchBookingsOrderStatus] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    product_code: Union[Unset, None, List[str]] = UNSET,
    min_tour_start_time: Union[Unset, None, str] = UNSET,
    max_tour_start_time: Union[Unset, None, str] = UNSET,
    updated_since: Union[Unset, None, str] = UNSET,
    min_date_created: Union[Unset, None, str] = UNSET,
    max_date_created: Union[Unset, None, str] = UNSET,
    reseller_reference: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponseBookingList]:
    """Search bookings

     Search bookings in your account

    Args:
        order_status (Union[Unset, None, SearchBookingsOrderStatus]):
        search (Union[Unset, None, str]):
        product_code (Union[Unset, None, List[str]]):
        min_tour_start_time (Union[Unset, None, str]):
        max_tour_start_time (Union[Unset, None, str]):
        updated_since (Union[Unset, None, str]):
        min_date_created (Union[Unset, None, str]):
        max_date_created (Union[Unset, None, str]):
        reseller_reference (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseBookingList]
    """

    return (
        await asyncio_detailed(
            client=client,
            order_status=order_status,
            search=search,
            product_code=product_code,
            min_tour_start_time=min_tour_start_time,
            max_tour_start_time=max_tour_start_time,
            updated_since=updated_since,
            min_date_created=min_date_created,
            max_date_created=max_date_created,
            reseller_reference=reseller_reference,
            limit=limit,
            offset=offset,
        )
    ).parsed
