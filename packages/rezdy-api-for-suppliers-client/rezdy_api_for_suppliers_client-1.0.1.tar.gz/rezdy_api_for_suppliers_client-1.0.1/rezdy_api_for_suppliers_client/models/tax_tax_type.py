from enum import Enum


class TaxTaxType(str, Enum):
    PERCENT = "PERCENT"
    FIXED_PER_QUANTITY = "FIXED_PER_QUANTITY"
    FIXED_PER_ORDER = "FIXED_PER_ORDER"
    FIXED_PER_DURATION = "FIXED_PER_DURATION"

    def __str__(self) -> str:
        return str(self.value)
