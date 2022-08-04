import sys
import string
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from worker import *
from ui_main import Ui_mainWindow
from progress import Progress
from configuration import Config     
from install_manager import InstallManager
from element_factory import ElementFactory

class MyMainWindow(Ui_mainWindow, QMainWindow):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.el = ElementFactory()
        self.mgt = InstallManager()
        self.progs = Progress()
        self.hwinfo = HwInfoWorker(parent=self)
        
        # ----- hardware info -----
        self.refresh_hwinfo()        
        # ----- driver options -----
        self.lanConf = Config(Config.lan)
        for id, vals in self.lanConf.get_conf().items():
            self.lanDriverDd.addItem(vals['title'], id)
            
        self.dpConf = Config(Config.display)
        for id, vals in self.dpConf.get_conf().items():
            self.displayDriverDd.addItem(vals['title'], id)
            
        self.othConf = Config(Config.other)
        self.otherCbs = {}
        for id, vals in self.othConf.get_conf().items():
            self.otherCbs.update({id: self.el.createCheckBox(id, vals['title'])})
            self.otherDriVBox.addWidget(self.otherCbs[id])
        
        # ----- event listener -----
        self.hwInfoRefreshBtn.clicked.connect(self.refresh_hwinfo)
        self.diskMgtBtn.clicked.connect(lambda x: self.mgt.execute(["start", "diskmgmt.msc"], shell=True))
        self.installBtn.clicked.connect(self.install)
        # ----- signal handler -----
        self.mgt._print.connect(self.stdout)
        self.mgt._success.connect(self.post_install)
        self.mgt._progress.connect(self.install_progress)
        self.hwinfo._add.connect(lambda create, text: self.hwInfoVBox.addWidget(create(text)))
        self.hwinfo._print.connect(self.stdout)
    
    def stdout(self, text: str): 
        num_nl = 22       
        if len(text) > num_nl and text.find('\n') <= 0:
            for idx in range(num_nl, len(text), num_nl):
                text = text[:idx] + "\n" + text[idx:]
            
        self.stdoutArea.addItem(f">> {text}")
        self.stdoutArea.verticalScrollBar().setValue(self.stdoutArea.verticalScrollBar().maximum())
        
    def install_progress(self, text: str):
        self.stdoutArea.takeItem(self.stdoutArea.count() - 1)
        self.stdoutArea.addItem(f">> {text}")
    
    def post_install(self):
        if self.atShutdownCb.isChecked():
            # t = threading.Timer(5, self.mgt.execute, kwargs={'cmd': ["shutdown", "/s", "/t", "1"]})
            # t.start()
            QMessageBox.information(self, '完成', '安裝成功，即將自動關機')
        else:
            box = QMessageBox()
            box.setIcon(QMessageBox.Information)
            box.setWindowTitle('完成')
            box.setText('搞掂')
            box.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
            btnok = box.button(QMessageBox.Ok)
            btnok.setText('好')
            btnclose = box.button(QMessageBox.Close)
            btnclose.setText('關閉程式')
            box.exec_()
            
            if box.clickedButton() == btnclose:
                exit(0)
    
    def refresh_hwinfo(self):
        for i in reversed(range(self.hwInfoVBox.count())): 
            self.hwInfoVBox.itemAt(i).widget().setParent(None)
        self.hwinfo.start()
    
    def install(self):
        if self.lanDriverDd.currentData() is not None:
            print(self.lanDriverDd.currentData())
            print(self.lanConf.conf[self.lanDriverDd.currentData()])
        if self.displayDriverDd.currentData() is not None:
            print(self.displayDriverDd.currentData())
            print(self.dpConf.conf[self.displayDriverDd.currentData()])
        for id, cb in self.otherCbs.items():
            if cb.isChecked():
                print(id)
                print(self.othConf.conf[id])
                
        # debug
        self.mgt.add_task(['C:\\Users\\user\\Desktop\\OneClick-Drivers-Installer\\src\\print.exe'])
        self.mgt.add_task(['C:\\Users\\user\\Desktop\\OneClick-Drivers-Installer\\src\\print.exe'])
        # start install
        if self.atInstallCb.isChecked():
            self.stdout('在安裝完成前，取消勺擇自動關機將會取消\n自動關機，反之亦然。')
            self.stdout('') # temp print for install_progress takeItem remove last list item
            t = threading.Thread(target=self.mgt.auto_install)
            t.start()
        else:
            self.mgt.manual_install()
    
        

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()