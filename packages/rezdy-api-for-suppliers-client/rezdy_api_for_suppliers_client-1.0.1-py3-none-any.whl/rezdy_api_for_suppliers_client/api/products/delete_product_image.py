from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response_no_data import ResponseNoData
from ...types import Response


def _get_kwargs(
    product_code: str,
    media_id: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/products/{productCode}/images/{mediaId}".format(
        client.base_url, productCode=product_code, mediaId=media_id
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
    media_id: int,
    *,
    client: Client,
) -> Response[ResponseNoData]:
    """Remove product Image

     Removes product Image. Filename is mandatory. It has to be specified either in the attachment, part
    of the form-data parameter 'file', or in the attachment, as a form-data parameter 'filename', which
    is common format for PHP frameworks, which are sending an array of attachments.

    Args:
        product_code (str):
        media_id (int):

    Returns:
        Response[ResponseNoData]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        media_id=media_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    product_code: str,
    media_id: int,
    *,
    client: Client,
) -> Optional[ResponseNoData]:
    """Remove product Image

     Removes product Image. Filename is mandatory. It has to be specified either in the attachment, part
    of the form-data parameter 'file', or in the attachment, as a form-data parameter 'filename', which
    is common format for PHP frameworks, which are sending an array of attachments.

    Args:
        product_code (str):
        media_id (int):

    Returns:
        Response[ResponseNoData]
    """

    return sync_detailed(
        product_code=product_code,
        media_id=media_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    product_code: str,
    media_id: int,
    *,
    client: Client,
) -> Response[ResponseNoData]:
    """Remove product Image

     Removes product Image. Filename is mandatory. It has to be specified either in the attachment, part
    of the form-data parameter 'file', or in the attachment, as a form-data parameter 'filename', which
    is common format for PHP frameworks, which are sending an array of attachments.

    Args:
        product_code (str):
        media_id (int):

    Returns:
        Response[ResponseNoData]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        media_id=media_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    product_code: str,
    media_id: int,
    *,
    client: Client,
) -> Optional[ResponseNoData]:
    """Remove product Image

     Removes product Image. Filename is mandatory. It has to be specified either in the attachment, part
    of the form-data parameter 'file', or in the attachment, as a form-data parameter 'filename', which
    is common format for PHP frameworks, which are sending an array of attachments.

    Args:
        product_code (str):
        media_id (int):

    Returns:
        Response[ResponseNoData]
    """

    return (
        await asyncio_detailed(
            product_code=product_code,
            media_id=media_id,
            client=client,
        )
    ).parsed
