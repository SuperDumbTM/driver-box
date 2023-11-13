# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'install_progress_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InstallProgressDialog(object):
    def setupUi(self, InstallProgressDialog):
        InstallProgressDialog.setObjectName("InstallProgressDialog")
        InstallProgressDialog.resize(350, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InstallProgressDialog.sizePolicy().hasHeightForWidth())
        InstallProgressDialog.setSizePolicy(sizePolicy)
        InstallProgressDialog.setMinimumSize(QtCore.QSize(350, 250))
        self.gridLayout = QtWidgets.QGridLayout(InstallProgressDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.progr_table = QtWidgets.QTableWidget(InstallProgressDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progr_table.sizePolicy().hasHeightForWidth())
        self.progr_table.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progr_table.setFont(font)
        self.progr_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.progr_table.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.progr_table.setStyleSheet("QHeaderView::section {\n"
"    color: black;\n"
"    background-color:  rgb(255, 255, 255);\n"
"    border-width: 0px 0px 2px 0px;\n"
"    border-style: dotted;\n"
"}")
        self.progr_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.progr_table.setFrameShadow(QtWidgets.QFrame.Plain)
        self.progr_table.setLineWidth(0)
        self.progr_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.progr_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.progr_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.progr_table.setTabKeyNavigation(False)
        self.progr_table.setProperty("showDropIndicator", False)
        self.progr_table.setDragDropOverwriteMode(False)
        self.progr_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.progr_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.progr_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.progr_table.setShowGrid(False)
        self.progr_table.setGridStyle(QtCore.Qt.SolidLine)
        self.progr_table.setWordWrap(True)
        self.progr_table.setCornerButtonEnabled(False)
        self.progr_table.setObjectName("progr_table")
        self.progr_table.setColumnCount(2)
        self.progr_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.progr_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.progr_table.setHorizontalHeaderItem(1, item)
        self.progr_table.horizontalHeader().setVisible(True)
        self.progr_table.horizontalHeader().setCascadingSectionResizes(True)
        self.progr_table.horizontalHeader().setDefaultSectionSize(150)
        self.progr_table.horizontalHeader().setHighlightSections(True)
        self.progr_table.horizontalHeader().setMinimumSectionSize(150)
        self.progr_table.horizontalHeader().setSortIndicatorShown(False)
        self.progr_table.horizontalHeader().setStretchLastSection(False)
        self.progr_table.verticalHeader().setVisible(False)
        self.progr_table.verticalHeader().setCascadingSectionResizes(False)
        self.progr_table.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.progr_table, 0, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(InstallProgressDialog)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Abort)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 1, 0, 1, 1)

        self.retranslateUi(InstallProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(InstallProgressDialog)

    def retranslateUi(self, InstallProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        InstallProgressDialog.setWindowTitle(_translate("InstallProgressDialog", "安裝狀態"))
        item = self.progr_table.horizontalHeaderItem(0)
        item.setText(_translate("InstallProgressDialog", "軀動名稱"))
        item = self.progr_table.horizontalHeaderItem(1)
        item.setText(_translate("InstallProgressDialog", "狀態"))