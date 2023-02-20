import pythoncom

from PyQt5 import QtCore

from utils.sysinfo import HwInfo
from ui.element_factory import ElementFactory


class HwInfoWorker(QtCore.QThread):
    
    qsig_msg: QtCore.pyqtSignal
    qsig_hwinfo: QtCore.pyqtSignal
    
    el = ElementFactory()
    
    def __init__(self,
                 qsig_msg: QtCore.pyqtSignal,
                 qsig_hwinfo: QtCore.pyqtSignal,
                 parent: QtCore.QObject = None) -> None:
        super().__init__(parent)
        self.qsig_msg = qsig_msg
        self.qsig_hwinfo = qsig_hwinfo
    
    @property
    def info_signal(self) -> QtCore.pyqtSignal:
        return self.qsig_hwinfo
    
    def run(self):
        pythoncom.CoInitialize()
        self.hwi = HwInfo()
        self.qsig_msg.emit('載入硬件資訊中..')
        
        self.qsig_hwinfo.emit(self.el.createHwInfoTitle, "底版 MOTHERBOARD")
        for item in self.hwi.get_mb_descr():
            self.qsig_hwinfo.emit(self.el.createHwInfoText, item)

        self.qsig_hwinfo.emit(self.el.createHwInfoTitle, "中央處理器 CPU")
        for item in self.hwi.get_cpu_descr():
            self.qsig_hwinfo.emit(self.el.createHwInfoText, item)
        
        self.qsig_hwinfo.emit(self.el.createHwInfoTitle, "記憶體 RAM")
        for item in self.hwi.get_ram_descr():
            self.qsig_hwinfo.emit(self.el.createHwInfoText, item)
        
        self.qsig_hwinfo.emit(self.el.createHwInfoTitle, "顯示卡 GPU")
        for item in self.hwi.get_gpu_descr():
            self.qsig_hwinfo.emit(self.el.createHwInfoText, item)
        
        self.qsig_hwinfo.emit(self.el.createHwInfoTitle, "網絡介面卡 NIC")
        for item in self.hwi.get_nic_descr():
            self.qsig_hwinfo.emit(self.el.createHwInfoText, item)
            
        self.qsig_hwinfo.emit(self.el.createHwInfoTitle, "儲存裝置 STORAGE")
        for item in self.hwi.get_disk_descr():
            self.qsig_hwinfo.emit(self.el.createHwInfoText, item)

        self.qsig_msg.emit('完成載入硬件資訊')