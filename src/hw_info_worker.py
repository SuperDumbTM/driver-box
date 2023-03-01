import pythoncom

from PyQt5 import QtCore, QtWidgets, QtGui

from utils.sysinfo import HwInfo


class HwInfoWorker(QtCore.QThread):
    
    qsig_msg: QtCore.pyqtSignal
    qsig_hwinfo: QtCore.pyqtSignal
    
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
        
        self.qsig_hwinfo.emit(self._createHwInfoTitle, "底版 MOTHERBOARD")
        for item in self.hwi.get_mb_descr():
            self.qsig_hwinfo.emit(self._createHwInfoText, item)

        self.qsig_hwinfo.emit(self._createHwInfoTitle, "中央處理器 CPU")
        for item in self.hwi.get_cpu_descr():
            self.qsig_hwinfo.emit(self._createHwInfoText, item)
        
        self.qsig_hwinfo.emit(self._createHwInfoTitle, "記憶體 RAM")
        for item in self.hwi.get_ram_descr():
            self.qsig_hwinfo.emit(self._createHwInfoText, item)
        
        self.qsig_hwinfo.emit(self._createHwInfoTitle, "顯示卡 GPU")
        for item in self.hwi.get_gpu_descr():
            self.qsig_hwinfo.emit(self._createHwInfoText, item)
        
        self.qsig_hwinfo.emit(self._createHwInfoTitle, "網絡介面卡 NIC")
        for item in self.hwi.get_nic_descr():
            self.qsig_hwinfo.emit(self._createHwInfoText, item)
            
        self.qsig_hwinfo.emit(self._createHwInfoTitle, "儲存裝置 STORAGE")
        for item in self.hwi.get_disk_descr():
            self.qsig_hwinfo.emit(self._createHwInfoText, item)

        self.qsig_msg.emit('完成載入硬件資訊')

    def _createHwInfoTitle(self, text: str):
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(10)
        font.setWeight(font.ExtraBold)
        
        label = QtWidgets.QLabel(text)
        label.setFont(font)
        return label
    
    def _createHwInfoText(self, text: str):
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(10)
        
        label = QtWidgets.QLabel(text)
        label.setFont(font)
        label.setStyleSheet('color: #545454')
        return label        
