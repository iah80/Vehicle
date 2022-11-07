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

    def record(self,metadata):
        for id in metadata.keys():
            h,w,c = metadata[id][0].shape
            name = f"video_record_{id}"
            self.writer = cv2.VideoWriter(f'{self.root_path}/{name}.mp4',self.fourcc,(w,h))
            for frame in metadata[id]:
                self.writer.write(frame)
        self.writer.release()

    def run(self):
        while self._thread_activate:
            if self.queue_frame.qsize() > 0:
                metadata = self.queue_frame.get()
                self.record(metadata)
            QtCore.QThread.msleep(1)