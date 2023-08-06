from typing import Any, Dict

import httpx

from ...client import Client
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


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    product_code: str,
    media_id: int,
    *,
    client: Client,
) -> Response[Any]:
    """Remove product Image

     Removes product Image. Filename is mandatory. It has to be specified either in the attachment, part
    of the form-data parameter 'file', or in the attachment, as a form-data parameter 'filename', which
    is common format for PHP frameworks, which are sending an array of attachments.

    Args:
        product_code (str):
        media_id (int):

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    product_code: str,
    media_id: int,
    *,
    client: Client,
) -> Response[Any]:
    """Remove product Image

     Removes product Image. Filename is mandatory. It has to be specified either in the attachment, part
    of the form-data parameter 'file', or in the attachment, as a form-data parameter 'filename', which
    is common format for PHP frameworks, which are sending an array of attachments.

    Args:
        product_code (str):
        media_id (int):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        media_id=media_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
