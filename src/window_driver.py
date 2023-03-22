import os
from typing import Literal

from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from ui.dri_cfg_viewer import Ui_DriverConfigViewer
from install.configuration import Driver, DriverType, DriverConfig
from window_conf_editor import DriverConfigEditorWindow


class DriverConfigViewerWindow(Ui_DriverConfigViewer, QtWidgets.QWidget):
    
    def __init__(self, dri_conf: DriverConfig, parent: QtWidgets = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(
            os.path.join(definitions.DIR_PIC, "list.ico")))
        
        # set table auto resize porpotion to window
        self.dri_cfg_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.dri_conf = dri_conf
        self.crrt_type = DriverType.NET
        self.show_config(self.crrt_type)
        
        # ---------- events ----------
        self.lan_dri_btn.clicked.connect(lambda: self.show_config(DriverType.NET))
        self.display_dri_btn.clicked.connect(lambda: self.show_config(DriverType.DISPLAY))
        self.misc_dri_btn.clicked.connect(lambda: self.show_config(DriverType.MISC))
        self.new_dri_btn.clicked.connect(self.create_driver) 
        self.dri_cfg_table.itemDoubleClicked.connect(self.edit_driver)
        # ---------- signals ----------
        
        
    def show_config(self, type: DriverType):
        self.clear_driver()
        drivers = self.dri_conf.get_type(type)
        for driver in drivers:
            self.append_driver(driver)
        self.crrt_type = type
            
    def append_driver(self, driver: Driver) -> int:
        row = self.dri_cfg_table.rowCount()
        self.dri_cfg_table.insertRow(row)
        
        self.dri_cfg_table.setItem(row , 0, QtWidgets.QTableWidgetItem(driver.name))
        
        path_item = QtWidgets.QTableWidgetItem(driver.path)
        path_item.setToolTip(driver.path)
        self.dri_cfg_table.setItem(row , 1, QtWidgets.QTableWidgetItem(path_item))

        self.dri_cfg_table.setItem(row , 2, QtWidgets.QTableWidgetItem(" ".join(driver.flag)))
        
        for col in range(self.dri_cfg_table.columnCount()):
            _item = self.dri_cfg_table.item(row, col)
            _item.setData(QtCore.Qt.ItemDataRole.UserRole, driver)
            if not driver.autoable:
                _item.setBackground(QtGui.QColor(230, 207, 0, 255))
                # self.dri_cfg_table.item(row, col).setToolTip("沒有設置安裝參數，不能自動安裝")
        self.dri_cfg_table.resizeRowToContents(row)
        return row
    
    def clear_driver(self) -> None:
        for i in range(self.dri_cfg_table.rowCount(), -1, -1):
            self.dri_cfg_table.removeRow(i)
        
    def edit_driver(self, item: QtWidgets.QTableWidgetItem):
        tgt_dri: Driver = item.data(QtCore.Qt.ItemDataRole.UserRole)
        
        self.conf_editor_window = DriverConfigEditorWindow(tgt_dri.id)
        self.conf_editor_window.qsig_save.connect(self.save_edited_driver)
        self.conf_editor_window.qsig_del.connect(self.delete_driver)
        
        self.conf_editor_window.dri_type_dropdown.setEnabled(False)
        self.conf_editor_window.fill_data(tgt_dri)
        self.conf_editor_window.exec_()  # instead of show(), exec_() will prohibit user to jump to other window
    
    def create_driver(self) -> None:
        self.conf_editor_window = DriverConfigEditorWindow()
        self.conf_editor_window.qsig_save.connect(self.save_new_driver)
        self.conf_editor_window.del_dri_btn.setEnabled(False)
        self.conf_editor_window.exec_()
    
    def save_edited_driver(self, driver: Driver) -> None:
        self.dri_conf.update(driver.id, driver)
        self.dri_conf.write()
        self.show_config(self.crrt_type)
        
    def save_new_driver(self, driver: Driver) -> None:
        self.dri_conf.create(driver)
        self.dri_conf.write()
        self.show_config(self.crrt_type)
    
    def delete_driver(self, driver: Driver) -> None:
        if driver.id is None:
            return
        self.dri_conf.delete(driver.id)
        self.dri_conf.write()
        self.show_config(self.crrt_type)

        