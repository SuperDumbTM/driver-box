import os
import json
import random
import string
import pathlib
from enum import Enum
from typing import Literal
from dataclasses import asdict, dataclass


ID_LEN = 6


class DriverType(str, Enum):
    
    NET = "network"
    DISPLAY = "display"
    MISC = "miscellaneous"
    
    @classmethod
    def members(cls) -> list["DriverType"]:
        return [enum for enum in cls]
    
    @staticmethod
    def from_str(dri_type: str) -> "Driver":
        for t in DriverType.members():
            if (t.value.lower() == dri_type.lower()):
                return t
        raise ValueError(f"driver type does not exists: {dri_type}")


@dataclass
class Driver:
    
    id: str
    type: DriverType
    name: str
    description: str
    path: str
    autoable: bool
    flag: list[str]
    
    def as_dict(self) -> dict[str]:
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
            isinstance(self.autoable, bool),
            isinstance(self.flag, list)
        ))


class DriverConfig:
    
    _data: dict[str, list[Driver]]
    
    _dir = "driver"
    """directory name for driver executables"""
    
    @property
    def driver_directory_abs(self) -> os.PathLike:
        return self.dridir
    
    def __init__(self, confpath: os.PathLike, dridir: os.PathLike) -> None:
        if not os.path.exists(confpath):
            raise FileExistsError(f"\"{confpath}\" does not exists")
        
        self.confdir = confpath
        self.dridir = dridir
        self._data = self._read()
        
    def get(self, dri_type: DriverType = None) -> list[Driver]:
        if dri_type is not None:
            return self._data[dri_type]
        else:
            return self._data
    
    def find(self, dri_id: str) -> Driver:
        _type, _id = self._find(dri_id)
        return self._data[_type][_id]
    
    def create(self, dri_type: DriverType, driver: Driver) -> None:
        if not driver.is_validate(is_new=True):
            raise ValueError()
        
        while locals().get("new_id") is None or not self.is_id_unique(new_id):
            new_id = ''.join(random.choice(string.ascii_uppercase + string.digits)
                            for _ in range(ID_LEN))
        driver.id = new_id
        self._data[dri_type].append(driver)        

    def update(self, dri_id: str, driver: Driver) -> None:
        _t, _idx = self._find(dri_id)
        
        self._data[_t][_idx] = driver
        
    
    def remove(self, dri_type: DriverType, id: str) -> None:
        self._data[dri_type] = [dri for dri in self._data[dri_type] if dri.id != id]
    
    def write(self) -> None:
        _d = {dri_type: [driver.as_dict() for driver in drivers] 
              for dri_type, drivers in self._data.items()}
        with open(self.confdir, "w", encoding="utf-8") as f:
                json.dump(_d, f)
    
    def is_id_unique(self, id: str) -> bool:
        for type, drivers in self._data.items():
            for driver in drivers:
                if driver.id == id:
                    return False
        return True
    
    def _find(self, dri_id: str) -> tuple[str, int]:
        for dri_type, drivers in self._data.items():
            for idx, driver in enumerate(drivers):
                if driver.id == dri_id:
                    return (dri_type, idx)
        return (None, None)

    def _read(self) -> None:
        with open(self.confdir, "r", encoding="utf-8") as f:
            buff = json.load(f)
            return {dri_type: [
                Driver(dri['id'], DriverType.from_str(dri_type), dri['name'],
                       dri['description'], dri['path'], dri['autoable'],
                       dri['flag']) 
                for dri in dris] for dri_type, dris in buff.items()}


class Setting(DriverConfig):
    
        def __init__(self, path: str) -> None:
            self.path = path
            with open(path, 'r', encoding="utf-8") as f:
                self.conf = json.load(f)
                
        def write_conf(self):
            with open(self.path, 'w', encoding="utf-8") as f:
                json.dump(self.conf, f)
        