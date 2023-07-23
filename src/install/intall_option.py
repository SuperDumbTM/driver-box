import json
import os
from dataclasses import asdict, dataclass

from enums.halt_option import HaltOption


@dataclass
class InstallOption:
    path: os.PathLike
    auto_install: bool
    async_install: bool
    retry_on_fail: bool
    halt_option: HaltOption
    is_set_passwd: bool
    passwd: str = ""

    @staticmethod
    def from_file(path: os.PathLike, not_found_ok: bool) -> "InstallOption":
        if not os.path.exists(path):
            if not not_found_ok:
                raise FileExistsError(f"\"{path}\" does not exists.")
            else:
                obj = InstallOption(True, True, True, HaltOption.REBOOT, False)
                obj.persist(path)
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
