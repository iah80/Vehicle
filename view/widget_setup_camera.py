from PyQt5 import uic, QtCore, QtWidgets, QtGui
import math


class WidgetSetupCamera(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'E:\python\Nhom15\resource\camera_setup.ui', self)
        self.connect_signals()
        self.rows = 0
        self.cols = 0

    def connect_signals(self):
        self.number_camera.textChanged.connect(self.select_row_column)

    def select_row_column(self, num_text):
        if num_text.isdigit():
            nums = int(num_text)
            self.rows = int(math.sqrt(nums))
            if self.rows ** 2 == nums:
                self.cols = self.rows
            else:
                for col in range(self.rows, nums + 1):
                    if col * self.rows >= nums:
                        self.cols = col
                        break
            self.line_row.setText(str(self.rows))
            self.line_column.setText(str(self.cols))
