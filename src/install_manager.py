import time
import queue
from task import Task
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal

class InstallManager(QThread):
    
    _progress =  pyqtSignal(str, QWidget)
    _finish = pyqtSignal(str)
    _status = pyqtSignal(str)
    
    def __init__(self, parent = None) -> None:
        self.tasks = queue.Queue(QThread)
        self.error = False
        super().__init__(parent)
            
    def add_task(self, label: QWidget, cmd: list, kwargs: dict = None):
        """insert new install task to install queue

        Args:
                `label` (QLabel) to-be updated text label (progress)
                `args` (list) installer executable path, flags
                `kwargs` (dict) argurment for subprocess.Popen
        """
        self.tasks.put_nowait((Task(cmd, kwargs), label))
        
    def is_finished(self) -> bool:
        return self.tasks.qsize() == 0
    
    def execute(self, label: QWidget, cmd: list, **kwargs):
        Task(cmd, kwargs).execute()
        self._finish.emit("已開啟安裝程式", label)
    
    def auto_install(self):
        fails = []
        progress = ("-","\\","|","/")
        while self.tasks.qsize() != 0:
            task: tuple[Task, QWidget] = self.tasks.get()
            thd = task[0]
            
            i = 0
            thd.start()
            while thd.rtcode is None:
                time.sleep(0.1)
                self._progress.emit(progress[i % len(progress)], task[1])
                # task[1].setText(process[i % len(process)])
                i += 1
            """    
            Intel igfx
            13: a system restart is needed before setup can continue
            14: setup has completed successfully but a system restart is required
            15: setup has completed successfully and a system restart has been initiated
            Custom return code
            -999: exception occurs during installing
            """
            if thd.rtcode not in (0, 13, 14, 15):
                if thd.rtcode == -999:
                    self._progress.emit(f"程式出錯\n{thd.err_msg}", task[1])
                    # task[1].setText(f"程式出錯\n{thd.err_msg}")
                else:
                    self._progress.emit(f"失敗，錯誤代碼：[{thd.rtcode}]", task[1])
                    # task[1].setText(f"失敗，錯誤代碼：[{thd.rtcode}]")
                fails.append(task)
                self.error = True
            elif thd.time <= 5:
                self._finish.emit("執行時間小於5秒，錯誤", task[1])
                # task[1].setText("執行時間小於5秒，錯誤")
                fails.append(task)
                self.error = True
            else:
                self._finish.emit("完成", task[1])
                # task[1].setText("完成")
                
        if self.error:
            for task in fails: self.tasks.put(task)
            self.error = False
            self.manual_install()
        
    def manual_install(self):
        while self.tasks.qsize() != 0:
            task: dict[list, QWidget] = self.tasks.get()
            # self.execute(task[1], task[0])
            self._finish.emit("已開啟安裝程式", task[1])
            # task[0].start()
            # task[1].setText("已開啟安裝程式")