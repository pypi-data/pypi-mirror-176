from enum import Enum


class ProductAgentPaymentType(str, Enum):
    PAYOUTS = "PAYOUTS"
    FULL_AGENT = "FULL_AGENT"
    DOWNPAYMENT = "DOWNPAYMENT"
    FULL_SUPPLIER = "FULL_SUPPLIER"
    NONE = "NONE"

    def __str__(self) -> str:
        return str(self.value)
