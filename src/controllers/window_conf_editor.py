import os
from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from install.execute_config import ExecuteConfig
from install.driver_option import Driver, DriverType, FLAG_PRESET
from ui.dri_cfg_editor import Ui_DriverConfigEditor


class DriverConfigEditorWindow(Ui_DriverConfigEditor, QtWidgets.QDialog):

    qsig_save = QtCore.pyqtSignal(Driver)
    qsig_del = QtCore.pyqtSignal(Driver)

    def __init__(self, dri_id: str = None, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(
            os.path.join(definitions.DIR_PIC, "setting.ico")))

        self.dri_id = dri_id
        for dri_type in DriverType:
            self.dri_type_dropdown.addItem(dri_type.value, dri_type)

        self.dri_flag_preset_dropdown.setItemData(0, [])
        for name, flags in FLAG_PRESET.items():
            self.dri_flag_preset_dropdown.addItem(name, flags)
        # ---------- events ----------
        # disable close window behavior when action buttons are clicked
        self.action_btns.disconnect()
        self.action_btns.accepted.connect(self.save)
        self.action_btns.rejected.connect(lambda: self.close())

        self.del_dri_btn.clicked.connect(self.delete)
        self.dri_path_btn.clicked.connect(self.select_dri_path)
        self.dri_flag_preset_dropdown.currentIndexChanged.connect(
            lambda idx: self.dri_flag_input.setText(
                ','.join(self.dri_flag_preset_dropdown.itemData(idx))
            ))

    def fill_data(self, config: Driver):
        self.dri_name_input.setText(config.name)

        for idx in range(self.dri_type_dropdown.count()):
            if self.dri_type_dropdown.itemData(idx) is config.type:
                self.dri_type_dropdown.setCurrentIndex(idx)
                break

        self.dri_path_input.setText(config.path)
        self.dri_flag_input.setText(",".join(config.flags))
        self.dri_fail_time_input.setText(str(config.exec_config.fail_time))
        self.dri_autoable_cb.setChecked(config.exec_config.silentable)
        self.dri_retryable_cb.setChecked(config.exec_config.retryable)
        self.dri_okrtcode_input.setText(
            ','.join(map(str, config.exec_config.ok_rtcode)))

    def select_dri_path(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            self,
            directory=definitions.DIR_DRI,
            filter="Executable (*.exe *.msi)")[0]
        if not path == "":
            self.dri_path_input.setText(
                os.path.relpath(path, definitions.DIR_ROOT))

    def open_save_err_msgbox(self) -> None:
        box = QtWidgets.QMessageBox()
        box.setWindowTitle("錯誤")
        box.setWindowIcon(self.windowIcon())
        box.setIcon(QtWidgets.QMessageBox.Critical)
        box.setText("未能儲存，請檢查是否已經填妥所有資料。")
        box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        btnok = box.button(QtWidgets.QMessageBox.Ok)
        btnok.setText("好")
        box.exec_()

    def save(self):
        try:
            dri = self._get_driver()
        except ValueError:
            self.open_save_err_msgbox()
            return

        if dri.is_validate():
            self.qsig_save.emit(dri)
            self.close()
        else:
            self.open_save_err_msgbox()

    def delete(self):
        self.qsig_del.emit(self._get_driver())
        self.close()

    def _get_driver(self) -> Driver:
        return Driver(self.dri_id,
                      DriverType(
                          self.dri_type_dropdown.currentData()),
                      self.dri_name_input.text(),
                      "",
                      self.dri_path_input.text(),
                      self.dri_flag_input.text().split(","),
                      ExecuteConfig(
                          self.dri_autoable_cb.isChecked(),
                          self.dri_retryable_cb.isChecked(),
                          tuple(
                              map(int, self.dri_okrtcode_input.text().split(',')))
                          if self.dri_okrtcode_input.text() != '' else [],
                          float(self.dri_fail_time_input.text()))
                      )
