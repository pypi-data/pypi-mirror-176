from enum import Enum


class ProductBookingMode(str, Enum):
    NO_DATE = "NO_DATE"
    DATE_ENQUIRY = "DATE_ENQUIRY"
    INVENTORY = "INVENTORY"

    def __str__(self) -> str:
        return str(self.value)
