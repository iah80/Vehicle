from PyQt5 import QtCore
from thread_process.detect import Detection

class ThreadRecognition(QtCore.QThread):
    def __init__(self):
        super().__init__()
        self.weight = ""