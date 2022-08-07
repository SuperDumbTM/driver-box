from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor

from ui_progress import Ui_InstallProgress
from element_factory import ElementFactory

class Progress(Ui_InstallProgress, QWidget):
    
    INFO = "Progress.INFO"
    WARN = "Progress.WARN"
    PASS = "Progress.PASS"
    FAIL = "Progress.FAIL"
    
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.el = ElementFactory()
        self.progressTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self._progresses: dict[str, int] = {}
        
    def add_progress(self, iden, driver: str, status: str) -> int:
        row = self.progressTable.rowCount()
        self.progressTable.insertRow(row)
        self.progressTable.setItem(row , 0, QTableWidgetItem(driver))
        self.progressTable.setItem(row , 1, QTableWidgetItem(status))
        self._progresses.update({iden: row})
        return row
    
    def update_progress(self, iden: str, text: str, level: str):
        item = QTableWidgetItem(text)
        item.setBackground(self.__get_color(level))  
        self.progressTable.setItem(self._progresses[iden], 1, item)
        
    def __get_color(self, level: str) -> QColor:
        if level == self.WARN:
            return QColor(230, 207, 0, 255)
        elif level == self.PASS:
            return QColor(0, 179, 12, 200)
        elif level == self.FAIL:
            return QColor(171, 34, 34, 200)
        else:
            return QColor(255, 255, 255, 1)