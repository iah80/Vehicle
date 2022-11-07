from PyQt5 import QtCore
import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sys

sys.path.insert(0, './yolov5')
import os
from pathlib import Path
import cv2
import torch
from yolov5.utils.dataloaders import VID_FORMATS, IMG_FORMATS
from yolov5.utils.general import check_file

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # yolov5 deepsort root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


class CaptureThread(QtCore.QThread):

    def __init__(self, queue):

        super().__init__()
        # id
        self.index = 0
        # VARIABLES
        self.cap = cv2.VideoCapture()
        self.source = 0  # file/dir/URL/glob, 0 for webcam
        self.__thread_active = True
        self.img = None
        self.q = queue

    def setup(self, source):
        self.source = source

    @torch.no_grad()
    def run(self):
        self.__thread_active = True
        print('Starting Capture Thread...')
        self.source = str(self.source)
        is_file = Path(self.source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = self.source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        if is_url and is_file:
            self.source = check_file(self.source)  # download
        # Create as many trackers as there are video sources
        self.cap.open(self.source)
        while self.cap.isOpened():
            if self.__thread_active:
                flag, img = self.cap.read()
                if not flag:
                    break
                if img is not None:
                    showimg = img
                    if self.q.qsize() < 10:
                        self.q.put(showimg)
                QtCore.QThread.msleep(1)
            else:
                self.cap.release()

    def stop(self):
        print('Stopping Capture Thread')
        self.__thread_active = False
        self.cap.release()
