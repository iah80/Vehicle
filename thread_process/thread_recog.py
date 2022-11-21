from PyQt5 import QtCore
from thread_process.detect import Detection
import torch
from PyQt5.QtCore import pyqtSignal
from datetime import datetime


class ThreadRecognition(QtCore.QThread):
    sig_emit_info = pyqtSignal(list)

    def __init__(self,queue_plate,queue_violation):
        super().__init__()
        self.weight = r"E:\python\Nhom15\digit_v5.pt"
        self._thread_activate = True
        self.queue_plate = queue_plate
        self.model = Detection()
        self.queue_violation = queue_violation
        self.dic_character = {}
        self.dic_id = []

    def getTime(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y_%H:%M:%S")
        return dt_string

    def save_text(self,speed,plate,id):
        path = r"E:\python\Nhom15\video_record"
        time_ = self.getTime()
        with open(f"{path}/violation_{id}.txt","w+") as f:
            f.write("{} {} {}".format(speed,plate,time_))

    @torch.no_grad()
    def run(self):
        self.model.setup_model(self.weight)
        self.model.set_property(0.6,None)
        names = self.model.getName()
        # print("names: ",names)
        while self._thread_activate:
            if self.queue_plate.qsize() > 0:
                charList = []
                positions = []
                id,image,speed ,img_car= self.queue_plate.get()
                if id not in self.dic_character:
                    self.dic_character[id] = []
                bbplate = self.model.detect(image)
                for bb in bbplate:
                    x1, y1, x2, y2, cls, conf = bb
                    charList.append(names[cls])
                    positions.append(x1)
                sortedList = [x for _, x in sorted(zip(positions, charList))]
                recog_val = "".join(map(str,sortedList))
                self.dic_character[id].append(recog_val)
                if speed > 0.0:
                    if id not in self.dic_id:
                        self.dic_id.append(id)
                        plate = max(self.dic_character[id])
                        self.sig_emit_info.emit([img_car,speed,plate])
                        self.save_text(speed,plate,id)
                        print("hello")
                print('recog: ',recog_val)
            QtCore.QThread.msleep(1)