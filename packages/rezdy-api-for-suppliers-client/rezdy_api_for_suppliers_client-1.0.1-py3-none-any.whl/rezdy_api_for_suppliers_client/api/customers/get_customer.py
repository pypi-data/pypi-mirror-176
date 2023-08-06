from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_customer import ResponseCustomer
from ...types import Response


def _get_kwargs(
    customer_id: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/customers/{customerId}".format(client.base_url, customerId=customer_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseCustomer]:
    if response.status_code == 200:
        response_200 = ResponseCustomer.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseCustomer]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    customer_id: int,
    *,
    client: Client,
) -> Response[ResponseCustomer]:
    """Get customer

     Load an existing customer by Id

    Args:
        customer_id (int):

    Returns:
        Response[ResponseCustomer]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    customer_id: int,
    *,
    client: Client,
) -> Optional[ResponseCustomer]:
    """Get customer

     Load an existing customer by Id

    Args:
        customer_id (int):

    Returns:
        Response[ResponseCustomer]
    """

    return sync_detailed(
        customer_id=customer_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    customer_id: int,
    *,
    client: Client,
) -> Response[ResponseCustomer]:
    """Get customer

     Load an existing customer by Id

    Args:
        customer_id (int):

    Returns:
        Response[ResponseCustomer]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    customer_id: int,
    *,
    client: Client,
) -> Optional[ResponseCustomer]:
    """Get customer

     Load an existing customer by Id

    Args:
        customer_id (int):

    Returns:
        Response[ResponseCustomer]
    """

    return (
        await asyncio_detailed(
            customer_id=customer_id,
            client=client,
        )
    ).parsed
