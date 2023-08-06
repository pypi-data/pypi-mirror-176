from enum import Enum


class VoucherStatus(str, Enum):
    ISSUED = "ISSUED"
    REDEEMED = "REDEEMED"
    PARTIALLY_REDEEMED = "PARTIALLY_REDEEMED"
    EXPIRED = "EXPIRED"

    def __str__(self) -> str:
        return str(self.value)
