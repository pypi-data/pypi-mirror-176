from enum import Enum


class RezdyConnectSettingsExternalBookingStrategy(str, Enum):
    TWO_STEPS_BOOKING = "TWO_STEPS_BOOKING"
    ONE_STEP_BOOKING = "ONE_STEP_BOOKING"

    def __str__(self) -> str:
        return str(self.value)
