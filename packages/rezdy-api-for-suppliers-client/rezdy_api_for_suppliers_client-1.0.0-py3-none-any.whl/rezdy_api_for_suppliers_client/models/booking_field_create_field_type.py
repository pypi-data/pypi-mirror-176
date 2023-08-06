from enum import Enum


class BookingFieldCreateFieldType(str, Enum):
    STRING = "String"
    LIST = "List"
    BOOLEAN = "Boolean"
    HIDDEN = "Hidden"

    def __str__(self) -> str:
        return str(self.value)
