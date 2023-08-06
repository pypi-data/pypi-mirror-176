from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    rate_name: Union[Unset, None, str] = UNSET,
    product_code: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rates/search".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["rateName"] = rate_name

    params["productCode"] = product_code

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    rate_name: Union[Unset, None, str] = UNSET,
    product_code: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Search rates

     Searches rates based on rate name and product code. If rateName and productCode are not specified,
    then it will return all rates belonging to the supplier

    Args:
        rate_name (Union[Unset, None, str]):
        product_code (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        rate_name=rate_name,
        product_code=product_code,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    rate_name: Union[Unset, None, str] = UNSET,
    product_code: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Search rates

     Searches rates based on rate name and product code. If rateName and productCode are not specified,
    then it will return all rates belonging to the supplier

    Args:
        rate_name (Union[Unset, None, str]):
        product_code (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        rate_name=rate_name,
        product_code=product_code,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
