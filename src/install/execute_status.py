from enum import Enum


class ExecuteStatus(Enum):
    PENDING = 1
    INPROGRESS = 2
    EXITED = 3
    SUCCESS = 4
    FAILED = 5
    ABORTED = 6
