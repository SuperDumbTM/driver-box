import sys
import os
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

if getattr(sys, 'frozen', False):
    ROOTDIR = os.path.dirname(sys.executable)
elif __file__:
    ROOTDIR = os.path.dirname(os.path.dirname(__file__))

class MyMainWindow(Ui_mainWindow, QMainWindow):
    
    progs_ui: Progress
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.lan_conf = Config(Config.lan)
        self.dp_conf = Config(Config.display)
        self.oth_conf = Config(Config.other)
        self.el = ElementFactory()
        self.mgt = InstallManager()
        self.hwinfo = HwInfoWorker(parent=self)
        
        self.otherCbs = {}
        
        # ----- hardware info -----
        self.refresh_hwinfo()  
        # ----- driver options -----
        self.__setup_driver_option()
        # ----- event listener -----
        self.hwInfoRefreshBtn.clicked.connect(self.refresh_hwinfo)
        self.diskMgtBtn.clicked.connect(lambda x: self.mgt.execute(["start", "diskmgmt.msc"], shell=True))
        self.installBtn.clicked.connect(self.install)
        # ----- signal handler -----
        self.mgt._print.connect(self.stdout)
        self.mgt._success.connect(self.post_install)
        self.mgt._progress.connect(lambda iden, txt, lv: self.progs_ui.update_progress(iden, txt, lv))
        self.hwinfo._add.connect(lambda create, text: self.hwInfoVBox.addWidget(create(text)))
        self.hwinfo._print.connect(self.stdout)
    
    def stdout(self, text: str): 
        num_nl = 22
        if len(text) > num_nl and text.find('\n') <= 0:
            for idx in range(num_nl, len(text), num_nl):
                text = text[:idx] + "\n" + text[idx:]
        self.stdoutArea.addItem(f">> {text}")
        self.stdoutArea.verticalScrollBar().setValue(self.stdoutArea.verticalScrollBar().maximum()) 
    
    def refresh_hwinfo(self):
        for i in reversed(range(self.hwInfoVBox.count())): 
            self.hwInfoVBox.itemAt(i).widget().setParent(None)
        self.hwinfo.start()
    
    def install(self):
        self.progs_ui = Progress()
        # lan driver
        if self.lanDriverDd.currentData() is not None:
            key = self.lanDriverDd.currentData()
            conf = self.lan_conf.conf[key]
            self.progs_ui.add_progress(conf['title'], "等待安裝中")
            self.mgt.add_task(key, [os.path.join(ROOTDIR, conf['path']), *(conf['flag'].split(','))])
        # display driver
        if self.displayDriverDd.currentData() is not None:
            key = self.lanDriverDd.currentData()
            conf = self.dp_conf.conf[key]
            self.progs_ui.add_progress(conf['title'], "等待安裝中")
            self.mgt.add_task(key, [os.path.join(ROOTDIR, conf['path']), *(conf['flag'].split(','))])
        # other driver
        for id, cb in self.otherCbs.items():
            if cb.isChecked():
                conf = self.oth_conf.conf[id]
                self.progs_ui.add_progress(id, conf['title'], "等待安裝中")
                self.mgt.add_task(id, [os.path.join(ROOTDIR, conf['path']), *(conf['flag'].split(','))])
        
        # debug
        # self.mgt.add_task('test', ['C:\\Users\\user\\Desktop\\OneClick-Drivers-Installer\\src\\print.exe'])
        # self.progs_ui.add_progress('test', 'test', "等待安裝中")
        # start install
        if self.atInstallCb.isChecked():
            self.stdout('在安裝完成前，取消勺擇自動關機將會取消\n自動關機，反之亦然。')
            t = threading.Thread(target=self.mgt.auto_install)
            t.start()
            self.progs_ui.show()
        else:
            self.mgt.manual_install()
    
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
    
    def __setup_driver_option(self):
        for id, vals in self.lan_conf.get_conf().items():
            self.lanDriverDd.addItem(vals['title'], id)
        
        for id, vals in self.dp_conf.get_conf().items():
            self.displayDriverDd.addItem(vals['title'], id)
            
        for id, vals in self.oth_conf.get_conf().items():
            self.otherCbs.update({id: self.el.createCheckBox(id, vals['title'])})
            self.otherDriVBox.addWidget(self.otherCbs[id])
        
        
def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()