from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QFont
import cv2


class VehicleViolation(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi(r'E:\python\Nhom15\resource\vehicle_violation.ui', self)
        self.images = None
        self.speed = None
        self.plate = ""

    def setInfo(self, list_info):  # list_info : images ,speed, plate
        self.images = list_info[0]
        self.speed = list_info[1]
        self.plate = list_info[2]

    def paintEvent(self, a0: QtGui.QPaintEvent):
        if self.images is not None:
            images = cv2.resize(self.images, (self.current_frame.width(), self.current_frame.height()))
            # images = self.images
            rgb_img = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
            qt_img = QPixmap.fromImage(
                QtGui.QImage(rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QtGui.QImage.Format_RGB888)
            ).scaled(self.current_frame.width(), self.current_frame.height())
            self.current_frame.setPixmap(qt_img)
            self.update()

            self.label_plate.setText(f'{self.plate}')
            self.label_plate.setStyleSheet("font-weight: bold")
            self.label_plate.setFont(QFont('Arial', 10))
            self.label_speed.setText(str(self.speed))
            self.label_speed.setStyleSheet("font-weight: bold")
            self.label_speed.setFont(QFont('Arial', 10))