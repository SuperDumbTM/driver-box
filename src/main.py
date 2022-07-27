import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_main import Ui_mainWindow


class MyMainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self,parent = None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

        self.installBtn.clicked.connect(lambda x:print(213))

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
    pass

if __name__ == "__main__":
    main()