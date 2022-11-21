from PyQt5 import uic,QtWidgets,QtGui,QtCore
import cv2
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap,QPainter
from UiLabel import UiLabel
import numpy as np
from coordinate import Ui_Form


class Polygon(QtWidgets.QWidget):
    sig_emit_image = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.uic = Ui_Form()
        self.uic.setupUi(self)
        self.coors = []
        self.image = None
        self.connect_signals()

    def connect_signals(self):
        self.uic.btn_save.clicked.connect(self.slot_save)
        self.sig_emit_image.connect(self.uic.current_frame.slot_get_image)

    def origin(self):
        self.uic.current_frame.origin()

    def slot_save(self):
        self.uic.current_frame.save_coors()
        self.hide()

    def emit_image(self,image):
        if image is not None:
            self.sig_emit_image.emit(image)