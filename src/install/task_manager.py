import time
from threading import Thread
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
    qsig_install_result = QtCore.pyqtSignal(ExecuteStatus)

    tasks: list[Task]

    def __init__(self,
                 qsig_msg: QtCore.pyqtSignal,
                 qsig_progr: QtCore.pyqtSignal,
                 parent=None) -> None:
        super().__init__(parent)
        self.qsig_msg = qsig_msg
        self.qsig_progr = qsig_progr

        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Insert a new task
        """
        self.tasks.append(task)

    def clear_tasks(self):
        """Remove all tasks
        """
        self.tasks.clear()

    def abort_tasks(self):
        """Terminate all tasks
        """
        for task in (t for t in self.tasks if t.status in (ExecuteStatus.PENDING, ExecuteStatus.INPROGRESS)):
            task.abort()
            if task.status != ExecuteStatus.ABORTED:
                self.qsig_msg.emit(f"未能終止 {task.name}\uff01")
            else:
                self.qsig_msg.emit(f"已終止執行 {task.name}")

    def is_finished(self) -> bool:
        """Returns whether all task are already executed
        """
        return all((task.status not in (ExecuteStatus.PENDING, ExecuteStatus.INPROGRESS)
                    for task in self.tasks))

    def auto_install(self, man_fallback: bool, paralle: bool) -> None:
        # ---------- start tasks ----------
        if paralle:
            threads: list[Thread] = []
            for task in self.tasks:
                threads.append(Thread(target=self.__at_worker,
                               args=[task], daemon=True))
                threads[-1].start()
            while any((t.is_alive() for t in threads)):
                time.sleep(1)
        else:
            for task in self.tasks:
                self.__at_worker(task)

        # ---------- finish all task ----------
        if any((t.is_aborted for t in self.tasks)):
            return self.qsig_install_result.emit(ExecuteStatus.ABORTED)
        elif any((t.status != ExecuteStatus.SUCCESS for t in self.tasks)):
            if man_fallback:
                self.qsig_msg.emit("有工作執行失敗，將以手動安裝模式重試")
                self.retry_install()
            return self.qsig_install_result.emit(ExecuteStatus.FAILED)
        else:
            self.qsig_msg.emit("已完成所有選擇的工作")
            return self.qsig_install_result.emit(ExecuteStatus.SUCCESS)

    def manual_install(self):
        for task in (t for t in self.tasks if t.status == ExecuteStatus.PENDING):
            self.qsig_msg.emit(f"開始安裝 {task.name} (手動模式)")
            try:
                Thread(target=task.execute, args=(True,), daemon=False).start()
            except Exception as e:
                self.qsig_msg.emit(f"{e} ({task.name})")

    def retry_install(self, no_options: bool = True):
        """Re-execute all the failed tasks

        Args:
            no_options (bool, optional): Whether to include the "execution options/flags" to the execution. \
                Defaults to True.
        """
        for task in (
            t for t in self.tasks if t.status not in (
                ExecuteStatus.SUCCESS, ExecuteStatus.INPROGRESS, ExecuteStatus.ABORTED)
        ):
            if not task.exe_conf.retryable:
                continue
            self.qsig_msg.emit(f"開始重試 {task.name} (手動模式)")
            try:
                Thread(
                    target=task.execute,
                    args=(no_options,),
                    daemon=False).start()
            except Exception as e:
                self.qsig_msg.emit(f"{e} ({task.name})")

    def __at_worker(self, task: Task):
        if task.is_aborted:
            return
        self.qsig_msg.emit(f"開始執行 {task.name} (自動模式)")

        t = Thread(target=task.execute, daemon=True)
        t.start()
        for i in itertools.count():
            if not t.is_alive():
                break
            try:
                self.qsig_progr.emit(task, task.status, _PBAR[i % len(_PBAR)])
                time.sleep(0.12)
            except AttributeError:
                # the ProgressWindow have been closed
                break
            except KeyError:
                # task not exists in the ProgressWindow
                pass
        t.join()

        # emit message from the executable
        for message in task.messages:
            self.qsig_msg.emit(f"{task.name}\uff1a{message}")

        try:
            if task.status == ExecuteStatus.ABORTED:
                self.qsig_progr.emit(task, task.status, "已取消")
            elif task.status == ExecuteStatus.ERROR:
                self.qsig_progr.emit(task, task.status, str(task.exception))
            elif task.status == ExecuteStatus.EXITED:
                self.qsig_progr.emit(
                    task,
                    task.status,
                    f"執行時間小於{task.exe_conf.fail_time}秒")
            elif task.status == ExecuteStatus.FAILED:
                self.qsig_progr.emit(
                    task,
                    ExecuteStatus.FAILED,
                    f"失敗，錯誤代碼：[{task.rtcode}]")
            else:
                self.qsig_progr.emit(task, ExecuteStatus.SUCCESS, "完成")
        except AttributeError:
            # the ProgressWindow have been closed
            pass
