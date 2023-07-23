from enum import Enum


class DriverType(str, Enum):

    NET = "network"
    DISPLAY = "display"
    MISC = "miscellaneous"

    @classmethod
    def members(cls) -> list["DriverType"]:
        return [enum for enum in cls]
