import os
import json
import random
import string
from typing import Any, Final, Optional, Union
from dataclasses import asdict, dataclass

try:
    from driver_type import DriverType
except ImportError:
    from .driver_type import DriverType


ID_LEN: Final[int] = 6
FLAG_PRESET: Final[dict] = {
    'AMD Chipset': ["/S"],
    'AMD Display': ["-install"],
    'Intel Bluetooth': ["/quiet", "/norestart"],
    'Intel Chipset': ["-s", "-norestart"],
    'Intel Display': ["-s"],
    'Intel iGPU': ["-s"],
    'Intel LAN': ["/s"],
    'Intel WiFi': ["-q", "-repair"],
    'Nvidia Display': ["-s", "-noreboot", "Display.Driver"],
    'Realtek LAN': ["-s"]
}


@dataclass(order=False)
class Driver:

    id: Optional[str]
    type: DriverType
    name: str
    description: str
    path: str
    flags: list[str]
    fail_time: Union[int, float]
    autoable: bool
    retryable: bool

    def asdict(self) -> dict[str, Any]:
        _d = asdict(self)
        _d['type'] = self.type.value
        return _d

    def is_validate(self, is_new: bool = False) -> bool:
        return all((
            is_new or (isinstance(self.id, str) and len(self.id) >= ID_LEN),
            isinstance(self.type, DriverType),
            isinstance(self.name, str),
            isinstance(self.description, str),
            isinstance(self.path, str) and os.path.exists(self.path),
            isinstance(self.flags, list),
            isinstance(self.fail_time, (int, float)),
            isinstance(self.autoable, bool),
            isinstance(self.retryable, bool)
        ))


class DriverConfig:

    _data: dict[str, list[Driver]]

    _dir = "driver"
    """Directory name for driver executables"""

    def __init__(self,
                 confpath: Union[str, os.PathLike],
                 dridir: Union[str, os.PathLike],
                 not_found_ok: bool
                 ) -> None:
        if not os.path.exists(confpath):
            if not not_found_ok:
                raise FileExistsError(f"\"{confpath}\" does not exists")
            os.makedirs(os.path.dirname(confpath), exist_ok=True)
            with open(os.path.join(confpath), 'w') as f:
                json.dump({DriverType.NET.value: [],
                           DriverType.DISPLAY.value: [],
                           DriverType.MISC.value: []},
                          f)

        self.confdir = confpath
        self.dridir = dridir
        self._data = self._read()

    def get(self, dri_id: str) -> Driver:
        """Retrive a driver configuration by driver ID

        Args:
            dri_id (str): Unique ID of the driver
        """
        _type, _id = self._locate(dri_id)
        return self._data[_type][_id]

    def get_type(self, dri_type: DriverType) -> list[Driver]:
        """Retrive driver configurations by driver type

        Args:
            dri_type (DriverType): Type of drivers

        Returns:
            list[Driver]: list of drivers of type `dri_type`
        """
        return self._data[dri_type] if dri_type is not None else self._data

    def create(self, driver: Driver) -> None:
        """Insert a new driver to the driver configuration

        Args:
            driver (Driver): New driver, `driver.id` will be generated automatically

        Raises:
            ValueError: The attribute(s) of the new driver is not valid
        """
        if not driver.is_validate(is_new=True):
            raise ValueError()

        while locals().get("new_id") is None or not self.is_id_unique(new_id):
            new_id = ''.join(random.choice(string.ascii_uppercase + string.digits)
                             for _ in range(ID_LEN))
        driver.id = new_id
        self._data[driver.type].append(driver)

    def update(self, dri_id: str, driver: Driver) -> None:
        """Update a driver configuration by the driver ID

        Args:
            dri_id (str): Target driver ID
            driver (Driver): New driver configuration
        """
        t, idx = self._locate(dri_id)
        self._data[t][idx] = driver

    def delete(self, dri_id: str) -> None:
        """Remove a driver configuration by the driver ID.
        You have to explicitly call `write` to presist the changes

        Args:
            dri_id (str): Target driver ID
        """
        t, _ = self._locate(dri_id)
        self._data[t] = [dri for dri in self._data[t] if dri.id != dri_id]

    def write(self) -> None:
        """Presist the changes to file system
        """
        _d = {dri_type: [driver.asdict() for driver in drivers]
              for dri_type, drivers in self._data.items()}
        with open(self.confdir, "w", encoding="utf-8") as f:
            json.dump(_d, f, indent=4)

    def is_id_unique(self, id: str) -> bool:
        """Check if a ID is unique amoung existing driver configuration

        Args:
            id (str): The ID to be checked
        """
        for drivers in self._data.values():
            for driver in drivers:
                if driver.id == id:
                    return False
        return True

    def _locate(self, dri_id: str) -> tuple[str, int]:
        for dri_type, drivers in self._data.items():
            for idx, driver in enumerate(drivers):
                if driver.id == dri_id:
                    return (dri_type, idx)
        return (None, None)

    def _read(self) -> None:
        with open(self.confdir, "r", encoding="utf-8") as f:
            buff = json.load(f)
            return {dri_type: [
                Driver(dri['id'],
                       DriverType.from_str(dri_type),
                       dri['name'],
                       dri['description'],
                       dri['path'],
                       dri['flags'],
                       dri['fail_time'],
                       dri['autoable'],
                       dri['retryable'],
                       )
                for dri in dris] for dri_type, dris in buff.items()}
