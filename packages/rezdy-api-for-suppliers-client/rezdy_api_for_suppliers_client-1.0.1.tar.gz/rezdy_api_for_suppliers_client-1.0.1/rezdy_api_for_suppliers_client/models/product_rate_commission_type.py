from enum import Enum


class ProductRateCommissionType(str, Enum):
    NET_RATE = "NET_RATE"
    PERCENT = "PERCENT"

    def __str__(self) -> str:
        return str(self.value)
