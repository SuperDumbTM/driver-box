import threading
import time
from subprocess import Popen, PIPE
from typing import Union
from timeit import default_timer as timer
from PyQt5.QtCore import pyqtSignal

class Task(threading.Thread):
    
    def __init__(self, iden, qslot: pyqtSignal, cmd: Union[str, list], kwargs) -> None:
        super().__init__()
        self.iden = iden
        self._cmd = cmd
        self._slot = qslot
        if kwargs == None: kwargs = {}
        self._kwargs = kwargs
        self.rtcode = None
        
    def execute(self):
        """execute without creating a new thread"""
        print(self._cmd)
        Popen(self._cmd, **self._kwargs)
    
    def run(self):
        try:
            start = timer()
            
            with Popen(self._cmd, stdout=PIPE, stderr=PIPE, **self._kwargs) as proc:
                for line in proc.stdout:
                    self._slot.emit((line.decode('utf-8')).strip())
                self.rtcode = proc.wait()
            
            self.time = timer() - start
        except Exception as e:
            raise