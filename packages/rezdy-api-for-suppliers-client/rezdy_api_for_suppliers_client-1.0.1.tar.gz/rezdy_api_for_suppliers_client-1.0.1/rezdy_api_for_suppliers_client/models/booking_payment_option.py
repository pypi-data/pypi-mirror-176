from enum import Enum


class BookingPaymentOption(str, Enum):
    CREDITCARD = "CREDITCARD"
    PAYPAL = "PAYPAL"
    BANKTRANSFER = "BANKTRANSFER"
    CASH = "CASH"
    INVOICE = "INVOICE"
    EXTERNAL = "EXTERNAL"
    ALIPAY = "ALIPAY"

    def __str__(self) -> str:
        return str(self.value)
