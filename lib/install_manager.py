import threading
import subprocess
import time
import tkinter as tk
from timeit import default_timer as timer


class AutoInstallManager(threading.Thread):
    
    _instance = None
    
    @staticmethod
    def get_instance():
        if AutoInstallManager._instance is None:
            AutoInstallManager()
        return AutoInstallManager._instance
    
    def __init__(self) -> None:
        if AutoInstallManager._instance is not None:
            raise Exception('Singleton class, use InstallManager.get_instance() instead')
        else:
            self.task_list = []
            self.finished = False
            self.error = False
            self.fail_proc = []
            super().__init__()
            AutoInstallManager._instance = self         
        
    def add_task(self, dets: dict):
        self.task_list.append(dets)
    
    def run(self):
        for task in self.task_list:
            t = InstallThread(task['args'])
            task['stat_var'].set("安裝中")
            t.start()
            
            # progress visuals
            proc_str = ["-","\\","|","/"]
            i = 0
            while t.get_rtcode() is None:
                idx = i%len(proc_str)
                task['stat_var'].set(proc_str[idx])
                i += 1
                time.sleep(0.1)
            
            print(t.get_rtcode())
            # Intel igfx
            # 13: a system restart is needed before setup can continue
            # 14: setup has completed successfully but a system restart is required
            # 15: setup has completed successfully and a system restart has been initiated
            # Custom return code
            # -999: exception occurs during installing
            if t.get_rtcode() not in (0, 13, 14, 15):
                if t.get_rtcode() == -999:
                    task['stat_var'].set("程式出錯\n" + t.get_error())
                else:
                    task['stat_var'].set("失敗")
                self.fail_proc.append(task['args'])
                self.error = True
            elif t.get_exec_time() <= 5:
                task['stat_var'].set("執行時間小於5秒，錯誤")
                self.fail_proc.append(task['args'])
                self.error = True
            else:
                task['stat_var'].set("完成")
        
        self.finished = True
        
    def is_finished(self) -> bool:
        return self.finished
    
    def has_error(self) -> bool:
        return self.error
    
    def get_fail_proc(self) -> list:
        return self.fail_proc       
            

class InstallThread(threading.Thread):
    
    def __init__(self, args: list) -> None:
        super().__init__()
        self.args = args
        self.__returncode = None
        self.exec_time = 0
        self.exception_msg = ""
        
    def run(self):
        try:
            start = timer()
            p = subprocess.Popen(self.args)
            p.wait()
            end = timer()
            
            self.exec_time = end-start
            self.__returncode =  p.returncode
        except Exception as e:
            self.exception_msg = str(e)
            self.__returncode = -999
    
    def get_rtcode(self) -> int:
        return self.__returncode
    
    def get_error(self) -> str:
        return self.exception_msg
    
    def get_exec_time(self) -> int:
        print(self.exec_time)
        return self.exec_time