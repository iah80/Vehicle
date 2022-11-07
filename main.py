from PyQt5 import QtWidgets
from view.main_window import MainWindow
import sys
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    uic = MainWindow()
    sys.exit(app.exec_())