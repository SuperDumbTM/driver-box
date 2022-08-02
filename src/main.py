import sys
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main_drawer import *
from ui_main import Ui_mainWindow
from element_factory import ElementFactory
from configuration import Config        

class MyMainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.el = ElementFactory()
        
        # hardware info
        self.hwinfo = HwInfoDrawer(parent=self)
        self.refresh_hwinfo()
        self.hwinfo.trigger.connect(lambda create, text: self.hwInfoVBox.addWidget(create(text)))
        
        # driver options
        self.lanConf = Config(Config.lan)
        self.dpConf = Config(Config.display)
        self.othConf = Config(Config.other)
        for id, vals in self.lanConf.get_conf().items():
            self.lanDriverDd.addItem(vals['title'], id)
        for id, vals in self.dpConf.get_conf().items():
            self.displayDriverDd.addItem(vals['title'], id)
            
        self.otherCb = {}
        for id, vals in self.othConf.get_conf().items():
            self.otherCb.update({id: self.el.createCheckBox(id, vals['title'])})
            self.otherDriVBox.addWidget(self.otherCb[id])
        
        # event listener
        self.hwInfoRefreshBtn.clicked.connect(self.refresh_hwinfo)
        # self.lanDriverDd.activated.connect(lambda x: print(self.lanDriverDd.currentData()))
        # self.displayDriverDd.activated.connect(lambda x: print(self.displayDriverDd.currentData()))
        
    
    def refresh_hwinfo(self):
        for i in reversed(range(self.hwInfoVBox.count())): 
            self.hwInfoVBox.itemAt(i).widget().setParent(None)
        self.hwinfo.start()
    
    
        

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()