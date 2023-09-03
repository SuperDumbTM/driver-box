from abc import ABC, abstractmethod
import os
import time
import struct
import subprocess
from typing import Iterable, Optional


try:
    from execute_config import ExecuteConfig
    from execute_status import ExecuteStatus
except ImportError:
    from .execute_config import ExecuteConfig
    from .execute_status import ExecuteStatus


class Task(ABC):

    def __init__(self, name: str, exe_conf: ExecuteConfig) -> None:
        self.name = name
        self.exe_conf = exe_conf

    @property
    def status(self) -> ExecuteStatus:
        pass

    @property
    @abstractmethod
    def is_aborted(self):
        """Whether the execution is terminated by users
        """
        pass

    @property
    @abstractmethod
    def exception(self) -> Optional[BaseException]:
        pass

    @abstractmethod
    def execute(self, no_options: bool = False):
        """Starts to execute the task
        """
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        """Return whether the task is still in execution
        """
        pass

    @abstractmethod
    def abort(self):
        """Terminate the task execution
        """
        pass


class ExecutableTask(Task):

    command: str | os.PathLike
    options: Optional[Iterable[str]]

    _status: ExecuteStatus = ExecuteStatus.PENDING
    _process: subprocess.Popen = None
    """Popen instance of the execution. `None` if the execution is not yet started"""

    _exception: BaseException = None

    def __init__(self,
                 name: str,
                 exe_conf: ExecuteConfig,
                 command: str | os.PathLike,
                 options: Optional[Iterable[str]] = None) -> None:
        super().__init__(name, exe_conf)
        self.command = command
        self.options = options

    @property
    def status(self) -> ExecuteStatus:
        return self._status

    @property
    def is_aborted(self):
        return self._status == ExecuteStatus.ABORTED

    @property
    def exception(self) -> Optional[BaseException]:
        return self._exception

    @property
    def messages(self) -> list[str]:
        """Message outputs during the execution
        """
        if self._process is None:
            return []
        else:
            return [line.decode('utf-8').strip() for line in self._process.stdout]

    @property
    def full_command(self) -> str:
        return "{0} {1}".format(self.command, ' '.join(self.options))

    @property
    def rtcode(self) -> Optional[int]:
        """Return code of the execution. `None` if the execution is not yet started or finished"""
        try:
            if self._process is None:
                return None
            else:
                return struct.unpack(
                    'i', struct.pack('I', self._process.returncode))[0]
        except IndexError:
            return self._process.returncode

    def execute(self, no_options: bool = False):
        self._status = ExecuteStatus.INPROGRESS

        try:
            exe_time = time.time()
            if no_options:
                self._process = subprocess.Popen(
                    self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                self._process = subprocess.Popen(
                    self.full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            while self.is_alive():
                time.sleep(0.1)
        except Exception as e:
            self._status = ExecuteStatus.ERROR
            self._exception = e
            return

        if self.is_aborted:
            pass
        elif self.rtcode not in (0, *self.exe_conf.ok_rtcode):
            self._status = ExecuteStatus.FAILED
        elif time.time() - exe_time < self.exe_conf.fail_time:
            self._status = ExecuteStatus.EXITED
        else:
            self._status = ExecuteStatus.SUCCESS

    def is_alive(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def abort(self):
        # os.system(f"taskkill /im " + self.executable.split("\\")[-1] + " /f")
        self._status = ExecuteStatus.ABORTING
        if self._process is None:
            self._status = ExecuteStatus.ABORTED
        else:
            self._process.kill()
            time.sleep(2)
            if self._process.poll() is not None:
                self._status = ExecuteStatus.ABORTED
            else:
                pass
