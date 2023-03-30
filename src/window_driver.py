import os

from PyQt5 import QtCore, QtGui, QtWidgets

import definitions
from ui.dri_cfg_viewer import Ui_DriverConfigViewer
from install.configuration import Driver, DriverType, DriverConfig
from widgets.tablewidget_dragable import TableWidgetDragable
from window_conf_editor import DriverConfigEditorWindow


class DriverConfigViewerWindow(Ui_DriverConfigViewer, QtWidgets.QWidget):
    
    _modified = False

    def __init__(self, dri_conf: DriverConfig, parent: QtWidgets = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self._setup_tableview()
        self.setWindowIcon(QtGui.QIcon(
            os.path.join(definitions.DIR_PIC, "list.ico")))

        # set table auto resize porpotion to window
        self.dri_opt_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.dri_conf = dri_conf
        self.crrt_type = DriverType.NET
        self.refresh_table(self.crrt_type)

        # ---------- events ----------
        self.lan_dri_btn.clicked.connect(lambda: self.refresh_table(DriverType.NET))
        self.display_dri_btn.clicked.connect(lambda: self.refresh_table(DriverType.DISPLAY))
        self.misc_dri_btn.clicked.connect(lambda: self.refresh_table(DriverType.MISC))
        self.new_dri_btn.clicked.connect(self.open_create_dialog) 
        self.dri_opt_table.itemDoubleClicked.connect(self.open_edit_dialog)
        # ---------- signals ----------

    # override
    def closeEvent(self, event):
        if (self._modified):
            QtWidgets.qApp.exit(-11354)
        super().closeEvent(event)

    def refresh_table(self, type: DriverType):
        """Refresh the driver table widget to show the latest driver options

        Args:
            type (DriverType): target driver type to display
        """
        self.clear_table()
        drivers = self.dri_conf.get_type(type)
        for driver in drivers:
            self.append_driver(driver)
        self.crrt_type = type

    def clear_table(self) -> None:
        """Clear the driver option table"""
        for i in range(self.dri_opt_table.rowCount(), -1, -1):
            self.dri_opt_table.removeRow(i)

    def append_driver(self, driver: Driver) -> int:
        """Append a new driver option to the driver option table

        Args:
            driver (Driver): driver to be added

        Returns:
            int: row index of the appended option
        """
        row = self.dri_opt_table.rowCount()
        self.dri_opt_table.insertRow(row)

        # col 1: driver name
        self.dri_opt_table.setItem(row , 0, QtWidgets.QTableWidgetItem(driver.name))
        # col 2: executable path
        path_item = QtWidgets.QTableWidgetItem(driver.path)
        path_item.setToolTip(driver.path)
        self.dri_opt_table.setItem(row , 1, QtWidgets.QTableWidgetItem(path_item))
        # col 3: install options/flags
        self.dri_opt_table.setItem(row , 2, QtWidgets.QTableWidgetItem(" ".join(driver.flag)))

        for col in range(self.dri_opt_table.columnCount()):
            _item = self.dri_opt_table.item(row, col)
            _item.setData(QtCore.Qt.ItemDataRole.UserRole, driver)
            if not driver.autoable:
                # set yellow background if the "row" is not autoable
                _item.setBackground(QtGui.QColor(230, 207, 0, 255))
                # self.dri_cfg_table.item(row, col).setToolTip("沒有設置安裝參數，不能自動安裝")
        self.dri_opt_table.resizeRowToContents(row)
        return row

    def open_edit_dialog(self, item: QtWidgets.QTableWidgetItem):
        tgt_dri: Driver = item.data(QtCore.Qt.ItemDataRole.UserRole)
        
        self.conf_editor_window = DriverConfigEditorWindow(tgt_dri.id)
        self.conf_editor_window.qsig_save.connect(self.save_edited_driver)
        self.conf_editor_window.qsig_del.connect(self.delete_driver)
        
        self.conf_editor_window.dri_type_dropdown.setEnabled(False)
        self.conf_editor_window.fill_data(tgt_dri)
        self.conf_editor_window.exec_()  # instead of show(), exec_() will prohibit user to jump to other window

    def open_create_dialog(self) -> None:
        self.conf_editor_window = DriverConfigEditorWindow()
        self.conf_editor_window.qsig_save.connect(self.save_new_driver)
        self.conf_editor_window.del_dri_btn.setEnabled(False)
        self.conf_editor_window.exec_()

    def save_edited_driver(self, driver: Driver) -> None:
        self.dri_conf.update(driver.id, driver)
        self.dri_conf.write()
        self.refresh_table(self.crrt_type)
        
        self._modified = True
    
    def save_new_driver(self, driver: Driver) -> None:
        self.dri_conf.create(driver)
        self.dri_conf.write()
        self.refresh_table(self.crrt_type)
        
        self._modified = True

    def delete_driver(self, driver: Driver) -> None:
        if driver.id is None:
            return
        self.dri_conf.delete(driver.id)
        self.dri_conf.write()
        self.refresh_table(self.crrt_type)
        
        self._modified = True

    def _setup_tableview(self):
        self.dri_opt_table = TableWidgetDragable(self.dri_info_sa_contents)
        self.dri_opt_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dri_opt_table.setStyleSheet("QHeaderView::section {\n"
            "    color: black;\n"
            "    background-color:  rgb(255, 255, 255);\n"
            "    border-width: 0px 0px 2px 0px;\n"
            "    border-style: dotted;\n"
            "}")
        self.dri_opt_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.dri_opt_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.dri_cfg_table.setDragEnabled(False)
        # self.dri_cfg_table.setDragDropOverwriteMode(False)
        # self.dri_cfg_table.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # self.dri_cfg_table.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        # self.dri_cfg_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # self.dri_cfg_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.dri_opt_table.setShowGrid(True)
        self.dri_opt_table.setGridStyle(QtCore.Qt.SolidLine)
        self.dri_opt_table.setCornerButtonEnabled(True)
        self.dri_opt_table.setObjectName("dri_cfg_table")
        self.dri_opt_table.setColumnCount(3)
        self.dri_opt_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.dri_opt_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.dri_opt_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.dri_opt_table.setHorizontalHeaderItem(2, item)
        self.dri_opt_table.horizontalHeader().setVisible(True)
        self.dri_opt_table.horizontalHeader().setCascadingSectionResizes(False)
        self.dri_opt_table.horizontalHeader().setDefaultSectionSize(80)
        self.dri_opt_table.horizontalHeader().setMinimumSectionSize(60)
        self.dri_opt_table.horizontalHeader().setStretchLastSection(False)
        self.dri_opt_table.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.dri_opt_table)
        self.dri_info_scrollarea.setWidget(self.dri_info_sa_contents)
        self.gridLayout.addWidget(self.dri_info_scrollarea, 0, 1, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        # self.dri_cfg_table.setSortingEnabled(False)
        item = self.dri_opt_table.horizontalHeaderItem(0)
        item.setText(_translate("DriverConfigViewer", "軀動名稱"))
        item = self.dri_opt_table.horizontalHeaderItem(1)
        item.setText(_translate("DriverConfigViewer", "路徑"))
        item = self.dri_opt_table.horizontalHeaderItem(2)
        item.setText(_translate("DriverConfigViewer", "安裝參數"))
