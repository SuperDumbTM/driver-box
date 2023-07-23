from enum import Enum


class HaltOption(Enum):
    NONE = "沒有動作"
    SHUTDOWN = "關機"
    REBOOT = "重新開機"
    BIOS = "進入 BIOS"
