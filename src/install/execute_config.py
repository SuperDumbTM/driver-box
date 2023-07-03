from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ExecuteConfig:

    retryable: bool
    ok_rtcode: list[int] = field(default_factory=list)
    fail_time: float = 5
