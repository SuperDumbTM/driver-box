import time
import queue
import threading
import itertools
import multiprocessing

from PyQt5 import QtCore

try:
    from task import Task
    from window_progress import ProgressWindow
except ImportError:
    from .task import Task
    from window_progress import ProgressWindow


class InstallManager(QtCore.QObject):  # inherit QObject to use pyqtSignal
    
    qsig_msg: QtCore.pyqtSignal
    qsig_progr: QtCore.pyqtSignal
    
    todos: queue.Queue[Task]
    live_tasks: dict[str, Task]
    fails: list[Task]
    
    qsig_successful = QtCore.pyqtSignal(bool)
    
    def __init__(self,
                 qsig_msg: QtCore.pyqtSignal,
                 qsig_progr: QtCore.pyqtSignal,
                 parent = None) -> None:
        super().__init__(parent)
        self.qsig_msg = qsig_msg
        self.qsig_progr = qsig_progr
        
        self.tasks: list[Task] = []
        self.todos = queue.Queue()
        self.live_tasks = {}
        self.fails: list[Task] = []
            
    def add_task(self, task: Task) -> None:
        """insert new install task to install queue"""
        self.tasks.append(task)
        self.todos.put_nowait(task)
        
    def is_finished(self) -> bool:
        return self.todos.qsize() == 0 and len(self.live_tasks) == 0
    
    def auto_install(self, paralle: bool):     
        # ---------- start tasks ----------
        while self.todos.qsize() != 0:
            if paralle:
                threading.Thread(
                    target=self.__at_helper, args=[self.todos.get()], daemon=True).start()
            else:
                self.__at_helper(self.todos.get())
        
        while paralle and any([t.is_alive() for t in self.live_tasks.values()]):
            time.sleep(1)
        
        # ---------- finish all task ----------
        for t in self.tasks:
            print(t.is_aborted)

        self.qsig_successful.emit(
            not any([t.is_aborted for t in self.tasks])
            and len(self.fails) <= 0
        )
        
        while len(self.fails) > 0:
            self.todos.put(self.fails.pop(0))
        self.manual_install()
    
    def __at_helper(self, task: Task):
        pbar = ("-", "\\", "|", "/")
        self.live_tasks[task.__hash__()] = task
        try:
            self.qsig_msg.emit(f"開始安裝 {task.driver.name}")
            # ---------- start thread ----------
            task.execute()
            exe_time = time.time()
            for i in itertools.count():
                if not task.is_alive():
                    break
                time.sleep(0.1)
                self.qsig_progr.emit(task.driver, pbar[i % len(pbar)], ProgressWindow.INFO)
            exe_time = time.time() - exe_time
            
            # emit message from the executable
            for message in task.messages:
                self.qsig_msg.emit(f"{task.driver.name}\uff1a{message}")
            
            """    
            Intel igfx
            13: a system restart is needed before setup can continue
            14: setup has completed successfully but a system restart is required
            15: setup has completed successfully and a system restart has been initiated
            """
            if task.is_aborted:
                self.qsig_progr.emit(task.driver, "已取消", ProgressWindow.WARN)
            elif task.rtcode not in (0, 13, 14, 15) or exe_time <= 5:
                self.fails.append(task)
                if exe_time <= 5 and task.rtcode is None:
                    self.qsig_progr.emit(task.driver, "執行時間小於5秒，錯誤", ProgressWindow.WARN)
                else:
                    self.qsig_progr.emit(task.driver, f"失敗，錯誤代碼：[{task.rtcode}]", ProgressWindow.FAIL)
            else:
                self.qsig_progr.emit(task.driver, "完成", ProgressWindow.PASS)
            # ---------- end thread ----------
        except Exception as e:
            self.fails.append(task)
            self.qsig_progr.emit(task.driver, "失敗", ProgressWindow.FAIL)
            self.qsig_msg.emit(f"{e} ({task.driver.name})")
        finally:
            # self.qsig_msg.emit(f"[{task.driver.name}] 完成安裝")
            self.live_tasks.pop(task.__hash__())
            pass
            
    def manual_install(self):
        while self.todos.qsize() > 0:
            task = self.todos.get()
            try:
                task.execute_pure()
                self.qsig_msg.emit(f"已開啟 {task.driver.name}")
            except Exception as e:
                self.qsig_msg.emit(f"{e} ({task.driver.name})")
                
    def abort(self):
        self.fails = []
        with self.todos.mutex:
            self.todos.queue.clear()
        
        for task in self.tasks:
            self.qsig_msg.emit(f"終止執行 {task.driver.name}")
            task.abort()
