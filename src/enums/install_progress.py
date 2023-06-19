from enum import Enum


class InstallProgress(Enum):
    INFO = 1
    WARN = 2
    PASS = 3
    FAIL = 4
