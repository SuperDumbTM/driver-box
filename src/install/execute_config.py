from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class ExecuteConfig:

    silentable: bool
    retryable: bool
    ok_rtcode: list[int] = field(default_factory=list)
    fail_time: float = 5

    def asdict(self) -> dict[str,]:
        return asdict(self)
