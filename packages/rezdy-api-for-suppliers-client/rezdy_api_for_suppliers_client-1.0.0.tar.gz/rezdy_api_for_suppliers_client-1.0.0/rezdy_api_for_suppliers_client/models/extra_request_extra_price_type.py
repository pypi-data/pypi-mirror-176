from enum import Enum


class ExtraRequestExtraPriceType(str, Enum):
    ANY = "ANY"
    FIXED = "FIXED"
    QUANTITY = "QUANTITY"

    def __str__(self) -> str:
        return str(self.value)
