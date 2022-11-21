import cv2
import numpy as np
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from queue import Queue
from thread_process.thread_capture import CaptureThread
from thread_process.threead_detect_cars import ThreadProcess
from thread_process.thread_detect_plate import ThreadPlate
from thread_process.thread_recog import ThreadRecognition
from thread_process.thread_record import RecordCar
from PyQt5.QtCore import QObject

from PyQt5.QtGui import QPixmap


class CameraItems(QtWidgets.QWidget):
    sig_emit_image = pyqtSignal(np.ndarray)
    sig_emit_info = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        uic.loadUi(r"E:\python\Nhom15\resource\camera_item.ui",self)
        self.installEventFilter(self)
        self.link_rtsp = None
        self.queue_capture = Queue()
        self.queue_show_image = Queue()
        self.queue_detect_plate = Queue()
        self.queue_recog = Queue()
        self.queue_record = Queue()
        self.queue_violation = Queue()
        self.thread_capture = CaptureThread(self.queue_capture)
        self.thread_process = ThreadProcess(self.queue_capture,self.queue_show_image,self.queue_detect_plate, self.queue_record,self.queue_violation)
        self.thread_plate = ThreadPlate(self.queue_detect_plate,self.queue_recog)
        self.thread_recog_plate = ThreadRecognition(self.queue_recog,self.queue_violation)
        self.thread_record = RecordCar(self.queue_record)
        self.connect_signals()

    def connect_signals(self):
        self.camera_frame.installEventFilter(self)
        self.btn_accept.clicked.connect(self.slot_accept)
        self.thread_recog_plate.sig_emit_info.connect(self.getinfo)

    def getinfo(self,info):
        self.sig_emit_info.emit(info)

    def slot_accept(self):
        self.link_rtsp = self.line_rtsp.text()
        self.group_setup.hide()
        self.show_camera()

    def show_camera(self):
        self.thread_capture.setup(self.link_rtsp)
        self.thread_capture.start()
        self.thread_process.start()
        self.thread_plate.start()
        self.thread_recog_plate.start()
        self.thread_record.start()

    def eventFilter(self, source:QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if self.group_setup.isHidden():
                self.group_setup.show()
            else:
                self.group_setup.hide()
            return True
        else:
            return super().eventFilter(source,event)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self.queue_show_image.qsize() > 0:
            if self.queue_violation.qsize() > 0:
                pass
            image_draw,current_frame = self.queue_show_image.get()
            self.sig_emit_image.emit(image_draw)
            if current_frame is not None:
                rgb_img = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
                qt_img = QPixmap.fromImage(
                    QtGui.QImage(rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QtGui.QImage.Format_RGB888)
                ).scaled(self.camera_frame.width(), self.camera_frame.height())
                self.camera_frame.setPixmap(qt_img)
        self.update()