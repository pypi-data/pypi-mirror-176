from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_no_data import ResponseNoData
from ...types import Response


def _get_kwargs(
    product_code: str,
    start_time_local: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/availability/product/{productCode}/startTimeLocal/{startTimeLocal}".format(
        client.base_url, productCode=product_code, startTimeLocal=start_time_local
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
    product_code: str,
    start_time_local: str,
    *,
    client: Client,
) -> Response[ResponseNoData]:
    """Delete availability

     Delete a single session starting at a specific local date time

    Args:
        product_code (str):
        start_time_local (str):

    Returns:
        Response[ResponseNoData]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        start_time_local=start_time_local,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    product_code: str,
    start_time_local: str,
    *,
    client: Client,
) -> Optional[ResponseNoData]:
    """Delete availability

     Delete a single session starting at a specific local date time

    Args:
        product_code (str):
        start_time_local (str):

    Returns:
        Response[ResponseNoData]
    """

    return sync_detailed(
        product_code=product_code,
        start_time_local=start_time_local,
        client=client,
    ).parsed


async def asyncio_detailed(
    product_code: str,
    start_time_local: str,
    *,
    client: Client,
) -> Response[ResponseNoData]:
    """Delete availability

     Delete a single session starting at a specific local date time

    Args:
        product_code (str):
        start_time_local (str):

    Returns:
        Response[ResponseNoData]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        start_time_local=start_time_local,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    product_code: str,
    start_time_local: str,
    *,
    client: Client,
) -> Optional[ResponseNoData]:
    """Delete availability

     Delete a single session starting at a specific local date time

    Args:
        product_code (str):
        start_time_local (str):

    Returns:
        Response[ResponseNoData]
    """

    return (
        await asyncio_detailed(
            product_code=product_code,
            start_time_local=start_time_local,
            client=client,
        )
    ).parsed
