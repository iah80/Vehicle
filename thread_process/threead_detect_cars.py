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

    def __init__(self, queue_cap, queue_showimg, queue_detect_plate,queue_record,queue_violation):
        super().__init__()
        self.queue = queue_cap
        self.queue_showimg = queue_showimg
        self.queue_detect_plate = queue_detect_plate
        self.queue_record = queue_record
        self.queue_violation = queue_violation
        self.model = "yolov5s.pt"
        self.thread_active = True
        self.tracking = None
        self.dict_id = []
        self.list_point = []
        self.dic_time = {}
        self.dic_speed = {}
        self.dic_frame = {}

    def read_text(self,w,h):
        with open(r"E:\python\Nhom15\resource\polygon.txt","r") as f:
            lines = f.readlines()
            for line in lines:
                coor = list(map(float, line.split(" ")))
                x = int(coor[0] * w)
                y = int(coor[1] * h)
                self.list_point.append([x, y])
    @torch.no_grad()
    def run(self):
        self.tracking = Tracking(self.model)
        self.tracking.set_property(0.7, [2])
        while self.thread_active:
            if self.queue.qsize() >= 1:
                img = self.queue.get()
                image = img.copy()
                h,w,c = img.shape
                if self.list_point is not None:
                    self.read_text(w,h)
                cv2.line(image,(self.list_point[0][0],self.list_point[0][1]),(self.list_point[1][0],
                        self.list_point[1][1]),(0,0,255),2)
                cv2.line(image, (self.list_point[2][0], self.list_point[2][1]),
                         (self.list_point[3][0], self.list_point[3][1]), (0, 0, 255), 2)
                res = self.tracking.track(image)
                for id in res.keys():
                    value = res[id]
                    if id not in self.dic_frame:
                        self.dic_frame[id] = []
                        self.dic_speed[id] = 0.0
                    self.dic_frame[id].append(img)
                    if id not in self.dic_time and value[3] >= self.list_point[0][1]:
                        self.dic_time[id] = time.time()
                    if id in self.dic_time and value[3] >= self.list_point[2][1]:
                        t = time.time() - self.dic_time[id]
                        if self.dic_speed[id] == 0.0 and t != 0:
                            speed = 20 / t
                            self.dic_speed[id] = speed
                            print("speed: ",speed)
                            self.queue_record.put([id,self.dic_frame[id]])
                        # del self.dic_frame[id]
                    cv2.putText(image,str(id),(value[0],value[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    cv2.rectangle(image,(value[0],value[1]),(value[2],value[3]),(0,0,255),2)
                    if value[3] >= self.list_point[2][1]-180:
                        self.dict_id.append(id)
                        crop_car = img[value[1]:value[3],value[0]:value[2]]
                        self.queue_detect_plate.put([id,crop_car,self.dic_speed[id]])
                if self.queue_showimg.qsize() < 1000:
                    self.queue_showimg.put([img,image])
            QtCore.QThread.msleep(1)

    def stop(self):
        self.thread_active = False