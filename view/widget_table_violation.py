import cv2
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
import os

from PyQt5.QtWidgets import QTableWidgetItem


class Violation(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"E:\python\Nhom15\resource\table_violation.ui",self)
        self.images = None
        self.path = r"E:\python\Nhom15\video_record"
        self.list_file = None
        self.list_video = None
        self.row = None
        self.contents = []
        self.connect_signals()

    def connect_signals(self):
        self.table_violation.selectionModel().selectionChanged.connect(
            self.on_selectionChanged
        )
        self.btn_view.clicked.connect(self.run_video)

    def run_video(self):
        if self.row is not None:
            self.label_plate.setText(self.contents[self.row][4])
            self.label_speed.setText(self.contents[self.row][3])
            link = self.table_violation.item(self.row,1)
            link = str(link.text())
            cap = cv2.VideoCapture(link)
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    self.images = frame
                else:
                    print("break")
                    break


    @QtCore.pyqtSlot(QtCore.QItemSelection, QtCore.QItemSelection)
    def on_selectionChanged(self, selected, deselected):
        for ix in selected.indexes():
            self.row = ix.row()

    def read_text(self,path,count):
        name = os.path.basename(path)
        name = name.split(".")[0] + ".txt"
        speed = ""
        plate = ""
        time_ = ""
        path_text = f'{self.path}/{name}'
        print("path_text: ",path_text)
        if os.path.exists(path_text):
            with open(f'{self.path}/{name}',"r") as f:
                lines = f.readlines()
                speed, plate, time_ = lines[0].split(" ")
                print("speed: ",speed)
                print("plate: ",plate)
                print("time: ",time_)
        return [count,time_,path,speed,plate]

    def update_table(self):
        self.list_file = os.listdir(self.path)
        self.list_video = [os.path.join(self.path,p) for p in self.list_file if p.endswith(".mp4")]
        print(self.list_video)
        count = 1
        for path in self.list_video:
            res = self.read_text(path,count)
            count += 1
            self.contents.append(res)
        number_cols = self.table_violation.columnCount()
        self.table_violation.setRowCount(0)
        row = 0
        for j in range(len(self.list_video)):
            row = row + 1
            for i in range(number_cols):
                self.table_violation.setRowCount(row)
                self.table_violation.setItem(j, i-1, QTableWidgetItem(self.contents[j][i]))

    def paintEvent(self, a0: QtGui.QPaintEvent):
        if self.images is not None:
            images = cv2.resize(self.images, (360, 360))
            # images = self.images
            rgb_img = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
            qt_img = QPixmap.fromImage(
                QtGui.QImage(rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QtGui.QImage.Format_RGB888)
            ).scaled(self.current_frame.width(), self.current_frame.height())
            self.current_frame.setPixmap(qt_img)
            self.update()
