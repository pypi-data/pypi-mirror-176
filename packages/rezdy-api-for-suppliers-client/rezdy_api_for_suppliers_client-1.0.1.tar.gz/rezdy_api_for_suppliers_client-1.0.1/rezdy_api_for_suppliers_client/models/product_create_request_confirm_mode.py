from enum import Enum


class ProductCreateRequestConfirmMode(str, Enum):
    MANUAL = "MANUAL"
    AUTOCONFIRM = "AUTOCONFIRM"
    MANUAL_THEN_AUTO = "MANUAL_THEN_AUTO"
    AUTO_THEN_MANUAL = "AUTO_THEN_MANUAL"

    def __str__(self) -> str:
        return str(self.value)
