import os
from typing import Literal

from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from ui.dri_cfg_viewer import Ui_DriverConfigViewer
from install.configuration import Driver, DriverType, DriverConfig
from widget.tablewidget_dragable import TableWidgetDragable
from window_conf_editor import DriverConfigEditorWindow


class DriverConfigViewerWindow(Ui_DriverConfigViewer, QtWidgets.QWidget):

    def __init__(self, dri_conf: DriverConfig, parent: QtWidgets = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self._setup_tableview()
        self.setWindowIcon(QtGui.QIcon(
            os.path.join(definitions.DIR_PIC, "list.ico")))

        # set table auto resize porpotion to window
        self.dri_cfg_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.dri_conf = dri_conf
        self.crrt_type = DriverType.NET
        self.show_drivers(self.crrt_type)

        # ---------- events ----------
        self.lan_dri_btn.clicked.connect(lambda: self.show_drivers(DriverType.NET))
        self.display_dri_btn.clicked.connect(lambda: self.show_drivers(DriverType.DISPLAY))
        self.misc_dri_btn.clicked.connect(lambda: self.show_drivers(DriverType.MISC))
        self.new_dri_btn.clicked.connect(self.create_driver) 
        self.dri_cfg_table.itemDoubleClicked.connect(self.edit_driver)
        # ---------- signals ----------

    def closeEvent(self, event):
        # print(QtWidgets.QApplication.topLevelWidgets())
        QtWidgets.QApplication.closeAllWindows()  # force close all windows
        super().closeEvent(event)

    def show_drivers(self, type: DriverType):
        self.clear_drivers()
        drivers = self.dri_conf.get_type(type)
        for driver in drivers:
            self.append_driver(driver)
        self.crrt_type = type

    def append_driver(self, driver: Driver) -> int:
        row = self.dri_cfg_table.rowCount()
        self.dri_cfg_table.insertRow(row)

        # col 1: driver name
        self.dri_cfg_table.setItem(row , 0, QtWidgets.QTableWidgetItem(driver.name))
        # col 2: executable path
        path_item = QtWidgets.QTableWidgetItem(driver.path)
        path_item.setToolTip(driver.path)
        self.dri_cfg_table.setItem(row , 1, QtWidgets.QTableWidgetItem(path_item))
        # col 3: install options/flags
        self.dri_cfg_table.setItem(row , 2, QtWidgets.QTableWidgetItem(" ".join(driver.flag)))

        for col in range(self.dri_cfg_table.columnCount()):
            _item = self.dri_cfg_table.item(row, col)
            _item.setData(QtCore.Qt.ItemDataRole.UserRole, driver)
            if not driver.autoable:
                # set yellow background if the "row" is not autoable
                _item.setBackground(QtGui.QColor(230, 207, 0, 255))
                # self.dri_cfg_table.item(row, col).setToolTip("沒有設置安裝參數，不能自動安裝")
        self.dri_cfg_table.resizeRowToContents(row)
        return row

    def clear_drivers(self) -> None:
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
        self.show_drivers(self.crrt_type)
    
    def save_new_driver(self, driver: Driver) -> None:
        self.dri_conf.create(driver)
        self.dri_conf.write()
        self.show_drivers(self.crrt_type)

    def delete_driver(self, driver: Driver) -> None:
        if driver.id is None:
            return
        self.dri_conf.delete(driver.id)
        self.dri_conf.write()
        self.show_drivers(self.crrt_type)

    def _setup_tableview(self):
        self.dri_cfg_table = TableWidgetDragable(self.dri_info_sa_contents)
        self.dri_cfg_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dri_cfg_table.setStyleSheet("QHeaderView::section {\n"
            "    color: black;\n"
            "    background-color:  rgb(255, 255, 255);\n"
            "    border-width: 0px 0px 2px 0px;\n"
            "    border-style: dotted;\n"
            "}")
        self.dri_cfg_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.dri_cfg_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.dri_cfg_table.setDragEnabled(False)
        # self.dri_cfg_table.setDragDropOverwriteMode(False)
        # self.dri_cfg_table.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # self.dri_cfg_table.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        # self.dri_cfg_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # self.dri_cfg_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.dri_cfg_table.setShowGrid(True)
        self.dri_cfg_table.setGridStyle(QtCore.Qt.SolidLine)
        self.dri_cfg_table.setCornerButtonEnabled(True)
        self.dri_cfg_table.setObjectName("dri_cfg_table")
        self.dri_cfg_table.setColumnCount(3)
        self.dri_cfg_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.dri_cfg_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.dri_cfg_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.dri_cfg_table.setHorizontalHeaderItem(2, item)
        self.dri_cfg_table.horizontalHeader().setVisible(True)
        self.dri_cfg_table.horizontalHeader().setCascadingSectionResizes(False)
        self.dri_cfg_table.horizontalHeader().setDefaultSectionSize(80)
        self.dri_cfg_table.horizontalHeader().setMinimumSectionSize(60)
        self.dri_cfg_table.horizontalHeader().setStretchLastSection(False)
        self.dri_cfg_table.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.dri_cfg_table)
        self.dri_info_scrollarea.setWidget(self.dri_info_sa_contents)
        self.gridLayout.addWidget(self.dri_info_scrollarea, 0, 1, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        # self.dri_cfg_table.setSortingEnabled(False)
        item = self.dri_cfg_table.horizontalHeaderItem(0)
        item.setText(_translate("DriverConfigViewer", "軀動名稱"))
        item = self.dri_cfg_table.horizontalHeaderItem(1)
        item.setText(_translate("DriverConfigViewer", "路徑"))
        item = self.dri_cfg_table.horizontalHeaderItem(2)
        item.setText(_translate("DriverConfigViewer", "安裝參數"))
