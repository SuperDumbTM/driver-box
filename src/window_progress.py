import os

from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from ui.progress import Ui_InstallProgress
from install.configuration import Driver


class ProgressWindow(Ui_InstallProgress, QtWidgets.QDialog):

    INFO = "Progress.INFO"
    WARN = "Progress.WARN"
    PASS = "Progress.PASS"
    FAIL = "Progress.FAIL"

    qsig_progress = QtCore.pyqtSignal(Driver, str, str)
    qsig_close = QtCore.pyqtSignal()

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

    def append_progress(self, driver: Driver, message: str) -> int:
        """Append and show a "driver install progress" to the UI

        Args:
            driver (Driver): the driver of the installation which the progress is belongs to
            message (str): installation progress of the driver

        Returns:
            int: row index of appened progress on the UI
        """
        self.progr_table.insertRow(row := self.progr_table.rowCount())
        self.progr_table.setItem(
            row, 0, QtWidgets.QTableWidgetItem(driver.name))
        self.progr_table.setItem(row, 1, QtWidgets.QTableWidgetItem(message))
        self._progresses.update({driver.id: row})
        return row

    def update_progress(self, driver: Driver, message: str, level: str):
        """Update the status of an "driver install progress\"

        Args:
            driver (Driver): the driver of the installation which the progress is belongs to
            message (str): installation progress of the driver
            level (str): message type of progress
        """
        item = QtWidgets.QTableWidgetItem(message)
        item.setBackground(self._status_color(level))
        self.progr_table.setItem(self._progresses[driver.id], 1, item)

        self.progr_table.resizeRowsToContents()

    def clear_progress(self) -> None:
        """Remove all existing "driver install progress" from the UI"""
        for i in range(self.progr_table.rowCount(), -1, -1):
            self.progr_table.removeRow(i)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.qsig_close.emit()
        return super().closeEvent(a0)

    def _status_color(self, level: str) -> QtGui.QColor:
        if level == self.WARN:
            return QtGui.QColor(230, 207, 0, 255)
        elif level == self.PASS:
            return QtGui.QColor(0, 179, 12, 200)
        elif level == self.FAIL:
            return QtGui.QColor(171, 34, 34, 200)
        else:
            return QtGui.QColor(255, 255, 255, 1)
