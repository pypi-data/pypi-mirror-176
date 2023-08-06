from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.response_session_list import ResponseSessionList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    product_code: List[str],
    start_time: Union[Unset, None, str] = UNSET,
    end_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    end_time_local: Union[Unset, None, str] = UNSET,
    min_availability: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    url = "{}/availability".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_product_code = product_code

    params["productCode"] = json_product_code

    params["startTime"] = start_time

    params["endTime"] = end_time

    params["startTimeLocal"] = start_time_local

    params["endTimeLocal"] = end_time_local

    params["minAvailability"] = min_availability

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


def _parse_response(*, response: httpx.Response) -> Optional[ResponseSessionList]:
    if response.status_code == 200:
        response_200 = ResponseSessionList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseSessionList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    product_code: List[str],
    start_time: Union[Unset, None, str] = UNSET,
    end_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    end_time_local: Union[Unset, None, str] = UNSET,
    min_availability: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponseSessionList]:
    """Search availability

     This service returns availability information for a specific date range. The service response
    contains a list of sessions, including their availability and pricing details.<br>
    <p>Pricing in the session can be different than the pricing of the products, in a case of a dynamic
    pricing when a supplier overrides a price for a specific session or a ticket type.</p>
    <p>In case of multiple products sharing this session, a session will contain price overrides for all
    of the shared products. Therefore it is necessary to filer only the price options matching the
    chosen product code on the client side, when displaying available price options to a customer.</p>

    Args:
        product_code (List[str]):
        start_time (Union[Unset, None, str]):
        end_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        end_time_local (Union[Unset, None, str]):
        min_availability (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseSessionList]
    """

    kwargs = _get_kwargs(
        client=client,
        product_code=product_code,
        start_time=start_time,
        end_time=end_time,
        start_time_local=start_time_local,
        end_time_local=end_time_local,
        min_availability=min_availability,
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
    product_code: List[str],
    start_time: Union[Unset, None, str] = UNSET,
    end_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    end_time_local: Union[Unset, None, str] = UNSET,
    min_availability: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponseSessionList]:
    """Search availability

     This service returns availability information for a specific date range. The service response
    contains a list of sessions, including their availability and pricing details.<br>
    <p>Pricing in the session can be different than the pricing of the products, in a case of a dynamic
    pricing when a supplier overrides a price for a specific session or a ticket type.</p>
    <p>In case of multiple products sharing this session, a session will contain price overrides for all
    of the shared products. Therefore it is necessary to filer only the price options matching the
    chosen product code on the client side, when displaying available price options to a customer.</p>

    Args:
        product_code (List[str]):
        start_time (Union[Unset, None, str]):
        end_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        end_time_local (Union[Unset, None, str]):
        min_availability (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseSessionList]
    """

    return sync_detailed(
        client=client,
        product_code=product_code,
        start_time=start_time,
        end_time=end_time,
        start_time_local=start_time_local,
        end_time_local=end_time_local,
        min_availability=min_availability,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    product_code: List[str],
    start_time: Union[Unset, None, str] = UNSET,
    end_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    end_time_local: Union[Unset, None, str] = UNSET,
    min_availability: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Response[ResponseSessionList]:
    """Search availability

     This service returns availability information for a specific date range. The service response
    contains a list of sessions, including their availability and pricing details.<br>
    <p>Pricing in the session can be different than the pricing of the products, in a case of a dynamic
    pricing when a supplier overrides a price for a specific session or a ticket type.</p>
    <p>In case of multiple products sharing this session, a session will contain price overrides for all
    of the shared products. Therefore it is necessary to filer only the price options matching the
    chosen product code on the client side, when displaying available price options to a customer.</p>

    Args:
        product_code (List[str]):
        start_time (Union[Unset, None, str]):
        end_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        end_time_local (Union[Unset, None, str]):
        min_availability (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseSessionList]
    """

    kwargs = _get_kwargs(
        client=client,
        product_code=product_code,
        start_time=start_time,
        end_time=end_time,
        start_time_local=start_time_local,
        end_time_local=end_time_local,
        min_availability=min_availability,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    product_code: List[str],
    start_time: Union[Unset, None, str] = UNSET,
    end_time: Union[Unset, None, str] = UNSET,
    start_time_local: Union[Unset, None, str] = UNSET,
    end_time_local: Union[Unset, None, str] = UNSET,
    min_availability: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
) -> Optional[ResponseSessionList]:
    """Search availability

     This service returns availability information for a specific date range. The service response
    contains a list of sessions, including their availability and pricing details.<br>
    <p>Pricing in the session can be different than the pricing of the products, in a case of a dynamic
    pricing when a supplier overrides a price for a specific session or a ticket type.</p>
    <p>In case of multiple products sharing this session, a session will contain price overrides for all
    of the shared products. Therefore it is necessary to filer only the price options matching the
    chosen product code on the client side, when displaying available price options to a customer.</p>

    Args:
        product_code (List[str]):
        start_time (Union[Unset, None, str]):
        end_time (Union[Unset, None, str]):
        start_time_local (Union[Unset, None, str]):
        end_time_local (Union[Unset, None, str]):
        min_availability (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):

    Returns:
        Response[ResponseSessionList]
    """

    return (
        await asyncio_detailed(
            client=client,
            product_code=product_code,
            start_time=start_time,
            end_time=end_time,
            start_time_local=start_time_local,
            end_time_local=end_time_local,
            min_availability=min_availability,
            limit=limit,
            offset=offset,
        )
    ).parsed
