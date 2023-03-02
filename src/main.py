import os
import sys

from PyQt5 import QtWidgets

import definitions
from install import configuration
from window_main import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)

    main_wd = MainWindow(
        configuration.DriverConfig(
            os.path.join(definitions.DIR_CONF, "driver.json"),
            definitions.DIR_DRI,
            True
        )
    )
    main_wd.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
