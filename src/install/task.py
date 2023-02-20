import sys
import threading
from dataclasses import dataclass, field
from subprocess import Popen, PIPE
from timeit import default_timer as timer

from PyQt5.QtCore import pyqtSignal

from .configuration import Driver

@dataclass(order=False, eq=False)
class Task(threading.Thread):
    
    driver: Driver
    qsig_msg: pyqtSignal
    command: str = None
    rtcode: int = field(init=False, default=-1)
    time: int = field(init=False, default=0)
    finished: bool = field(init=False, default=False)
    
    def __post_init__(self):
        if self.command is None:
            self.command = [self.driver.path, *self.driver.flag]
        super().__init__()
        
    def execute(self):
        """execute without creating a new thread"""
        Popen(self.command)
        
    
    def run(self):
        try:
            start = timer()
            with Popen(self.command, stdout=PIPE, stderr=PIPE) as proc:
                for line in proc.stdout:
                    self.qsig_msg.emit(line.decode('utf-8').strip())
                self.rtcode = proc.wait()
            self.time = timer() - start
        except Exception as e:
            pass
        finally:
            self.finished = True