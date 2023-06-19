import os

from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from enums.install_progress import InstallProgress
from ui.progress import Ui_InstallProgress
from install.configuration import Driver


class ProgressWindow(Ui_InstallProgress, QtWidgets.QDialog):

    qsig_progress = QtCore.pyqtSignal(Driver, str, InstallProgress)
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

    def update_progress(self, driver: Driver, message: str, progress: InstallProgress):
        """Update the status of an "driver install progress\"

        Args:
            driver (Driver): the driver of the installation which the progress is belongs to
            message (str): installation progress of the driver
            level (str): message type of progress
        """
        item = QtWidgets.QTableWidgetItem(message)
        item.setBackground(self._status_color(progress))

        self.progr_table.setItem(self._progresses[driver.id], 1, item)
        self.progr_table.resizeRowsToContents()

    def clear_progresses(self) -> None:
        """Remove all "driver install progress" from the UI"""
        for i in range(self.progr_table.rowCount(), -1, -1):
            self.progr_table.removeRow(i)

    # override
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.qsig_close.emit()
        return super().closeEvent(a0)

    def _status_color(self, progress: InstallProgress) -> QtGui.QColor:
        """Gets the color to display for `status`

        Args:
            level (str): The status of the installation
        """
        if progress == InstallProgress.WARN:
            return QtGui.QColor(230, 207, 0, 255)
        elif progress == InstallProgress.PASS:
            return QtGui.QColor(0, 179, 12, 200)
        elif progress == InstallProgress.FAIL:
            return QtGui.QColor(171, 34, 34, 200)
        else:
            return QtGui.QColor(255, 255, 255, 1)
