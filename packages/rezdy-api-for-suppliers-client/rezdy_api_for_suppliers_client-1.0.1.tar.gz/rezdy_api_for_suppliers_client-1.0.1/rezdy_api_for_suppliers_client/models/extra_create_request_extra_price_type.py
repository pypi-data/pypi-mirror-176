from enum import Enum


class ExtraCreateRequestExtraPriceType(str, Enum):
    ANY = "ANY"
    FIXED = "FIXED"
    QUANTITY = "QUANTITY"

    def __str__(self) -> str:
        return str(self.value)
