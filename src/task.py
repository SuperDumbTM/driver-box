import threading
import subprocess
import time
from timeit import default_timer as timer

class Task(threading.Thread):
    
    def __init__(self, args: list) -> None:
        super().__init__()
        self.args = args
        self.rtcode = None
        self.err_msg = ""
    
    def run(self):
        try:
            start = timer()
            p = subprocess.Popen(self.args)
            p.wait()
            end = timer()
            
            self.time = end-start
            self.rtcode =  p.returncode
        except Exception as e:
            self.err_msg = str(e)
            self.rtcode = -999
    
    def get_rtcode(self) -> int:
        return self.rtcode
    
    def get_error(self) -> str:
        return self.err_msg
    
    def get_exec_time(self) -> int:
        return self.time