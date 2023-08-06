from enum import Enum


class BookingPaymentType(str, Enum):
    PAYPAL = "PAYPAL"
    CASH = "CASH"
    CREDITCARD = "CREDITCARD"
    BANKTRANSFER = "BANKTRANSFER"
    BANKCHEQUE = "BANKCHEQUE"
    REFUND = "REFUND"
    VOUCHER = "VOUCHER"
    PROMO_CODE = "PROMO_CODE"
    FREE = "FREE"
    OTHER = "OTHER"
    INVOICE = "INVOICE"
    REZDY_PAYOUTS = "REZDY_PAYOUTS"
    ALIPAY = "ALIPAY"

    def __str__(self) -> str:
        return str(self.value)
