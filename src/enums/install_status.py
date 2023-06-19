from enum import Enum


class InstallStatus(Enum):
    PENDING = 1
    INPROGRESS = 2
    EXITED = 3
    SUCCESS = 4
    FAILED = 5
    ABORTED = 6
