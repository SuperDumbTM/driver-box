from enum import Enum


class ExecuteStatus(Enum):
    PENDING = 1
    INPROGRESS = 2
    EXITED = 3
    SUCCESS = 4
    ERROR = 5
    FAILED = 6
    ABORTED = 7
