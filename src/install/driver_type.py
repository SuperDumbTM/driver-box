from enum import Enum


class DriverType(str, Enum):

    NET = "network"
    DISPLAY = "display"
    MISC = "miscellaneous"

    @classmethod
    def members(cls) -> list["DriverType"]:
        return [enum for enum in cls]

    @staticmethod
    def from_str(dri_type: str) -> "DriverType":
        for t in DriverType.members():
            if (t.value.lower() == dri_type.lower()):
                return t
        raise ValueError(f"driver type does not exists: {dri_type}")
