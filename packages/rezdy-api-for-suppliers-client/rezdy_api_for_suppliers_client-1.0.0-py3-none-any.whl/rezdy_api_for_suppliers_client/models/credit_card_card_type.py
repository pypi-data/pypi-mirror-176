from enum import Enum


class CreditCardCardType(str, Enum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    AMEX = "AMEX"
    DINERS = "DINERS"
    DISCOVER = "DISCOVER"
    JCB = "JCB"

    def __str__(self) -> str:
        return str(self.value)
