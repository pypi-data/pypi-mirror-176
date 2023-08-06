from enum import Enum


class VoucherValueType(str, Enum):
    VALUE_LIMITPRODUCT = "VALUE_LIMITPRODUCT"
    VALUE = "VALUE"
    VALUE_LIMITCATALOG = "VALUE_LIMITCATALOG"
    PERCENT_LIMITPRODUCT = "PERCENT_LIMITPRODUCT"
    PERCENT = "PERCENT"
    PERCENT_LIMITCATALOG = "PERCENT_LIMITCATALOG"
    PRODUCT = "PRODUCT"

    def __str__(self) -> str:
        return str(self.value)
