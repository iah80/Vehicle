import cv2
from PyQt5 import uic, QtCore, QtWidgets, QtGui


class Violation(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"E:\python\Nhom15\resource\table_violation.ui",self)
