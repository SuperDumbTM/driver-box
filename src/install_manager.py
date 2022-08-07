import time
import queue

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal

from task import Task
from progress import Progress

class InstallManager(QThread):
    
    _progress =  pyqtSignal(str, str, str)
    _print = pyqtSignal(str)
    _success = pyqtSignal(bool)
    
    def __init__(self, parent = None) -> None:
        self.tasks = queue.Queue()
        super().__init__(parent)
            
    def add_task(self, iden: str, cmd: list, kwargs: dict = None):
        """insert new install task to install queue

        Args:
                `label` (QLabel) to-be updated text label (progress)
                `args` (list) installer executable path, flags
                `kwargs` (dict) argurment for subprocess.Popen
        """
        self.tasks.put_nowait((Task(iden, self._print, cmd, kwargs)))
        
    def is_finished(self) -> bool:
        return self.tasks.qsize() == 0
    
    def execute(self, cmd: list, **kwargs):
        Task(cmd, kwargs).execute()
        self._print.emit(f"已開啟 {str(cmd[1:])}")
    
    def auto_install(self):
        fails = []
        pbar = ("-","\\","|","/")
        
        # ---------- start tasks ----------
        while self.tasks.qsize() != 0:
            task: Task = self.tasks.get()
            
            try:
                self._print.emit(f"[{task.iden}] 開始執行")
                # ---------- start thread ----------
                i = 0
                task.start()
                while task.rtcode is None:
                    time.sleep(0.1)
                    self._progress.emit(task.iden, pbar[i % len(pbar)], Progress.INFO)
                    i += 1
                
                """    
                Intel igfx
                13: a system restart is needed before setup can continue
                14: setup has completed successfully but a system restart is required
                15: setup has completed successfully and a system restart has been initiated
                Custom return code
                -999: exception occurs during installing
                """
                if task.rtcode not in (0, 13, 14, 15) or task.time <= 5:
                    fails.append(task)
                    if task.time <= 5:
                        self._progress.emit(task.iden, "執行時間小於5秒，錯誤", Progress.WARN)
                    else:
                        self._progress.emit(task.iden, f"失敗，錯誤代碼：[{task.rtcode}]", Progress.FAIL)                
                else:
                    self._progress.emit(task.iden, "完成", Progress.PASS)
                # ---------- end thread ----------
                self._print.emit(f"[{task.iden}] 完成執行")
            except Exception as e:
                fails.append(task)
                self._print.emit(task.iden, e)
                self._progress.emit(task.iden, f"程式出錯\n{e}", Progress.FAIL)
        # ---------- finish all task ----------
        
        self._success.emit(len(fails) == 0)
        if len(fails) > 0:
            while len(fails): self.tasks.put(fails.pop(0))
            self.manual_install()
        
    def manual_install(self):
        while self.tasks.qsize() != 0:
            task: Task = self.tasks.get()
            task.execute()
            self._print.emit(f"[{task.iden}] 已開啟安裝程式")