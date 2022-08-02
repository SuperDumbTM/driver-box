import threading
import subprocess
import time
import queue
from task import Task
from PyQt5.QtWidgets import QLabel

class InstallManager:
    _instance = None
    
    @staticmethod
    def get_instance():
        if InstallManager._instance is None:
            InstallManager()
        return InstallManager._instance
    
    def __init__(self) -> None:
        if InstallManager._instance is not None:
            return InstallManager.get_instance()
            # raise Exception('Singleton class, use InstallManager.get_instance() instead')
        else:
            self.tasks = queue.Queue()
            self.error = False
            super().__init__()
            InstallManager._instance = self
            
    def add_task(self, task: dict[list, QLabel]):
        self.tasks.put_nowait(task)
        
    def is_finished(self) -> bool:
        return self.tasks.qsize() == 0
    
    def auto_install(self):
        fails = []
        process = ["-","\\","|","/"]
        while self.tasks.qsize() != 0:
            task: dict[list, QLabel] = self.tasks.get()
            thd = Task(task['args'])
            
            i = 0
            thd.start()
            while thd.get_rtcode() is None:
                time.sleep(0.1)
                task['label'].setText(process[i % len(process)])
                i += 1
                
            # Intel igfx
            # 13: a system restart is needed before setup can continue
            # 14: setup has completed successfully but a system restart is required
            # 15: setup has completed successfully and a system restart has been initiated
            # Custom return code
            # -999: exception occurs during installing
            if thd.get_rtcode() not in (0, 13, 14, 15):
                if thd.get_rtcode() == -999:
                    task['label'].setText(f"程式出錯\n{thd.get_error()}")
                else:
                    task['label'].setText(f"失敗，錯誤代碼：[{thd.get_rtcode()}]")
                fails.append(task)
                self.error = True
            elif thd.get_exec_time() <= 5:
                task['label'].setText("執行時間小於5秒，錯誤")
                fails.append(task)
                self.error = True
            else:
                task['label'].setText("完成")
                
        if self.error:
            for task in fails: self.tasks.put(task)
            self.manual_install()
        
        
    def manual_install(self):
        while self.tasks.qsize() != 0:
            task: dict[list, QLabel] = self.tasks.get()
            Task(task['args'][0]).start()
            task['label'].setText("已開啟安裝程式")
    
    def execute(self, args: list, kwargs):
        return subprocess.Popen(args, kwargs)