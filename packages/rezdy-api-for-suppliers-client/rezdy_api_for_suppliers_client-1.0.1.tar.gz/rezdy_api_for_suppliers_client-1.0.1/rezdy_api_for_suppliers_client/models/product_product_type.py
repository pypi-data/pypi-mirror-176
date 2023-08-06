from enum import Enum


class ProductProductType(str, Enum):
    ACTIVITY = "ACTIVITY"
    DAYTOUR = "DAYTOUR"
    MULTIDAYTOUR = "MULTIDAYTOUR"
    PRIVATE_TOUR = "PRIVATE_TOUR"
    TICKET = "TICKET"
    RENTAL = "RENTAL"
    CHARTER = "CHARTER"
    EVENT = "EVENT"
    GIFT_CARD = "GIFT_CARD"
    TRANSFER = "TRANSFER"
    LESSON = "LESSON"
    MERCHANDISE = "MERCHANDISE"
    CUSTOM = "CUSTOM"

    def __str__(self) -> str:
        return str(self.value)
