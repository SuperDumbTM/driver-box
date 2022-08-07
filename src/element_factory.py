from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ElementFactory:
    
    def createHwInfoTitle(self, text: str):
        font = QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(10)
        font.setWeight(font.ExtraBold)
        
        label = QLabel(text)
        label.setFont(font)
        return label
    
    def createHwInfoText(self, text: str):
        font = QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(10)
        
        label = QLabel(text)
        label.setFont(font)
        label.setStyleSheet('color: #545454')
        return label
    
    def createCheckBox(self, id: str, text: str):
        cb = QCheckBox(id)
        cb.setObjectName(f"{id}Cb")
        cb.setText(text)
        return cb
    
    def createTableItem(self, text: str):
        return QTableWidgetItem(text)