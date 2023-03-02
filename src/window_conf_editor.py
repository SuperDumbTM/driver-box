import os

from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from ui.dri_cfg_editor import Ui_DriverConfigEditor
from install.configuration import Driver, DriverType, DriverConfig, FLAG_PRESET


class DriverConfigEditorWindow(Ui_DriverConfigEditor, QtWidgets.QDialog):
    
    qsig_save = QtCore.pyqtSignal(Driver)
    qsig_del = QtCore.pyqtSignal(Driver)
    
    def __init__(self, dri_id: str = None, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)

        self.dri_id = dri_id
        for dri_type in DriverType.members():
            self.dri_type_dropdown.addItem(dri_type.value, dri_type)
        
        for name, flags in FLAG_PRESET.items():
            self.dri_flag_preset_dropdown.addItem(name, flags)
        # ---------- events ----------
        self.action_btns.accepted.connect(self.save)
        self.del_dri_btn.clicked.connect(self.delete)
        self.dri_exe_path_btn.clicked.connect(self.select_dri_path)
        self.dri_flag_preset_dropdown.currentIndexChanged.connect(
            lambda idx: self.dri_flag_input.setText(
                ','.join(self.dri_flag_preset_dropdown.itemData(idx))
            ))
        
    def fill_data(self, driver: Driver):
        self.dri_name_input.setText(driver.name)
        
        for idx in range(self.dri_type_dropdown.count()):
            if self.dri_type_dropdown.itemData(idx) is driver.type:
                self.dri_type_dropdown.setCurrentIndex(idx)
                break
        
        self.dri_exe_input.setText(driver.path)
        self.dri_flag_input.setText(",".join(driver.flag))
        self.dri_autoable_checkbox.setChecked(driver.autoable)
        
    def select_dri_path(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            self,
            directory=definitions.DIR_DRI,
            filter="Executable (*.exe *.msi)")[0]
        if not path == "":
            self.dri_exe_input.setText(os.path.relpath(path, definitions.DIR_ROOT))
        
    def save(self):
        self.qsig_save.emit(self._get_driver())
    
    def delete(self):
        self.qsig_del.emit(self._get_driver())
        self.close()
    
    def _get_driver(self) -> Driver:
        return Driver(self.dri_id,
                      DriverType.from_str(self.dri_type_dropdown.currentData()),
                      self.dri_name_input.text(),
                      "",
                      self.dri_exe_input.text(),
                      self.dri_autoable_checkbox.isChecked(),
                      self.dri_flag_input.text().split(","))