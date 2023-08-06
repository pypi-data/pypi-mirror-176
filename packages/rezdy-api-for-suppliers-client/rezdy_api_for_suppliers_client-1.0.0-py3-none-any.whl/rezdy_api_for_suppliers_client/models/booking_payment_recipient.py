from enum import Enum


class BookingPaymentRecipient(str, Enum):
    SUPPLIER = "SUPPLIER"
    RESELLER = "RESELLER"
    REZDY = "REZDY"

    def __str__(self) -> str:
        return str(self.value)
