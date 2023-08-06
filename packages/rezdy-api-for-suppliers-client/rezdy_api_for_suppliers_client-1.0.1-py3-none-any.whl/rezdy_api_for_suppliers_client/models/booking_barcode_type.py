from enum import Enum


class BookingBarcodeType(str, Enum):
    TEXT = "TEXT"
    CODE_39 = "CODE_39"
    CODE_128 = "CODE_128"
    QR_CODE = "QR_CODE"
    EAN_8 = "EAN_8"
    EAN_13 = "EAN_13"
    ITF = "ITF"

    def __str__(self) -> str:
        return str(self.value)
