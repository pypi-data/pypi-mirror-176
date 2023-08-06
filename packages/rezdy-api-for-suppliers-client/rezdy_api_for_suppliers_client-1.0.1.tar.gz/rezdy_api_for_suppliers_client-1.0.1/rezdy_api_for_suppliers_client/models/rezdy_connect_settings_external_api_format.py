from enum import Enum


class RezdyConnectSettingsExternalApiFormat(str, Enum):
    XML = "XML"
    JSON = "JSON"

    def __str__(self) -> str:
        return str(self.value)
