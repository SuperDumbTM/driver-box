from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from ui_progress import Ui_InstallProgress
from element_factory import ElementFactory

class Progress(Ui_InstallProgress, QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.treeWidget.header().setSectionResizeMode(QHeaderView.Fixed)
    
    def add_items(self):
        rowcount = self.treeWidget.topLevelItemCount()
        self.treeWidget.addTopLevelItem(QTreeWidgetItem(rowcount))
        
        self.treeWidget.topLevelItem(rowcount).setText(0, 'Lincoln a good boy')
        self.treeWidget.topLevelItem(rowcount).setCheckState(0, QtCore.Qt.Unchecked)
        self.treeWidget.topLevelItem(rowcount).setFlags(
            self.treeWidget.topLevelItem(rowcount).flags() | QtCore.Qt.ItemIsUserCheckable)
        self.treeWidget.topLevelItem(rowcount).setText(1, 'He added a second column')
        self.treeWidget.topLevelItem(rowcount).setTextAlignment(0, QtCore.Qt.AlignHCenter)
        self.treeWidget.topLevelItem(rowcount).setTextAlignment(1, QtCore.Qt.AlignHCenter)