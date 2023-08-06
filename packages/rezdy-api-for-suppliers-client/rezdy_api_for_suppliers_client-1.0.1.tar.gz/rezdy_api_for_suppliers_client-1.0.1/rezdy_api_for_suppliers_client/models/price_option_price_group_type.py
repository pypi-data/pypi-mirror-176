from enum import Enum


class PriceOptionPriceGroupType(str, Enum):
    EACH = "EACH"
    TOTAL = "TOTAL"

    def __str__(self) -> str:
        return str(self.value)
