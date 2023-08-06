from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_voucher import ResponseVoucher
from ...types import Response


def _get_kwargs(
    voucher_code: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/vouchers/{voucherCode}".format(client.base_url, voucherCode=voucher_code)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseVoucher]:
    if response.status_code == 200:
        response_200 = ResponseVoucher.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseVoucher]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    voucher_code: str,
    *,
    client: Client,
) -> Response[ResponseVoucher]:
    """Get voucher

     Load an existing voucher by Voucher Code

    Args:
        voucher_code (str):

    Returns:
        Response[ResponseVoucher]
    """

    kwargs = _get_kwargs(
        voucher_code=voucher_code,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    voucher_code: str,
    *,
    client: Client,
) -> Optional[ResponseVoucher]:
    """Get voucher

     Load an existing voucher by Voucher Code

    Args:
        voucher_code (str):

    Returns:
        Response[ResponseVoucher]
    """

    return sync_detailed(
        voucher_code=voucher_code,
        client=client,
    ).parsed


async def asyncio_detailed(
    voucher_code: str,
    *,
    client: Client,
) -> Response[ResponseVoucher]:
    """Get voucher

     Load an existing voucher by Voucher Code

    Args:
        voucher_code (str):

    Returns:
        Response[ResponseVoucher]
    """

    kwargs = _get_kwargs(
        voucher_code=voucher_code,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    voucher_code: str,
    *,
    client: Client,
) -> Optional[ResponseVoucher]:
    """Get voucher

     Load an existing voucher by Voucher Code

    Args:
        voucher_code (str):

    Returns:
        Response[ResponseVoucher]
    """

    return (
        await asyncio_detailed(
            voucher_code=voucher_code,
            client=client,
        )
    ).parsed
