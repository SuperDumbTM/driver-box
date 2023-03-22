import sys
import os
import threading
from subprocess import Popen

from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from hw_info_worker import HwInfoWorker
from ui.main import Ui_MainWindow
from window_progress import ProgressWindow
from window_driver import DriverConfigViewerWindow
from install.configuration import DriverType, DriverConfig
from install.install_manager import InstallManager
from install.task import Task


class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    
    qsig_msg = QtCore.pyqtSignal(str)
    qsig_hwinfo = QtCore.pyqtSignal(object, str)
    
    def __init__(self, driconfig: DriverConfig):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(os.path.join(definitions.DIR_PIC, "icon.ico")))
        
        self.driconfg = driconfig
        self.progr_window = ProgressWindow()
        self.dri_conf_window = DriverConfigViewerWindow(driconfig)
        self.hwinfo_worker = HwInfoWorker(self.qsig_msg,
                                          self.qsig_hwinfo,
                                          parent=self)
        self.refresh_hwinfo()
        # ----- driver options -----
        for option in self.driconfg.get_type("network"):
            self.lan_driver_dropdown.addItem(option.name, option.id)
        
        for option in self.driconfg.get_type("display"):
            self.display_dri_dropdown.addItem(option.name, option.id)
        
        for option in self.driconfg.get_type("miscellaneous"):
            cb = QtWidgets.QCheckBox(option.name)
            # NOTE: QCheckBox cannot be assigned a value to the UI element like QComboBox 
            setattr(cb, "dri_id", option.id)  # use setattr() to achive the same functionality
            self.misc_dri_vbox.addWidget(cb)
        # ---------- events ----------
        self.hwInfo_refresh_btn.clicked.connect(self.refresh_hwinfo)
        self.disk_mgt_btn.clicked.connect(lambda: Popen(["start", "diskmgmt.msc"], shell=True))
        self.install_btn.clicked.connect(self.install)
        self.edit_driver_action.triggered.connect(self.dri_conf_window.show)
        self.at_install_cb.clicked.connect(lambda val:self._at_install_onclick(val))
        # ---------- signals ----------
        self.qsig_msg.connect(self.send_msg)
        self.qsig_hwinfo.connect(
            lambda create, text: self.hwinfo_vbox.addWidget(create(text)))
    
    def send_msg(self, text: str): 
        self.prog_msg_box.addItem(f"> {text}")
        self.prog_msg_box.verticalScrollBar().setValue(
            self.prog_msg_box.verticalScrollBar().maximum())  # scroll to bottom
    
    def refresh_hwinfo(self):
        for i in reversed(range(self.hwinfo_vbox.count())):
            self.hwinfo_vbox.itemAt(i).widget().setParent(None)
        self.hwinfo_worker.start()
        
    def alert(self, message: str):
        pass
    
    def install(self):
        manager = InstallManager(self.qsig_msg, self.progr_window.qsig_progress)
        manager.qsig_successful.connect(self.post_install)
        
        # terminate the remaining tasks when progress window is closed
        def prog_close():
            nonlocal self, manager
            if not manager.is_finished():
                manager.abort()
                self.send_msg("已終止安裝")
        self.progr_window.qsig_close.connect(prog_close)
        
        self.progr_window.clear_progress()
        # lan driver
        if self.lan_driver_dropdown.currentData() is not None:
            _conf = self.driconfg.get(self.lan_driver_dropdown.currentData())
            
            self.progr_window.append_progress(_conf, "等待安裝中")
            manager.add_task(Task(_conf))
        # display driver
        if self.display_dri_dropdown.currentData() is not None:
            _conf = self.driconfg.get(self.display_dri_dropdown.currentData())
            
            self.progr_window.append_progress(_conf, "等待安裝中")
            manager.add_task(Task(_conf))
        # other driver
        for i in range(self.misc_dri_vbox.count()):
            cb = self.misc_dri_vbox.itemAt(i).widget()
            if not cb.isChecked():
                continue
            _conf = self.driconfg.get(cb.dri_id)
            self.progr_window.append_progress(_conf, "等待安裝中")
            manager.add_task(Task(_conf))
        
        # start install
        if len(manager) == 0:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("失敗")
            box.setWindowIcon(self.windowIcon())
            box.setIcon(QtWidgets.QMessageBox.Warning)
            box.setText("未有選擇任何軀動")
            box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            btnok = box.button(QtWidgets.QMessageBox.Ok)
            btnok.setText("好")
            box.exec_()
        elif self.at_install_cb.isChecked():
            t = threading.Thread(
                target=manager.auto_install,
                args=[(self.at_retry_cb.isCheckable() or self.at_retry_cb.isEnabled())
                      and self.at_retry_cb.isChecked()
                      ,self.async_install_cb.isChecked()],
                daemon=True)
            t.start()
            self.progr_window.exec_()
        else:
            manager.manual_install()
    
    def post_install(self, success: bool):
        if not success:
            pass
        elif ((self.at_halt_rb.isCheckable() or self.at_halt_rb.isEnabled())
              and self.at_halt_rb.isChecked()):
            t = threading.Timer(5, lambda: Popen(["shutdown", "/s", "/t", "1"]))
            t.start()
            QtWidgets.QMessageBox.information(self, "完成", "安裝成功，即將自動關機")
        else:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("完成")
            box.setWindowIcon(self.windowIcon())
            box.setIcon(QtWidgets.QMessageBox.Information)
            box.setText("搞掂")
            box.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Close)
            btnok = box.button(QtWidgets.QMessageBox.Ok)
            btnok.setText("好")
            btnclose = box.button(QtWidgets.QMessageBox.Close)
            btnclose.setText("關閉程式")
            box.exec_()
            
            if box.clickedButton() == btnclose:
                exit(0)

    def closeEvent(self, event):
        # print(QtWidgets.QApplication.topLevelWidgets())
        QtWidgets.QApplication.closeAllWindows()  # force close all windows
        super().closeEvent(event)
    
    def _at_install_onclick(self, is_checked: bool):
        self.at_retry_cb.setEnabled(is_checked)
        self.async_install_cb.setEnabled(is_checked)
        self.at_halt_rb.setEnabled(is_checked)
        self.at_reboot_rb.setEnabled(is_checked)
        self.at_nothing_rb.setEnabled(is_checked)    
    