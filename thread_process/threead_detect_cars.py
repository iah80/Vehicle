import time

import numpy as np
import torch
from PyQt5 import QtCore
from sort.sort import Sort
from yolov5.models.experimental import attempt_load
from yolov5.utils.augmentations import letterbox
from yolov5.utils.general import check_img_size, non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device
import cv2
from detect import Tracking


class ThreadProcess(QtCore.QThread):

    def __init__(self, queue_cap, queue_showimg,queue_detect_plate):
        super().__init__()
        self.queue = queue_cap
        self.queue_showimg = queue_showimg
        self.queue_detect_plate = queue_detect_plate
        self.model = "yolov5s.pt"
        self.thread_active = True
        self.tracking = None
        self.dict_id = []

    @torch.no_grad()
    def run(self):
        self.tracking = Tracking(self.model)
        self.tracking.set_property(0.7, [2])
        while self.thread_active:
            if self.queue.qsize() >= 1:
                img = self.queue.get()
                image = img.copy()
                res = self.tracking.track(image)
                for id in res.keys():
                    value = res[id]
                    cv2.putText(image,str(id),(value[0],value[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    cv2.rectangle(image,(value[0],value[1]),(value[2],value[3]),(0,0,255),2)
                    if id not in self.dict_id:
                        self.dict_id.append(id)
                        crop_car = img[value[1]:value[3],value[0]:value[2]]
                        cv2.imwrite(f'{id}.jpg',crop_car)
                        self.queue_detect_plate.put([id, crop_car])
                if self.queue_showimg.qsize() < 5:
                    self.queue_showimg.put(image)
            QtCore.QThread.msleep(1)

    def stop(self):
        self.thread_active = False