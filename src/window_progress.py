from PyQt5 import QtCore, QtGui, QtWidgets

from ui.progress import Ui_InstallProgress
from ui.element_factory import ElementFactory
from install.configuration import Driver

class ProgressWindow(Ui_InstallProgress, QtWidgets.QWidget):
    
    INFO = "Progress.INFO"
    WARN = "Progress.WARN"
    PASS = "Progress.PASS"
    FAIL = "Progress.FAIL"
    
    qsig_progress = QtCore.pyqtSignal(Driver, str, str)
    
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        # set table auto resize porpotion to window
        self.progr_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.qsig_progress.connect(self.update_progress)
        self._progresses: dict[str, int] = {}
        
    def append_progress(self, driver: Driver, progress: str) -> int:
        row = self.progr_table.rowCount()
        self.progr_table.insertRow(row)
        self.progr_table.setItem(row , 0, QtWidgets.QTableWidgetItem(driver.name))
        self.progr_table.setItem(row , 1, QtWidgets.QTableWidgetItem(progress))
        self._progresses.update({driver.id: row})
        return row
    
    def update_progress(self, driver: Driver, status: str, level: str):
        item = QtWidgets.QTableWidgetItem(status)
        item.setBackground(self.__get_color(level))
        self.progr_table.setItem(self._progresses[driver.id], 1, item)
        
        self.progr_table.resizeRowsToContents()
    
    def clear_progress(self) -> None:
        for i in range(self.progr_table.rowCount(), -1, -1):
            self.progr_table.removeRow(i)
        
    def __get_color(self, level: str) -> QtGui.QColor:
        if level == self.WARN:
            return QtGui.QColor(230, 207, 0, 255)
        elif level == self.PASS:
            return QtGui.QColor(0, 179, 12, 200)
        elif level == self.FAIL:
            return QtGui.QColor(171, 34, 34, 200)
        else:
            return QtGui.QColor(255, 255, 255, 1)