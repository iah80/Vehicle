from detect import Detection
import torch
from PyQt5 import QtCore
import cv2


class ThreadPlate(QtCore.QThread):
    def __init__(self,queue_detect,queue_recog):
        super().__init__()
        self.weight = r"E:\python\Nhom15\plate.pt"
        self.thread_active = True
        self.queue_detect = queue_detect
        self.queue_recog = queue_recog
        self.model = Detection()

    @torch.no_grad()
    def run(self):
        self.model.setup_model(self.weight)
        self.model.set_property(0.7, [0])
        count = 0
        while self.thread_active:
            if self.queue_detect.qsize() >= 1:
                id,img = self.queue_detect.get()
                image = img.copy()
                res = self.model.detect(image)
                if len(res) > 0:
                    crop_plate = img[res[0][1]:res[0][3],res[0][0]:res[0][2]]
                    cv2.imwrite(f"image_crop_{count}.jpg",crop_plate)
                    count += 1
                    if self.queue_recog.qsize() < 2:
                        self.queue_recog.put(crop_plate)
            QtCore.QThread.msleep(1)
