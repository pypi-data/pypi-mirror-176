from enum import Enum


class CustomerGender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

    def __str__(self) -> str:
        return str(self.value)
