import time
import queue
from task import Task
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal

class InstallManager(QThread):
    
    _progress =  pyqtSignal(str)
    _finish = pyqtSignal(str)
    _print = pyqtSignal(str)
    _success = pyqtSignal(bool)
    
    def __init__(self, parent = None) -> None:
        self.tasks = queue.Queue()
        self.error = False
        super().__init__(parent)
            
    def add_task(self,cmd: list, kwargs: dict = None):
        """insert new install task to install queue

        Args:
                `label` (QLabel) to-be updated text label (progress)
                `args` (list) installer executable path, flags
                `kwargs` (dict) argurment for subprocess.Popen
        """
        self.tasks.put_nowait((Task(cmd, kwargs)))
        
    def is_finished(self) -> bool:
        return self.tasks.qsize() == 0
    
    def execute(self, cmd: list, **kwargs):
        Task(cmd, kwargs).execute()
        self._print.emit(f"已開啟 {str(cmd[1:])}")
    
    def auto_install(self):
        fails = []
        progress = ("-","\\","|","/")
        while self.tasks.qsize() != 0:
            task: Task = self.tasks.get()
            
            i = 0
            task.start()
            while task.rtcode is None:
                time.sleep(0.1)
                self._progress.emit(progress[i % len(progress)])
                i += 1
            """    
            Intel igfx
            13: a system restart is needed before setup can continue
            14: setup has completed successfully but a system restart is required
            15: setup has completed successfully and a system restart has been initiated
            Custom return code
            -999: exception occurs during installing
            """
            if task.rtcode not in (0, 13, 14, 15):
                if task.rtcode == -999:
                    self._progress.emit(f"程式出錯\n{task.err_msg}")
                else:
                    self._progress.emit(f"失敗，錯誤代碼：[{task.rtcode}]")
                fails.append(task)
                self.error = True
            elif task.time <= 5:
                self._progress.emit("執行時間小於5秒，錯誤")
                fails.append(task)
                self.error = True
            else:
                self._progress.emit("完成")
        
        self._success.emit(len(fails) == 0)
        if self.error:
            for task in fails: self.tasks.put(task)
            self.error = False
            self.manual_install()
        
    def manual_install(self):
        while self.tasks.qsize() != 0:
            task: Task = self.tasks.get()
            task.execute()
            self._print.emit("已開啟安裝程式")