from abc import ABC, abstractmethod
import os
import time
import struct
import subprocess
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional, Union

from enums.install_status import InstallStatus


class Task(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def rtcode(self) -> Optional[int]:
        """Return code of the execution. `None` if the execution is not yet started or finished"""
        pass

    @property
    @abstractmethod
    def messages(self) -> list[str]:
        """Message outputs during the execution"""
        pass

    @property
    @abstractmethod
    def is_aborted(self):
        """Whether the execution is manually terminated"""
        pass

    @property
    @abstractmethod
    def exception(self) -> Optional[BaseException]:
        pass

    @abstractmethod
    def execute(self, no_options: bool = False):
        """Run the executable"""
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        """Return whether the executable is still executing"""
        pass

    @abstractmethod
    def abort(self):
        """Terminate the execution"""
        pass


@dataclass(order=False, eq=False)
class ShellTask(Task):

    name: str
    command: Union[str, os.PathLike]

    options: Optional[Iterable[str]] = field(default_factory=tuple)
    abort_time: Optional[float] = None

    status: InstallStatus = field(init=False, default=InstallStatus.PENDING)
    process: subprocess.Popen = field(init=False, default=None)
    """Popen instance of the execution.  `None` if the execution is not yet started"""
    _exception: BaseException = field(init=False, default=None)

    _aborted: bool = field(init=False, default=False)

    @property
    def full_command(self) -> str:
        return "{0} {1}".format(self.command, ' '.join(self.options))

    @property
    def rtcode(self) -> Optional[int]:
        """Return code of the execution. `None` if the execution is not yet started or finished"""
        try:
            if self.process is None:
                return None
            else:
                return struct.unpack(
                    'i', struct.pack('I', self.process.returncode))[0]
        except IndexError:
            return self.process.returncode

    @property
    def messages(self) -> list[str]:
        """Message outputs during the execution"""
        if self.process is None:
            return []
        else:
            return [line.decode('utf-8').strip() for line in self.process.stdout]

    @property
    def is_aborted(self):
        """Whether the execution is manually terminated"""
        return self._aborted

    @property
    def exception(self) -> Optional[BaseException]:
        return self._exception

    def execute(self, no_options: bool = False):
        """Run the executable"""
        self.status = InstallStatus.INPROGRESS

        try:
            exe_time = time.time()
            if no_options:
                self.process = subprocess.Popen(
                    self.full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                self.process = subprocess.Popen(
                    self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            while self.is_alive():
                time.sleep(0.1)
        except Exception as e:
            self._exception = e

        if self.is_aborted:
            pass
            # self.status = InstallStatus.ABORTED
        elif self.rtcode == 0:
            self.status = InstallStatus.SUCCESS
        elif self.abort_time and time.time() - exe_time < self.abort_time:
            self.status = InstallStatus.EXITED
        else:
            self.status = InstallStatus.FAILED

    def is_alive(self) -> bool:
        """Return whether the executable is still executing"""
        return self.process is None or self.process.poll() is None

    def abort(self):
        """Terminate the execution"""
        # os.system(f"taskkill /im " + self.executable.split("\\")[-1] + " /f")
        self._aborted = True

        if self.process is None:
            self.status = InstallStatus.ABORTED
        else:
            self.process.kill()
            if self.process.poll() is not None:
                self.status = InstallStatus.ABORTED


# @dataclass(order=False, eq=False)
# class FunctionalTask(Task):

#     name: str
#     function: Callable
#     args: Optional[list]
#     kwargs: Optional[dict]
#     abort_time: Optional[float] = None

#     status: InstallStatus = field(init=False, default=InstallStatus.PENDING)
#     process: subprocess.Popen = field(init=False, default=None)
#     """Popen instance of the execution.  `None` if the execution is not yet started"""
#     _exception: BaseException = field(init=False, default=None)

#     _aborted: bool = field(init=False, default=False)

#     @property
#     def rtcode(self) -> Optional[int]:
#         pass

#     @property
#     def messages(self) -> list[str]:
#         pass

#     @property
#     def is_aborted(self):
#         pass

#     @property
#     def exception(self) -> Optional[BaseException]:
#         return self._exception

#     def execute(self, no_options: bool = False):
#         pass

#     def is_alive(self) -> bool:
#         pass

#     def abort(self):
#         pass
