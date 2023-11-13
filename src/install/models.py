import json
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

try:
    from enums import DriverType, HaltOption
except ImportError:
    from .enums import DriverType, HaltOption


@dataclass(order=False)
class Driver:

    id: Optional[str]
    type: DriverType
    name: str
    description: str
    path: str
    flags: list[str]
    exec_config: "ExecuteConfig"

    def asdict(self) -> dict[str, Any]:
        d = asdict(self)
        d['type'] = self.type.value
        d['exec_config'] = self.exec_config.asdict()
        return d

    def is_validate(self) -> bool:
        return all((
            isinstance(self.id, (str, type(None))),
            isinstance(self.type, DriverType),
            isinstance(self.name, str),
            isinstance(self.description, str),
            isinstance(self.path, str) and os.path.exists(self.path),
            isinstance(self.flags, list),
            isinstance(self.exec_config, ExecuteConfig),
        ))


@dataclass(frozen=True)
class ExecuteConfig:

    silentable: bool
    retryable: bool
    ok_rtcode: list[int] = field(default_factory=list)
    fail_time: float = 5

    def asdict(self) -> dict[str,]:
        return asdict(self)


@dataclass
class InstallOption:
    path: os.PathLike
    auto_install: bool
    async_install: bool
    retry_on_fail: bool
    halt_option: HaltOption
    is_init_disks: bool
    is_set_passwd: bool
    passwd: str = ""

    @staticmethod
    def from_file(path: os.PathLike, not_found_ok: bool) -> "InstallOption":
        if not os.path.exists(path):
            if not not_found_ok:
                raise FileExistsError(f"\"{path}\" does not exists.")
            else:
                obj = InstallOption(path, True, True, True,
                                    HaltOption.REBOOT, False, False)
                obj.persist()
                return obj
        with open(path, "r") as f:
            config = json.load(f)
            config['halt_option'] = HaltOption(config['halt_option'])
            return InstallOption(path=path, **config)

    def persist(self):
        dump = asdict(self)
        dump.pop("path")
        dump['halt_option'] = dump['halt_option'].value

        with open(self.path, "w") as f:
            json.dump(dump, f, indent=4)
