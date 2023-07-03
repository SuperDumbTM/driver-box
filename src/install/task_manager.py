import time
import threading
import itertools

from PyQt5 import QtCore

try:
    from execute_status import ExecuteStatus
    from task import Task
except ImportError:
    from .execute_status import ExecuteStatus
    from .task import Task


_PBAR = ("-", "\\", "|", "/")


class TaskManager(QtCore.QObject):  # inherit QObject to use pyqtSignal
    
    qsig_msg: QtCore.pyqtSignal
    qsig_progr: QtCore.pyqtSignal
    
    tasks: list[Task]
    
    qsig_install_result = QtCore.pyqtSignal(ExecuteStatus)
    
    def __init__(self,
                 qsig_msg: QtCore.pyqtSignal,
                 qsig_progr: QtCore.pyqtSignal,
                 parent = None) -> None:
        super().__init__(parent)
        self.qsig_msg = qsig_msg
        self.qsig_progr = qsig_progr
        
        self.tasks: list[Task] = []
        
    def __len__(self) -> int:
        return len(self.tasks)
            
    def add_task(self, task: Task) -> None:
        """Insert a new task to the queue"""
        self.tasks.append(task)
    
    def clear_tasks(self):
        """Remove all tasks from the queue"""
        self.tasks.clear()
        
    def abort_tasks(self):
        """Terminate all tasks"""
        for task in (t for t in self.tasks if t.status in (ExecuteStatus.PENDING, ExecuteStatus.INPROGRESS)):
            task.abort()
            if task.status != ExecuteStatus.ABORTED:
                self.qsig_msg.emit(f"未能終止 {task.name}\uff01")
            else:
                self.qsig_msg.emit(f"已終止執行 {task.name}")
        
    def is_finished(self) -> bool:
        return all((task.status not in (ExecuteStatus.PENDING, ExecuteStatus.INPROGRESS)
                    for task in self.tasks))
    
    def auto_install(self, man_fallback: bool, paralle: bool):
        # ---------- start tasks ----------
        for task in self.tasks:
            if paralle:
                threading.Thread(
                    target=self.__at_helper, args=[task], daemon=True).start()
            else:
                self.__at_helper(task)
        
        while paralle and any((t.status == ExecuteStatus.PENDING or
                               t.is_alive() for t in self.tasks)):
            time.sleep(1)
        
        # ---------- finish all task ----------
        if any((t.is_aborted for t in self.tasks)):
            return self.qsig_install_result.emit(ExecuteStatus.ABORTED)
        elif any((t.status != ExecuteStatus.SUCCESS for t in self.tasks)):
            if man_fallback:
                self.qsig_msg.emit("有工作執行失敗，將以手動安裝模式重試")
            self.manual_install()
            return self.qsig_install_result.emit(ExecuteStatus.FAILED)
        else:
            self.qsig_msg.emit("已完成所有選擇的工作")
            return self.qsig_install_result.emit(ExecuteStatus.SUCCESS)
    
    def __at_helper(self, task: Task):
        if task.is_aborted:
            return
        self.qsig_msg.emit(f"開始執行 {task.name} (自動模式)")
        
        t = threading.Thread(target=task.execute, daemon=True)
        t.start()
        for i in itertools.count():
            time.sleep(0.1)
            if not task.is_alive():
                break
            self.qsig_progr.emit(
                task, ExecuteStatus.INPROGRESS, _PBAR[i % len(_PBAR)])
        t.join()
        
        # emit message from the executable
        for message in task.messages:
            self.qsig_msg.emit(f"{task.name}\uff1a{message}")
        
        """    
        Intel igfx
        13: a system restart is needed before setup can continue
        14: setup has completed successfully but a system restart is required
        15: setup has completed successfully and a system restart has been initiated
        """
        if task.is_aborted:
            self.qsig_progr.emit(
                task, ExecuteStatus.ABORTED, "已取消")
        elif task.status == ExecuteStatus.EXITED:
            self.qsig_progr.emit(
                task,
                task.status,
                f"執行時間小於{task.exe_conf.fail_time}秒")
        elif task.exception is not None:
            self.qsig_progr.emit(task, task.status, "失敗")
            self.qsig_msg.emit(f"[{task.name}] {task.exception}")
        elif task.rtcode not in (0, 13, 14, 15):
            self.qsig_progr.emit(
                task,
                ExecuteStatus.FAILED,
                f"失敗，錯誤代碼：[{task.rtcode}]")
        else:
            self.qsig_progr.emit(task, ExecuteStatus.SUCCESS, "完成")
            
    def manual_install(self):
        for task in (t for t in self.tasks if t.status
                     in (ExecuteStatus.PENDING, ExecuteStatus.FAILED)):
            self.qsig_msg.emit(f"開始安裝 {task.name} (手動模式)")
            try:
                task.execute(no_options=True)
            except Exception as e:
                self.qsig_msg.emit(f"{e} ({task.name})")
