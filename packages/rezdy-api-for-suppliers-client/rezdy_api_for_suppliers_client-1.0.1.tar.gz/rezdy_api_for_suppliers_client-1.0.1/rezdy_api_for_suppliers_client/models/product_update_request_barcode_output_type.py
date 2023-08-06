from enum import Enum


class ProductUpdateRequestBarcodeOutputType(str, Enum):
    PARTICIPANT = "PARTICIPANT"
    ORDER = "ORDER"

    def __str__(self) -> str:
        return str(self.value)
