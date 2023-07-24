from enum import Enum


class DriverType(str, Enum):

    NET = "network"
    DISPLAY = "display"
    MISC = "miscellaneous"
