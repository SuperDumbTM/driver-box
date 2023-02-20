import time
import queue

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal

try:
    from task import Task
    from window_progress import ProgressWindow
except ImportError:
    from .task import Task
    from window_progress import ProgressWindow

class InstallManager(QThread):
    
    qsig_msg: pyqtSignal
    qsig_progr: pyqtSignal
    tasks: queue.Queue[Task]
    
    qsig_success = pyqtSignal(bool)
    
    def __init__(self,
                 qsig_msg: pyqtSignal,
                 qsig_progr: pyqtSignal,
                 parent = None) -> None:
        super().__init__(parent)
        self.qsig_msg = qsig_msg
        self.qsig_progr = qsig_progr
        self.tasks = queue.Queue()
            
    def add_task(self, task: Task) -> None:
        """insert new install task to install queue"""
        self.tasks.put_nowait(task)
        
    def is_finished(self) -> bool:
        return self.tasks.qsize() == 0
    
    def auto_install(self):
        fails = []
        pbar = ("-","\\","|","/")
        
        # ---------- start tasks ----------
        while self.tasks.qsize() != 0:
            task = self.tasks.get()

            try:
                self.qsig_msg.emit(f"[{task.driver.name}] 開始執行")
                # ---------- start thread ----------
                i = 0
                task.start()
                while not task.finished:
                    time.sleep(0.1)
                    self.qsig_progr.emit(task.driver, pbar[i % len(pbar)], ProgressWindow.INFO)
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
                        self.qsig_progr.emit(task.driver, "執行時間小於5秒，錯誤", ProgressWindow.WARN)
                    else:
                        self.qsig_progr.emit(task.driver, f"失敗，錯誤代碼：[{task.rtcode}]", ProgressWindow.FAIL)                
                else:
                    self.qsig_progr.emit(task.driver, "完成", ProgressWindow.PASS)
                # ---------- end thread ----------
                self.qsig_msg.emit(f"[{task.driver.name}] 完成執行")
            except Exception as e:
                fails.append(task)
                self.qsig_msg.emit(f"{task.driver.name} {e}")
                # self.qsig_progr.emit(task.driver, f"程式出錯\n{e}", ProgressWindow.FAIL)
        # ---------- finish all task ----------
        
        self.qsig_success.emit(len(fails) <= 0)
        if len(fails) > 0:
            while len(fails):
                self.tasks.put(fails.pop(0))
            self.manual_install()
        
    def manual_install(self):
        while self.tasks.qsize() > 0:
            try:
                task = self.tasks.get()
                task.execute()
                self.qsig_msg.emit(f"[{task.driver.name}] 已開啟安裝程式")
            except Exception as e:
                self.qsig_msg.emit(f"[{task.driver.name}] {e}")