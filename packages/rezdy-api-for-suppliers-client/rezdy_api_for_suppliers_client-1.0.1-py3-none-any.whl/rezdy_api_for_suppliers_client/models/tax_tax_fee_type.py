from enum import Enum


class TaxTaxFeeType(str, Enum):
    TAX = "TAX"
    FEE = "FEE"

    def __str__(self) -> str:
        return str(self.value)
