from PyQt5 import QtCore
import cv2


class RecordCar(QtCore.QThread):
    def __init__(self,queue):
        super().__init__()
        self.queue_frame = queue
        self.writer = cv2.VideoWriter()
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self._thread_activate = True
        self.root_path = r"E:\python\Nhom15\video_record"

    def record(self,metadata,id):
        h,w,c = metadata[0].shape
        name = f"violation_{id}"
        self.writer = cv2.VideoWriter(f'{self.root_path}/{name}.mp4',self.fourcc,30,(w,h))
        for frame in metadata:
            self.writer.write(frame)
        self.writer.release()

    def run(self):
        while self._thread_activate:
            if self.queue_frame.qsize() > 0:
                id,metadata = self.queue_frame.get()
                self.record(metadata,id)
            QtCore.QThread.msleep(1)