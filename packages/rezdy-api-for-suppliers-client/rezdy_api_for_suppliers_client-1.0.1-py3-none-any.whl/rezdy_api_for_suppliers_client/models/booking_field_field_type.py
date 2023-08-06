from enum import Enum


class BookingFieldFieldType(str, Enum):
    STRING = "String"
    LIST = "List"
    BOOLEAN = "Boolean"
    PHONE = "Phone"
    DATE = "Date"
    HIDDEN = "Hidden"

    def __str__(self) -> str:
        return str(self.value)
