import os
import time
import struct
import subprocess
from dataclasses import dataclass, field
from typing import Optional, Union

from enums.install_status import InstallStatus


@dataclass(order=False, eq=False)
class Task:

    name: str
    command: Union[str, os.PathLike]
    options: Optional[list[str]]
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
