from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.booking_update import BookingUpdate
from ...models.response_booking import ResponseBooking
from ...types import Response


def _get_kwargs(
    order_number: str,
    *,
    client: Client,
    json_body: BookingUpdate,
) -> Dict[str, Any]:
    url = "{}/bookings/{orderNumber}".format(client.base_url, orderNumber=order_number)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResponseBooking]:
    if response.status_code == 200:
        response_200 = ResponseBooking.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResponseBooking]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    order_number: str,
    *,
    client: Client,
    json_body: BookingUpdate,
) -> Response[ResponseBooking]:
    """Update booking

     When implementing booking update take into consideration below:

    - only certain fields can currently be updated using API
    - only manual payment bookings can be updated
    - update booking in API triggers webhooks and e-mail notifications in the same way as the order
    update through UI
    - good practice is to retrieve the full booking object either from create or get booking response,
    update the necessary fields and pass it whole back to the booking update service. In the future we
    might support updates of additional fields e.g. add and delete of participants. If you don't send
    the participants array in the request, we will recognize it as the participants deletion and remove
    the participant from the existing order
    - order of the items in arrays have to be preserved for the following fields \"items\",
    \"participants\", since no ids are exposed in the API and thus are matched based on the position in
    the array again the existing booking object
    - agent can update supplier orders only if the supplier allow them to *edit orders* when sharing
    their products

    The service method does not support a partial update, **full booking object, as it was retrieved
    from the booking create or search services**, has to be send back to the request payload.
     Otherwise, the properties or relations which <i>are currently supported (see below)</i> and they
    are not sent, will be deleted.
     **Order of the items in arrays have to be preserved for the following fields 'items',
    'participants'.**

    **Currently supported** fields are:

    - Booking.customer - all customer data can be updated
    - Booking.field - all 'per booking' booking fields values
    - Booking.item.participant.field - all 'per participant' booking fields values
    - Booking.resellerComments - both the booking agent and the supplier can update the booking
    resellerComments
    - Booking.resellerReference - both the booking agent and the supplier can update the booking
    resellerReference
    - Booking.items.pickupLocation.locationName - both the booking agent and the supplier can update the
    booking pickup location

    For the sample requests provided in the right panel, consider the booking object below being
    retrieved from a POST order or GET order methods:

    ```
    {
        \"requestStatus\": {
                \"success\": true,
                \"version\": \"v1\"
        },
        \"booking\": {
                \"orderNumber\": \"RSKCJ1K\",
                \"status\": \"CONFIRMED\",
                \"supplierId\": 61,
                \"supplierName\": \"SUPPLIER_PREMIUM_AU\",
                \"customer\": {
                        \"id\": 2,
                        \"firstName\": \"Dusan\",
                        \"lastName\": \"Zahoransky\",
                        \"name\": \"Dusan Zahoransky\",
                        \"email\": \"sample@test.com\"
                },
                \"items\": [
                        {
                                \"productName\": \"activity i session seats pp adult 100f\",
                                \"productCode\": \"P123456\",
                                \"startTime\": \"2017-01-19T09:00:00Z\",
                                \"endTime\": \"2017-01-19T11:00:00Z\",
                                \"startTimeLocal\": \"2017-01-19 20:00:00\",
                                \"endTimeLocal\": \"2017-01-19 22:00:00\",
                                \"quantities\": [
                                        {
                                                \"optionLabel\": \"Adult\",
                                                \"optionPrice\": 100,
                                                \"value\": 1
                                        }
                                ],
                                \"totalQuantity\": 1,
                                \"amount\": 100,
                                \"extras\": [
                                ],
                                \"participants\": [
                                        {
                                                \"fields\": [
                                                        {
                                                                \"label\": \"First Name\",
                                                                \"value\": \"Janko\",
                                                                \"requiredPerParticipant\": false,
                                                                \"requiredPerBooking\": false,
                                                                \"visiblePerParticipant\": false,
                                                                \"visiblePerBooking\": false
                                                        },
                                                        {
                                                                \"label\": \"Last Name\",
                                                                \"value\": \"Hrasko\",
                                                                \"requiredPerParticipant\": false,
                                                                \"requiredPerBooking\": false,
                                                                \"visiblePerParticipant\": false,
                                                                \"visiblePerBooking\": false
                                                        }
                                                ]
                                        }
                                ],
                                \"subtotal\": 100,
                                \"vouchers\": [
                                ]
                        }
                ],
                \"totalAmount\": 100,
                \"totalCurrency\": \"AUD\",
                \"totalPaid\": 0,
                \"totalDue\": 100,
                \"dateCreated\": \"2017-01-19T03:36:18.462Z\",
                \"dateConfirmed\": \"2017-01-19T03:36:18.462Z\",
                \"payments\": [
                ],
                \"fields\": [
                        {
                                \"label\": \"Special Requirements\",
                                \"value\": \"No meat meal option\",
                                \"requiredPerParticipant\": false,
                                \"requiredPerBooking\": false,
                                \"visiblePerParticipant\": false,
                                \"visiblePerBooking\": false
                        }
                ],
                \"source\": \"API\",
                \"vouchers\": [
                ]
        }
    }
    ```

    Args:
        order_number (str):
        json_body (BookingUpdate): Booking update object used to update a booking in Rezdy's
            system.

    Returns:
        Response[ResponseBooking]
    """

    kwargs = _get_kwargs(
        order_number=order_number,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    order_number: str,
    *,
    client: Client,
    json_body: BookingUpdate,
) -> Optional[ResponseBooking]:
    """Update booking

     When implementing booking update take into consideration below:

    - only certain fields can currently be updated using API
    - only manual payment bookings can be updated
    - update booking in API triggers webhooks and e-mail notifications in the same way as the order
    update through UI
    - good practice is to retrieve the full booking object either from create or get booking response,
    update the necessary fields and pass it whole back to the booking update service. In the future we
    might support updates of additional fields e.g. add and delete of participants. If you don't send
    the participants array in the request, we will recognize it as the participants deletion and remove
    the participant from the existing order
    - order of the items in arrays have to be preserved for the following fields \"items\",
    \"participants\", since no ids are exposed in the API and thus are matched based on the position in
    the array again the existing booking object
    - agent can update supplier orders only if the supplier allow them to *edit orders* when sharing
    their products

    The service method does not support a partial update, **full booking object, as it was retrieved
    from the booking create or search services**, has to be send back to the request payload.
     Otherwise, the properties or relations which <i>are currently supported (see below)</i> and they
    are not sent, will be deleted.
     **Order of the items in arrays have to be preserved for the following fields 'items',
    'participants'.**

    **Currently supported** fields are:

    - Booking.customer - all customer data can be updated
    - Booking.field - all 'per booking' booking fields values
    - Booking.item.participant.field - all 'per participant' booking fields values
    - Booking.resellerComments - both the booking agent and the supplier can update the booking
    resellerComments
    - Booking.resellerReference - both the booking agent and the supplier can update the booking
    resellerReference
    - Booking.items.pickupLocation.locationName - both the booking agent and the supplier can update the
    booking pickup location

    For the sample requests provided in the right panel, consider the booking object below being
    retrieved from a POST order or GET order methods:

    ```
    {
        \"requestStatus\": {
                \"success\": true,
                \"version\": \"v1\"
        },
        \"booking\": {
                \"orderNumber\": \"RSKCJ1K\",
                \"status\": \"CONFIRMED\",
                \"supplierId\": 61,
                \"supplierName\": \"SUPPLIER_PREMIUM_AU\",
                \"customer\": {
                        \"id\": 2,
                        \"firstName\": \"Dusan\",
                        \"lastName\": \"Zahoransky\",
                        \"name\": \"Dusan Zahoransky\",
                        \"email\": \"sample@test.com\"
                },
                \"items\": [
                        {
                                \"productName\": \"activity i session seats pp adult 100f\",
                                \"productCode\": \"P123456\",
                                \"startTime\": \"2017-01-19T09:00:00Z\",
                                \"endTime\": \"2017-01-19T11:00:00Z\",
                                \"startTimeLocal\": \"2017-01-19 20:00:00\",
                                \"endTimeLocal\": \"2017-01-19 22:00:00\",
                                \"quantities\": [
                                        {
                                                \"optionLabel\": \"Adult\",
                                                \"optionPrice\": 100,
                                                \"value\": 1
                                        }
                                ],
                                \"totalQuantity\": 1,
                                \"amount\": 100,
                                \"extras\": [
                                ],
                                \"participants\": [
                                        {
                                                \"fields\": [
                                                        {
                                                                \"label\": \"First Name\",
                                                                \"value\": \"Janko\",
                                                                \"requiredPerParticipant\": false,
                                                                \"requiredPerBooking\": false,
                                                                \"visiblePerParticipant\": false,
                                                                \"visiblePerBooking\": false
                                                        },
                                                        {
                                                                \"label\": \"Last Name\",
                                                                \"value\": \"Hrasko\",
                                                                \"requiredPerParticipant\": false,
                                                                \"requiredPerBooking\": false,
                                                                \"visiblePerParticipant\": false,
                                                                \"visiblePerBooking\": false
                                                        }
                                                ]
                                        }
                                ],
                                \"subtotal\": 100,
                                \"vouchers\": [
                                ]
                        }
                ],
                \"totalAmount\": 100,
                \"totalCurrency\": \"AUD\",
                \"totalPaid\": 0,
                \"totalDue\": 100,
                \"dateCreated\": \"2017-01-19T03:36:18.462Z\",
                \"dateConfirmed\": \"2017-01-19T03:36:18.462Z\",
                \"payments\": [
                ],
                \"fields\": [
                        {
                                \"label\": \"Special Requirements\",
                                \"value\": \"No meat meal option\",
                                \"requiredPerParticipant\": false,
                                \"requiredPerBooking\": false,
                                \"visiblePerParticipant\": false,
                                \"visiblePerBooking\": false
                        }
                ],
                \"source\": \"API\",
                \"vouchers\": [
                ]
        }
    }
    ```

    Args:
        order_number (str):
        json_body (BookingUpdate): Booking update object used to update a booking in Rezdy's
            system.

    Returns:
        Response[ResponseBooking]
    """

    return sync_detailed(
        order_number=order_number,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    order_number: str,
    *,
    client: Client,
    json_body: BookingUpdate,
) -> Response[ResponseBooking]:
    """Update booking

     When implementing booking update take into consideration below:

    - only certain fields can currently be updated using API
    - only manual payment bookings can be updated
    - update booking in API triggers webhooks and e-mail notifications in the same way as the order
    update through UI
    - good practice is to retrieve the full booking object either from create or get booking response,
    update the necessary fields and pass it whole back to the booking update service. In the future we
    might support updates of additional fields e.g. add and delete of participants. If you don't send
    the participants array in the request, we will recognize it as the participants deletion and remove
    the participant from the existing order
    - order of the items in arrays have to be preserved for the following fields \"items\",
    \"participants\", since no ids are exposed in the API and thus are matched based on the position in
    the array again the existing booking object
    - agent can update supplier orders only if the supplier allow them to *edit orders* when sharing
    their products

    The service method does not support a partial update, **full booking object, as it was retrieved
    from the booking create or search services**, has to be send back to the request payload.
     Otherwise, the properties or relations which <i>are currently supported (see below)</i> and they
    are not sent, will be deleted.
     **Order of the items in arrays have to be preserved for the following fields 'items',
    'participants'.**

    **Currently supported** fields are:

    - Booking.customer - all customer data can be updated
    - Booking.field - all 'per booking' booking fields values
    - Booking.item.participant.field - all 'per participant' booking fields values
    - Booking.resellerComments - both the booking agent and the supplier can update the booking
    resellerComments
    - Booking.resellerReference - both the booking agent and the supplier can update the booking
    resellerReference
    - Booking.items.pickupLocation.locationName - both the booking agent and the supplier can update the
    booking pickup location

    For the sample requests provided in the right panel, consider the booking object below being
    retrieved from a POST order or GET order methods:

    ```
    {
        \"requestStatus\": {
                \"success\": true,
                \"version\": \"v1\"
        },
        \"booking\": {
                \"orderNumber\": \"RSKCJ1K\",
                \"status\": \"CONFIRMED\",
                \"supplierId\": 61,
                \"supplierName\": \"SUPPLIER_PREMIUM_AU\",
                \"customer\": {
                        \"id\": 2,
                        \"firstName\": \"Dusan\",
                        \"lastName\": \"Zahoransky\",
                        \"name\": \"Dusan Zahoransky\",
                        \"email\": \"sample@test.com\"
                },
                \"items\": [
                        {
                                \"productName\": \"activity i session seats pp adult 100f\",
                                \"productCode\": \"P123456\",
                                \"startTime\": \"2017-01-19T09:00:00Z\",
                                \"endTime\": \"2017-01-19T11:00:00Z\",
                                \"startTimeLocal\": \"2017-01-19 20:00:00\",
                                \"endTimeLocal\": \"2017-01-19 22:00:00\",
                                \"quantities\": [
                                        {
                                                \"optionLabel\": \"Adult\",
                                                \"optionPrice\": 100,
                                                \"value\": 1
                                        }
                                ],
                                \"totalQuantity\": 1,
                                \"amount\": 100,
                                \"extras\": [
                                ],
                                \"participants\": [
                                        {
                                                \"fields\": [
                                                        {
                                                                \"label\": \"First Name\",
                                                                \"value\": \"Janko\",
                                                                \"requiredPerParticipant\": false,
                                                                \"requiredPerBooking\": false,
                                                                \"visiblePerParticipant\": false,
                                                                \"visiblePerBooking\": false
                                                        },
                                                        {
                                                                \"label\": \"Last Name\",
                                                                \"value\": \"Hrasko\",
                                                                \"requiredPerParticipant\": false,
                                                                \"requiredPerBooking\": false,
                                                                \"visiblePerParticipant\": false,
                                                                \"visiblePerBooking\": false
                                                        }
                                                ]
                                        }
                                ],
                                \"subtotal\": 100,
                                \"vouchers\": [
                                ]
                        }
                ],
                \"totalAmount\": 100,
                \"totalCurrency\": \"AUD\",
                \"totalPaid\": 0,
                \"totalDue\": 100,
                \"dateCreated\": \"2017-01-19T03:36:18.462Z\",
                \"dateConfirmed\": \"2017-01-19T03:36:18.462Z\",
                \"payments\": [
                ],
                \"fields\": [
                        {
                                \"label\": \"Special Requirements\",
                                \"value\": \"No meat meal option\",
                                \"requiredPerParticipant\": false,
                                \"requiredPerBooking\": false,
                                \"visiblePerParticipant\": false,
                                \"visiblePerBooking\": false
                        }
                ],
                \"source\": \"API\",
                \"vouchers\": [
                ]
        }
    }
    ```

    Args:
        order_number (str):
        json_body (BookingUpdate): Booking update object used to update a booking in Rezdy's
            system.

    Returns:
        Response[ResponseBooking]
    """

    kwargs = _get_kwargs(
        order_number=order_number,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    order_number: str,
    *,
    client: Client,
    json_body: BookingUpdate,
) -> Optional[ResponseBooking]:
    """Update booking

     When implementing booking update take into consideration below:

    - only certain fields can currently be updated using API
    - only manual payment bookings can be updated
    - update booking in API triggers webhooks and e-mail notifications in the same way as the order
    update through UI
    - good practice is to retrieve the full booking object either from create or get booking response,
    update the necessary fields and pass it whole back to the booking update service. In the future we
    might support updates of additional fields e.g. add and delete of participants. If you don't send
    the participants array in the request, we will recognize it as the participants deletion and remove
    the participant from the existing order
    - order of the items in arrays have to be preserved for the following fields \"items\",
    \"participants\", since no ids are exposed in the API and thus are matched based on the position in
    the array again the existing booking object
    - agent can update supplier orders only if the supplier allow them to *edit orders* when sharing
    their products

    The service method does not support a partial update, **full booking object, as it was retrieved
    from the booking create or search services**, has to be send back to the request payload.
     Otherwise, the properties or relations which <i>are currently supported (see below)</i> and they
    are not sent, will be deleted.
     **Order of the items in arrays have to be preserved for the following fields 'items',
    'participants'.**

    **Currently supported** fields are:

    - Booking.customer - all customer data can be updated
    - Booking.field - all 'per booking' booking fields values
    - Booking.item.participant.field - all 'per participant' booking fields values
    - Booking.resellerComments - both the booking agent and the supplier can update the booking
    resellerComments
    - Booking.resellerReference - both the booking agent and the supplier can update the booking
    resellerReference
    - Booking.items.pickupLocation.locationName - both the booking agent and the supplier can update the
    booking pickup location

    For the sample requests provided in the right panel, consider the booking object below being
    retrieved from a POST order or GET order methods:

    ```
    {
        \"requestStatus\": {
                \"success\": true,
                \"version\": \"v1\"
        },
        \"booking\": {
                \"orderNumber\": \"RSKCJ1K\",
                \"status\": \"CONFIRMED\",
                \"supplierId\": 61,
                \"supplierName\": \"SUPPLIER_PREMIUM_AU\",
                \"customer\": {
                        \"id\": 2,
                        \"firstName\": \"Dusan\",
                        \"lastName\": \"Zahoransky\",
                        \"name\": \"Dusan Zahoransky\",
                        \"email\": \"sample@test.com\"
                },
                \"items\": [
                        {
                                \"productName\": \"activity i session seats pp adult 100f\",
                                \"productCode\": \"P123456\",
                                \"startTime\": \"2017-01-19T09:00:00Z\",
                                \"endTime\": \"2017-01-19T11:00:00Z\",
                                \"startTimeLocal\": \"2017-01-19 20:00:00\",
                                \"endTimeLocal\": \"2017-01-19 22:00:00\",
                                \"quantities\": [
                                        {
                                                \"optionLabel\": \"Adult\",
                                                \"optionPrice\": 100,
                                                \"value\": 1
                                        }
                                ],
                                \"totalQuantity\": 1,
                                \"amount\": 100,
                                \"extras\": [
                                ],
                                \"participants\": [
                                        {
                                                \"fields\": [
                                                        {
                                                                \"label\": \"First Name\",
                                                                \"value\": \"Janko\",
                                                                \"requiredPerParticipant\": false,
                                                                \"requiredPerBooking\": false,
                                                                \"visiblePerParticipant\": false,
                                                                \"visiblePerBooking\": false
                                                        },
                                                        {
                                                                \"label\": \"Last Name\",
                                                                \"value\": \"Hrasko\",
                                                                \"requiredPerParticipant\": false,
                                                                \"requiredPerBooking\": false,
                                                                \"visiblePerParticipant\": false,
                                                                \"visiblePerBooking\": false
                                                        }
                                                ]
                                        }
                                ],
                                \"subtotal\": 100,
                                \"vouchers\": [
                                ]
                        }
                ],
                \"totalAmount\": 100,
                \"totalCurrency\": \"AUD\",
                \"totalPaid\": 0,
                \"totalDue\": 100,
                \"dateCreated\": \"2017-01-19T03:36:18.462Z\",
                \"dateConfirmed\": \"2017-01-19T03:36:18.462Z\",
                \"payments\": [
                ],
                \"fields\": [
                        {
                                \"label\": \"Special Requirements\",
                                \"value\": \"No meat meal option\",
                                \"requiredPerParticipant\": false,
                                \"requiredPerBooking\": false,
                                \"visiblePerParticipant\": false,
                                \"visiblePerBooking\": false
                        }
                ],
                \"source\": \"API\",
                \"vouchers\": [
                ]
        }
    }
    ```

    Args:
        order_number (str):
        json_body (BookingUpdate): Booking update object used to update a booking in Rezdy's
            system.

    Returns:
        Response[ResponseBooking]
    """

    return (
        await asyncio_detailed(
            order_number=order_number,
            client=client,
            json_body=json_body,
        )
    ).parsed
