import os
from dataclasses import dataclass, field
import subprocess

from .configuration import Driver


@dataclass(order=False, eq=False)
class Task:

    driver: Driver
    command: str = None

    process: subprocess.Popen = field(init=False, default=None)
    """Popen instance of the execution.  `None` if the execution is not yet started"""

    _aborted: bool = field(init=False, default=False)

    @property
    def executable(self) -> os.PathLike:
        """Path of the executable"""
        return self.driver.path

    @property
    def rtcode(self):
        """Return code of the execution. `None` if the execution is not yet started or finished"""
        return None if self.process is None else self.process.returncode

    @property
    def messages(self) -> list[str]:
        """Message output during the execution"""
        return [] if self.process is None else [line.decode('utf-8').strip() for line in self.process.stdout]

    @property
    def is_aborted(self):
        """Whether the execution is manually terminated"""
        return self._aborted

    def __post_init__(self):
        if self.command is None:
            self.command = [self.driver.path, *self.driver.flag]

    def execute(self):
        """Run the executable"""
        self.process = subprocess.Popen(
            self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def execute_pure(self):
        """Run the executable without any flags/options"""
        self.process = subprocess.Popen(
            self.driver.path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def is_alive(self) -> bool:
        """Return whether the executable is still executing"""
        return self.process is None or self.process.poll() is None

    def abort(self):
        """Terminate the execution"""
        # os.system(f"taskkill /im " + self.executable.split("\\")[-1] + " /f")
        self.process.kill()
        self._aborted = True
