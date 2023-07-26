import os
import threading
from subprocess import Popen

from PyQt5 import QtCore, QtGui, QtWidgets
from controllers.window_defaults_editor import InstallOptionEditorWindow

import definitions
from enums.halt_option import HaltOption
from install.driver_type import DriverType
from .window_progress import ProgressWindow
from .window_driver import DriverConfigViewerWindow
from ui.main import Ui_MainWindow
from utils import commands
from utils.qwidget import is_widget_enabled
from utils.hw_info_worker import HwInfoWorker
from widgets.driver_checkbox import DriverOptionCheckBox
from install.driver_option import Driver, DriverOption
from install.execute_status import ExecuteStatus
from install.intall_option import InstallOption
from install.task_manager import TaskManager
from install.task import ExecutableTask


class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):

    qsig_msg = QtCore.pyqtSignal(str)
    qsig_hwinfo = QtCore.pyqtSignal(object, str)

    def __init__(self, driconfig: DriverOption, installopt: InstallOption):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(
            os.path.join(definitions.DIR_PIC, "icon.ico")))

        self.driconfg = driconfig
        self.installopt = installopt

        self._hwinfo_worker = HwInfoWorker(self.qsig_msg,
                                           self.qsig_hwinfo,
                                           parent=self)

        # ---------- driver options ----------
        for option in self.driconfg.get_type(DriverType.NET):
            self.lan_driver_dropdown.addItem(option.name, option.id)
        self.lan_driver_dropdown.currentIndexChanged.connect(
            self._dri_on_select)

        for option in self.driconfg.get_type(DriverType.DISPLAY):
            self.display_dri_dropdown.addItem(option.name, option.id)
        self.display_dri_dropdown.currentIndexChanged.connect(
            self._dri_on_select)

        for option in self.driconfg.get_type(DriverType.MISC):
            cb = DriverOptionCheckBox(option.name)
            cb.dri_id = option.id
            self.misc_dri_vbox.addWidget(cb)
            cb.clicked.connect(self._dri_on_select)
        # ---------- halt options ----------
        for option in HaltOption:
            self.halt_option_dropdown.addItem(option.value, option)
        # ---------- events ----------
        self.hwInfo_refresh_btn.clicked.connect(self.refresh_hwinfo)
        self.disk_mgt_btn.clicked.connect(
            lambda: Popen(["start", "diskmgmt.msc"], shell=True))
        self.install_btn.clicked.connect(self._install)
        self.at_install_cb.clicked.connect(self.set_ati_checked)
        self.dri_opt_reset_btn.clicked.connect(self.reset_fields)
        self.set_passwd_cb.clicked.connect(self.set_passwd_checked)

        self.edit_driver_action.triggered.connect(
            lambda: DriverConfigViewerWindow(driconfig).show())
        self.edit_defaults_action.triggered.connect(
            self._show_defaults_edit_window)

        # ---------- signals ----------
        self.qsig_msg.connect(self.send_msg)
        self.qsig_hwinfo.connect(
            lambda create, text: self.hwinfo_vbox.addWidget(create(text)))

        self.refresh_hwinfo()
        self.reset_fields()

    def send_msg(self, text: str):
        """Display a message to the message box

        Args:
            text (str): message to be displayed
        """
        self.prog_msg_box.addItem(f"> {text}")
        self.prog_msg_box.verticalScrollBar().setValue(
            self.prog_msg_box.verticalScrollBar().maximum())  # scroll to bottom

    def refresh_hwinfo(self):
        """Rescan and update the hardware information of the computer
        """
        for i in reversed(range(self.hwinfo_vbox.count())):
            self.hwinfo_vbox.itemAt(i).widget().setParent(None)
        self._hwinfo_worker.start()

    def set_ati_checked(self, checked: bool):
        """Enable/disable the auto-installation option checkboxes
        """
        self.at_install_cb.setChecked(checked)
        for idx in range(self.install_mode_options.count()):
            widget = self.install_mode_options.itemAt(idx).widget()
            if (widget.objectName() != self.at_install_cb.objectName()
                    and isinstance(widget, (QtWidgets.QCheckBox, QtWidgets.QRadioButton))):
                widget.setEnabled(checked)

        if self.is_selected_autoable():
            self.set_halt_options(checked)

    def set_passwd_checked(self, checked: bool):
        self.set_passwd_cb.setChecked(checked)
        self.set_passwd_txt.setEnabled(
            self.set_passwd_cb.isChecked())

    def set_halt_options(self, enable: bool):
        """Enable/disable the halt option checkboxes
        """
        if not self.at_install_cb.isChecked():
            enable = False

        self.halt_option_dropdown.setEnabled(enable)

    def reset_fields(self):
        """Reset all the input fields to default value.
        """
        self.lan_driver_dropdown.setCurrentIndex(0)
        self.display_dri_dropdown.setCurrentIndex(0)
        for widget in self._misc_dri_options():
            widget.setChecked(False)

        self.set_ati_checked(self.installopt.auto_install)
        self.async_install_cb.setChecked(self.installopt.async_install)
        self.at_retry_cb.setChecked(self.installopt.retry_on_fail)
        self.halt_option_dropdown.setCurrentIndex(
            self.halt_option_dropdown.findData(self.installopt.halt_option))
        self.set_passwd_checked(self.installopt.is_set_passwd)
        self.set_passwd_txt.setPlainText(self.installopt.passwd)

    def selected_drivers(self) -> list[Driver]:
        drivers = []
        # network driver
        if self.lan_driver_dropdown.currentData() is not None:
            drivers.append(self.driconfg.get(
                self.lan_driver_dropdown.currentData()))
        # display driver
        if self.display_dri_dropdown.currentData() is not None:
            drivers.append(self.driconfg.get(
                self.display_dri_dropdown.currentData()))
        # miscellaneous driver
        for widget in self._misc_dri_options():
            if not widget.isChecked():
                continue
            elif not isinstance(widget, DriverOptionCheckBox):
                continue
            drivers.append(self.driconfg.get(widget.dri_id))
        return drivers

    def is_selected_autoable(self) -> bool:
        """Returns whether all the selected drivers can be installed with \
            slient /unattend mode.
        """
        return all((dri.exec_config.silentable for dri in self.selected_drivers()))

    def _install(self):
        """Start the install process
        """
        prog_window = ProgressWindow()
        manager = TaskManager(self.qsig_msg, prog_window.qsig_progress)
        manager.qsig_install_result.connect(self._post_install)

        # set password
        if self.set_passwd_cb.isChecked():
            manager.add_task(
                commands.set_password(commands.get_current_usrname(), self.set_passwd_txt.toPlainText()))
            self.send_msg(
                f"{commands.get_current_usrname()} 的密碼將會更改為 \"'{self.set_passwd_txt.toPlainText()}\"")

        def prog_close():
            """Terminate the remaining tasks when progress window is closed
            """
            if not manager.is_finished():
                manager.abort_tasks()
                self.send_msg("已終止安裝")
        prog_window.qsig_window_close.connect(prog_close)

        for dri_conf in self.selected_drivers():
            _task = ExecutableTask(
                dri_conf.name, dri_conf.exec_config, dri_conf.path, dri_conf.flags)
            prog_window.append_progress(_task, "等待安裝中")
            manager.add_task(_task)

        # ---------- start installation ----------
        if len(manager.tasks) == 0:
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
            threading.Thread(
                target=manager.auto_install,
                args=[
                    (is_widget_enabled(self.at_retry_cb)
                     and self.at_retry_cb.isChecked()),
                    self.async_install_cb.isChecked(),
                ],
                daemon=True).start()
            prog_window.exec_()
        else:
            manager.manual_install()

    def _post_install(self, status: ExecuteStatus):
        """Follow-up routine for the installation process

        Args:
            success (ExecuteStatus): Execution status
        """
        if (status != ExecuteStatus.SUCCESS
            and not (status != ExecuteStatus.ABORTED
                     and not self.at_retry_cb.isChecked())):
            pass
        elif (is_widget_enabled(self.halt_option_dropdown)):
            if self.halt_option_dropdown.currentData() == HaltOption.SHUTDOWN:
                commands.shutdown(5).execute()
                QtWidgets.QMessageBox.information(self, "完成", "即將自動關機")
            elif self.halt_option_dropdown.currentData() == HaltOption.REBOOT:
                commands.reboot(5).execute()
                QtWidgets.QMessageBox.information(self, "完成", "即將重新開機")
            elif self.halt_option_dropdown.currentData() == HaltOption.BIOS:
                commands.reboot_uefi(5).execute()
                QtWidgets.QMessageBox.information(
                    self, "完成", "即將自動重啟至 BIOS")
        else:
            box = QtWidgets.QMessageBox()
            box.setWindowIcon(self.windowIcon())
            box.setIcon(QtWidgets.QMessageBox.Information)
            box.setText("完成")
            box.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Close)
            btnok = box.button(QtWidgets.QMessageBox.Ok)
            btnok.setText("好")
            btnclose = box.button(QtWidgets.QMessageBox.Close)
            btnclose.setText("關閉程式")
            box.exec_()

            if box.clickedButton() == btnclose:
                QtWidgets.qApp.exit(0)

    def _dri_on_select(self):
        """Analyse and update execution options for auto installation mode
        based on user selection on to be installed drivers.

        E.g. If selected drivers contains non-autoable drivers,\
            disable execution options for auto installation mode
        """
        self.set_halt_options(self.is_selected_autoable())
        # if not self.is_selected_autoable():
        #     self.at_nothing_rb.setChecked(True)

    def _misc_dri_options(self) -> list[QtWidgets.QCheckBox]:
        """Returns all the "miscellaneous" driver options
        """
        return [self.misc_dri_vbox.itemAt(i).widget()
                for i in range(self.misc_dri_vbox.count())]

    def _show_defaults_edit_window(self):
        window = InstallOptionEditorWindow(self.installopt)

        def set_installopt(new): self.installopt = new
        window.qsig_save.connect(set_installopt)
        window.exec_()

    # override
    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()  # force close all windows
        super().closeEvent(event)
