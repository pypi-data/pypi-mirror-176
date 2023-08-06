from enum import Enum


class ProductCreateRequestBarcodeOutputType(str, Enum):
    PARTICIPANT = "PARTICIPANT"
    ORDER = "ORDER"

    def __str__(self) -> str:
        return str(self.value)
