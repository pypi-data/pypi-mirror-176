from enum import Enum


class CustomerTitle(str, Enum):
    MR = "MR"
    MS = "MS"
    MRS = "MRS"
    MISS = "MISS"

    def __str__(self) -> str:
        return str(self.value)
