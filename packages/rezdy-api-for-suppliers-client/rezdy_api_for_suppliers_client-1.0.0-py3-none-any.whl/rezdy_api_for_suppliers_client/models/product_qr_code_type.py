from enum import Enum


class ProductQrCodeType(str, Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"

    def __str__(self) -> str:
        return str(self.value)
