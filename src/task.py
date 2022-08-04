import threading
import time
from subprocess import Popen, PIPE
from typing import Union
from timeit import default_timer as timer

class Task(threading.Thread):
    
    def __init__(self, cmd: Union(str, list), kwargs) -> None:
        super().__init__()
        self._cmd = cmd
        self._kwargs = kwargs
        self.rtcode = None
        self.err_msg = ""
        
    def execute(self):
        """execute without creating a new thread"""
        Popen(self._cmd, **self._kwargs)
    
    def run(self):
        try:
            start = timer()
            
            p = Popen(self._cmd, stdout=PIPE, bufsize=1, **self._kwargs)
            with p.stdout:
                for line in iter(p.stdout.readline, b''): 
                    print(line)
            self.rtcode = p.wait()
            
            end = timer()
            self.time = end-start
        except Exception as e:
            self.err_msg = str(e)
            self.rtcode = -999