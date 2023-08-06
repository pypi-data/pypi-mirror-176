from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_company import ResponseCompany
from ...types import Response


def _get_kwargs(
    company_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/companies/name/{companyName}".format(client.base_url, companyName=company_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseCompany]:
    if response.status_code == 200:
        response_200 = ResponseCompany.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseCompany]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    company_name: str,
    *,
    client: Client,
) -> Response[ResponseCompany]:
    """Get company by name

     Load an existing Company by it's name in Rezdy. Company name must be given in full name.

    Args:
        company_name (str):

    Returns:
        Response[ResponseCompany]
    """

    kwargs = _get_kwargs(
        company_name=company_name,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    company_name: str,
    *,
    client: Client,
) -> Optional[ResponseCompany]:
    """Get company by name

     Load an existing Company by it's name in Rezdy. Company name must be given in full name.

    Args:
        company_name (str):

    Returns:
        Response[ResponseCompany]
    """

    return sync_detailed(
        company_name=company_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    company_name: str,
    *,
    client: Client,
) -> Response[ResponseCompany]:
    """Get company by name

     Load an existing Company by it's name in Rezdy. Company name must be given in full name.

    Args:
        company_name (str):

    Returns:
        Response[ResponseCompany]
    """

    kwargs = _get_kwargs(
        company_name=company_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    company_name: str,
    *,
    client: Client,
) -> Optional[ResponseCompany]:
    """Get company by name

     Load an existing Company by it's name in Rezdy. Company name must be given in full name.

    Args:
        company_name (str):

    Returns:
        Response[ResponseCompany]
    """

    return (
        await asyncio_detailed(
            company_name=company_name,
            client=client,
        )
    ).parsed
