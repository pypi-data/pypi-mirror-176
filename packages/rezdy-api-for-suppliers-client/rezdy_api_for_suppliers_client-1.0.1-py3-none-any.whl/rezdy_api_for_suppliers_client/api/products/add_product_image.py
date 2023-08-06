from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.add_product_image_multipart_data import AddProductImageMultipartData
from ...models.response_image import ResponseImage
from ...types import Response


def _get_kwargs(
    product_code: str,
    *,
    client: Client,
    multipart_data: AddProductImageMultipartData,
) -> Dict[str, Any]:
    url = "{}/products/{productCode}/images".format(client.base_url, productCode=product_code)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseImage]:
    if response.status_code == 200:
        response_200 = ResponseImage.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseImage]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    product_code: str,
    *,
    client: Client,
    multipart_data: AddProductImageMultipartData,
) -> Response[ResponseImage]:
    """Add product image

     First, a product has to be created using```POST /products```, the response contain a product object
    upon a successful creation. Use the product code to for the add/delete images URLs.

    Use a standard file upload request (multipart form data) with a file attachment, parameter name is
    `file` as the call payload, and also a mandatory filename. If you have multiple images, you need to
    make one separate call for each image.

    A successful response contains generated image URLs including different image dimension and the
    image Id. Use the image Id to delete the image, if you want to remove it from the product.

    ### Request example

    File has to be specified either in the attachment, part of the form-data parameter 'file', or in the
    attachment, as a form-data parameter 'filename', which is common format for PHP frameworks, which
    are sending an array of attachments.

    Request:
    ```
    POST https://api.rezdy.com/latest/products/P12345/images?apiKey=123456789XYZ
    ```
    content-type=[multipart/form-data; boundary=----WebKitFormBoundarymDtt4W0lhmAsKFkZ]

    ```
    ------WebKitFormBoundarymDtt4W0lhmAsKFkZ
    Content-Disposition: form-data; name=\"file\"; filename=\"myImage.png\"
    Content-Type: image/png
    ...
    IMAGE BINARY DATA
    ...
    ------WebKitFormBoundarymDtt4W0lhmAsKFkZ--
    ```


    Args:
        product_code (str):
        multipart_data (AddProductImageMultipartData):

    Returns:
        Response[ResponseImage]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        client=client,
        multipart_data=multipart_data,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    product_code: str,
    *,
    client: Client,
    multipart_data: AddProductImageMultipartData,
) -> Optional[ResponseImage]:
    """Add product image

     First, a product has to be created using```POST /products```, the response contain a product object
    upon a successful creation. Use the product code to for the add/delete images URLs.

    Use a standard file upload request (multipart form data) with a file attachment, parameter name is
    `file` as the call payload, and also a mandatory filename. If you have multiple images, you need to
    make one separate call for each image.

    A successful response contains generated image URLs including different image dimension and the
    image Id. Use the image Id to delete the image, if you want to remove it from the product.

    ### Request example

    File has to be specified either in the attachment, part of the form-data parameter 'file', or in the
    attachment, as a form-data parameter 'filename', which is common format for PHP frameworks, which
    are sending an array of attachments.

    Request:
    ```
    POST https://api.rezdy.com/latest/products/P12345/images?apiKey=123456789XYZ
    ```
    content-type=[multipart/form-data; boundary=----WebKitFormBoundarymDtt4W0lhmAsKFkZ]

    ```
    ------WebKitFormBoundarymDtt4W0lhmAsKFkZ
    Content-Disposition: form-data; name=\"file\"; filename=\"myImage.png\"
    Content-Type: image/png
    ...
    IMAGE BINARY DATA
    ...
    ------WebKitFormBoundarymDtt4W0lhmAsKFkZ--
    ```


    Args:
        product_code (str):
        multipart_data (AddProductImageMultipartData):

    Returns:
        Response[ResponseImage]
    """

    return sync_detailed(
        product_code=product_code,
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    product_code: str,
    *,
    client: Client,
    multipart_data: AddProductImageMultipartData,
) -> Response[ResponseImage]:
    """Add product image

     First, a product has to be created using```POST /products```, the response contain a product object
    upon a successful creation. Use the product code to for the add/delete images URLs.

    Use a standard file upload request (multipart form data) with a file attachment, parameter name is
    `file` as the call payload, and also a mandatory filename. If you have multiple images, you need to
    make one separate call for each image.

    A successful response contains generated image URLs including different image dimension and the
    image Id. Use the image Id to delete the image, if you want to remove it from the product.

    ### Request example

    File has to be specified either in the attachment, part of the form-data parameter 'file', or in the
    attachment, as a form-data parameter 'filename', which is common format for PHP frameworks, which
    are sending an array of attachments.

    Request:
    ```
    POST https://api.rezdy.com/latest/products/P12345/images?apiKey=123456789XYZ
    ```
    content-type=[multipart/form-data; boundary=----WebKitFormBoundarymDtt4W0lhmAsKFkZ]

    ```
    ------WebKitFormBoundarymDtt4W0lhmAsKFkZ
    Content-Disposition: form-data; name=\"file\"; filename=\"myImage.png\"
    Content-Type: image/png
    ...
    IMAGE BINARY DATA
    ...
    ------WebKitFormBoundarymDtt4W0lhmAsKFkZ--
    ```


    Args:
        product_code (str):
        multipart_data (AddProductImageMultipartData):

    Returns:
        Response[ResponseImage]
    """

    kwargs = _get_kwargs(
        product_code=product_code,
        client=client,
        multipart_data=multipart_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    product_code: str,
    *,
    client: Client,
    multipart_data: AddProductImageMultipartData,
) -> Optional[ResponseImage]:
    """Add product image

     First, a product has to be created using```POST /products```, the response contain a product object
    upon a successful creation. Use the product code to for the add/delete images URLs.

    Use a standard file upload request (multipart form data) with a file attachment, parameter name is
    `file` as the call payload, and also a mandatory filename. If you have multiple images, you need to
    make one separate call for each image.

    A successful response contains generated image URLs including different image dimension and the
    image Id. Use the image Id to delete the image, if you want to remove it from the product.

    ### Request example

    File has to be specified either in the attachment, part of the form-data parameter 'file', or in the
    attachment, as a form-data parameter 'filename', which is common format for PHP frameworks, which
    are sending an array of attachments.

    Request:
    ```
    POST https://api.rezdy.com/latest/products/P12345/images?apiKey=123456789XYZ
    ```
    content-type=[multipart/form-data; boundary=----WebKitFormBoundarymDtt4W0lhmAsKFkZ]

    ```
    ------WebKitFormBoundarymDtt4W0lhmAsKFkZ
    Content-Disposition: form-data; name=\"file\"; filename=\"myImage.png\"
    Content-Type: image/png
    ...
    IMAGE BINARY DATA
    ...
    ------WebKitFormBoundarymDtt4W0lhmAsKFkZ--
    ```


    Args:
        product_code (str):
        multipart_data (AddProductImageMultipartData):

    Returns:
        Response[ResponseImage]
    """

    return (
        await asyncio_detailed(
            product_code=product_code,
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
