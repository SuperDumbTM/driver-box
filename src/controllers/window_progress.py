import os

from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from install.execute_status import ExecuteStatus
from install.task import Task
from ui.progress import Ui_InstallProgress


class ProgressWindow(Ui_InstallProgress, QtWidgets.QDialog):

    qsig_progress = QtCore.pyqtSignal(Task, ExecuteStatus, str)
    qsig_window_close = QtCore.pyqtSignal()

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(
            os.path.join(definitions.DIR_PIC, "progress.ico")))
        # set table auto resize porpotion to window
        self.progr_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

        self.qsig_progress.connect(self.update_progress)
        self._progresses: dict[str, int] = {}

    def append_progress(self, task: Task, message: str) -> int:
        """Append and show a "driver install progress" to the UI

        Args:
            task (Task): The task of which the progress is belongs to
            message (str): Messages to be displayed

        Returns:
            int: Row index of appened progress on the UI
        """
        self.progr_table.insertRow(row := self.progr_table.rowCount())
        self.progr_table.setItem(
            row, 0, QtWidgets.QTableWidgetItem(task.name))
        self.progr_table.setItem(row, 1, QtWidgets.QTableWidgetItem(message))
        self._progresses.update({task.__hash__(): row})
        return row

    def update_progress(self, task: Task, progress: ExecuteStatus, message: str):
        """Update the status of an "driver install progress\"

        Args:
            task (Task): The task of which the progress is belongs to
            progress (str): Installation progress of the task
            message (str): Messages to be displayed
        """
        item = QtWidgets.QTableWidgetItem(message)
        item.setBackground(self._status_color(progress))

        self.progr_table.setItem(self._progresses[task.__hash__()], 1, item)
        self.progr_table.resizeRowsToContents()

    def clear_progresses(self) -> None:
        """Remove all progress from the UI
        """
        return
        for i in range(self.progr_table.rowCount(), -1, -1):
            self.progr_table.removeRow(i)

    # override
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.qsig_window_close.emit()
        return super().closeEvent(a0)

    def _status_color(self, progress: ExecuteStatus) -> QtGui.QColor:
        """Gets the color to display for `status`

        Args:
            level (str): Installation progress of the task
        """
        if progress == ExecuteStatus.EXITED:
            return QtGui.QColor(230, 207, 0, 255)
        elif progress == ExecuteStatus.SUCCESS:
            return QtGui.QColor(0, 179, 12, 200)
        elif progress in (ExecuteStatus.FAILED, ExecuteStatus.ABORTED, ExecuteStatus.ERROR):
            return QtGui.QColor(171, 34, 34, 200)
        else:
            return QtGui.QColor(255, 255, 255, 1)
