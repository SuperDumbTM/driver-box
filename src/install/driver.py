import os
from dataclasses import asdict, dataclass
from typing import Any, Optional

from install.enums import DriverType
from install.execute_config import ExecuteConfig


@dataclass(order=False)
class Driver:

    id: Optional[str]
    type: DriverType
    name: str
    description: str
    path: str
    flags: list[str]
    exec_config: ExecuteConfig

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
