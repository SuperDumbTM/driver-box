import os
import sys

from PyQt5 import QtWidgets

import definitions
from install import configuration
from window_main import MainWindow


def main():
    exit_code: int = None
    app = QtWidgets.QApplication(sys.argv)

    if not os.path.exists(definitions.DIR_DRI):
        os.mkdir(definitions.DIR_DRI)
    if not os.path.exists(definitions.DIR_CONF):
        os.mkdir(definitions.DIR_CONF)

    while exit_code is None or exit_code == definitions.UI_RESTART_CODE:
        main_window = MainWindow(
            configuration.DriverConfig(
                os.path.join(definitions.DIR_CONF, "driver.json"),
                definitions.DIR_DRI,
                True
            )
        )
        main_window.show()
        exit_code = app.exec_()
        main_window.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
