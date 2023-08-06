from enum import Enum


class ProductSeoTagMetaType(str, Enum):
    META_NAME = "META_NAME"
    META_PROPERTY = "META_PROPERTY"
    LINK_REL = "LINK_REL"
    TITLE = "TITLE"
    NOINDEX = "NOINDEX"
    REL_CANONICAL = "REL_CANONICAL"

    def __str__(self) -> str:
        return str(self.value)
