from enum import Enum


class BookingResellerSource(str, Enum):
    ONLINE = "ONLINE"
    INTERNAL = "INTERNAL"
    PARTNERS = "PARTNERS"
    COMMUNITY = "COMMUNITY"
    MARKETPLACE = "MARKETPLACE"
    MARKETPLACE_PREF_RATE = "MARKETPLACE_PREF_RATE"
    API = "API"

    def __str__(self) -> str:
        return str(self.value)
