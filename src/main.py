import os
import sys

from PyQt5 import QtWidgets

import definitions
from controllers.window_main import MainWindow
from install.driver_option import DriverOption
from install.intall_option import InstallOption


def main():
    exit_code: int = None
    app = QtWidgets.QApplication(sys.argv)

    if not os.path.exists(definitions.DIR_DRI):
        os.mkdir(definitions.DIR_DRI)
    if not os.path.exists(definitions.DIR_CONF):
        os.mkdir(definitions.DIR_CONF)

    while exit_code is None or exit_code == definitions.UI_RERENDER_CODE:
        main_window = MainWindow(
            DriverOption(
                os.path.join(definitions.DIR_CONF, "driver.json"),
                definitions.DIR_DRI,
                True),
            InstallOption.from_file(
                os.path.join(definitions.DIR_CONF, "install_option.json"),
                True)
        )
        main_window.show()
        exit_code = app.exec_()
        main_window.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
