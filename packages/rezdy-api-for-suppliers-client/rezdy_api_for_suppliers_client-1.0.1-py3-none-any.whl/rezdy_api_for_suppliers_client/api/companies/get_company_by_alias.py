from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_company import ResponseCompany
from ...types import Response


def _get_kwargs(
    company_alias: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/companies/alias/{companyAlias}".format(client.base_url, companyAlias=company_alias)

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
    company_alias: str,
    *,
    client: Client,
) -> Response[ResponseCompany]:
    """Get company by alias

     Load an existing Company by it's alias in Rezdy. Company alias is not a permanent identifier and can
    change over time.

    Args:
        company_alias (str):

    Returns:
        Response[ResponseCompany]
    """

    kwargs = _get_kwargs(
        company_alias=company_alias,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    company_alias: str,
    *,
    client: Client,
) -> Optional[ResponseCompany]:
    """Get company by alias

     Load an existing Company by it's alias in Rezdy. Company alias is not a permanent identifier and can
    change over time.

    Args:
        company_alias (str):

    Returns:
        Response[ResponseCompany]
    """

    return sync_detailed(
        company_alias=company_alias,
        client=client,
    ).parsed


async def asyncio_detailed(
    company_alias: str,
    *,
    client: Client,
) -> Response[ResponseCompany]:
    """Get company by alias

     Load an existing Company by it's alias in Rezdy. Company alias is not a permanent identifier and can
    change over time.

    Args:
        company_alias (str):

    Returns:
        Response[ResponseCompany]
    """

    kwargs = _get_kwargs(
        company_alias=company_alias,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    company_alias: str,
    *,
    client: Client,
) -> Optional[ResponseCompany]:
    """Get company by alias

     Load an existing Company by it's alias in Rezdy. Company alias is not a permanent identifier and can
    change over time.

    Args:
        company_alias (str):

    Returns:
        Response[ResponseCompany]
    """

    return (
        await asyncio_detailed(
            company_alias=company_alias,
            client=client,
        )
    ).parsed
