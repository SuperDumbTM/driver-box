from abc import abstractmethod
from PyQt5 import QtCore, QtGui, QtWidgets
from hw_info import HwInfo
from element_factory import ElementFactory
import pythoncom

class Drawer(QtCore.QThread):
    
    update_signal: QtCore.pyqtSignal
    
    def __init__(self, parent: QtCore.QObject = None) -> None:
        self.el = ElementFactory()
        super().__init__(parent)

class HwInfoDrawer(QtCore.QThread):
    
    el = ElementFactory()
    trigger = QtCore.pyqtSignal(object, str)
    
    def __init__(self, parent: QtCore.QObject = None) -> None:
        super().__init__(parent)
        # self.vbox = QtWidgets.QVBoxLayout()
        # self.vbox.setObjectName("hwInfoVBox")

        
    def run(self):
        pythoncom.CoInitialize()
        self.hwi = HwInfo()
        
        self.trigger.emit(self.el.createHwInfoTitle, "底版 MOTHERBOARD")
        for item in self.hwi.get_mb_descr():
            self.trigger.emit(self.el.createHwInfoText, item)
        self.trigger.emit(self.el.createHwInfoTitle, "中央處理器 CPU")
        for item in self.hwi.get_cpu_descr():
            self.trigger.emit(self.el.createHwInfoText, item)
        self.trigger.emit(self.el.createHwInfoTitle, "記憶體 RAM")
        for item in self.hwi.get_ram_descr():
            self.trigger.emit(self.el.createHwInfoText, item)
        self.trigger.emit(self.el.createHwInfoTitle, "顯示卡 GPU")
        for item in self.hwi.get_gpu_descr():
            self.trigger.emit(self.el.createHwInfoText, item)
        self.trigger.emit(self.el.createHwInfoTitle, "網絡介面卡 NIC")
        for item in self.hwi.get_nic_descr():
            self.trigger.emit(self.el.createHwInfoText, item)
        self.trigger.emit(self.el.createHwInfoTitle, "儲存裝置 STORAGE")
        for item in self.hwi.get_disk_descr():
            self.trigger.emit(self.el.createHwInfoText, item)

        # ret = []
        # ret.append(self.el.createHwInfoTitle("底版 MOTHERBOARD"))
        # for item in self.hwi.get_mb_descr():
        #     ret.append(self.el.createHwInfoText(item))
        # ret.append(self.el.createHwInfoTitle("中央處理器 CPU"))
        # for item in self.hwi.get_cpu_descr():
        #     ret.append(self.el.createHwInfoText(item))
        # ret.append(self.el.createHwInfoTitle("記憶體 RAM"))
        # for item in self.hwi.get_ram_descr():
        #     ret.append(self.el.createHwInfoText(item))
        # ret.append(self.el.createHwInfoTitle("顯示卡 GPU"))
        # for item in self.hwi.get_gpu_descr():
        #     ret.append(self.el.createHwInfoText(item))
        # ret.append(self.el.createHwInfoTitle("網絡介面卡 NIC"))
        # for item in self.hwi.get_nic_descr():
        #     ret.append(self.el.createHwInfoText(item))
        # ret.append(self.el.createHwInfoTitle("儲存裝置 STORAGE"))
        # for item in self.hwi.get_disk_descr():
        #     ret.append(self.el.createHwInfoText(item))
        
        # self.vbox.addWidget(self.el.createHwInfoTitle("底版 MOTHERBOARD"))
        # for item in self.hwi.get_mb_descr():
        #     self.vbox.addWidget(self.el.createHwInfoText(item))
        # self.vbox.addWidget(self.el.createHwInfoTitle("中央處理器 CPU"))
        # for item in self.hwi.get_cpu_descr():
        #     self.vbox.addWidget(self.el.createHwInfoText(item))
        # self.vbox.addWidget(self.el.createHwInfoTitle("記憶體 RAM"))
        # for item in self.hwi.get_ram_descr():
        #     self.vbox.addWidget(self.el.createHwInfoText(item))
        # self.vbox.addWidget(self.el.createHwInfoTitle("顯示卡 GPU"))
        # for item in self.hwi.get_gpu_descr():
        #     self.vbox.addWidget(self.el.createHwInfoText(item))
        # self.vbox.addWidget(self.el.createHwInfoTitle("網絡介面卡 NIC"))
        # for item in self.hwi.get_nic_descr():
        #     self.vbox.addWidget(self.el.createHwInfoText(item))
        # self.vbox.addWidget(self.el.createHwInfoTitle("儲存裝置 STORAGE"))
        # for item in self.hwi.get_disk_descr():
        #     self.vbox.addWidget(self.el.createHwInfoText(item))
        
        # self.trigger.emit(ret)
