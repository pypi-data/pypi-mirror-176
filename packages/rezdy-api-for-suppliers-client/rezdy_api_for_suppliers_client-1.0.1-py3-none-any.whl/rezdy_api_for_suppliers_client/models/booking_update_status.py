from enum import Enum


class BookingUpdateStatus(str, Enum):
    PROCESSING = "PROCESSING"
    NEW = "NEW"
    ON_HOLD = "ON_HOLD"
    PENDING_SUPPLIER = "PENDING_SUPPLIER"
    PENDING_CUSTOMER = "PENDING_CUSTOMER"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    ABANDONED_CART = "ABANDONED_CART"

    def __str__(self) -> str:
        return str(self.value)
