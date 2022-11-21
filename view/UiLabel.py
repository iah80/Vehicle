from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPainter, QPixmap, QPolygon
from PyQt5.QtCore import QPoint, Qt, QRect, QLine
import cv2


class UiLabel(QtWidgets.QLabel):
    def __init__(self,parent):
        super().__init__()
        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1
        self.coors = []
        self.image = None
        self.img = None
        self.points = []
        self.list_point = []

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if len(self.list_point) > 4:
            self.list_point = []
        x = ev.x()
        y = ev.y()
        # self.coors.append((x,y))
        # self.points.append(QPoint(x,y))
        self.list_point.append((x,y))

    # def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
    #     self.x2 = int(ev.pos().x())
    #     self.y2 = int(ev.pos().y())
    #     self.list_point.append((self.x2,self.y2))

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.x2 = int(ev.pos().x())
        self.y2 = int(ev.pos().y())

    def paintEvent(self, event) -> None:

        qt_img = None
        if self.image is not None:

            img = self.image.copy()
            # image = cv2.resize(image, (360, 360))
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qt_img = QPixmap.fromImage(
                QtGui.QImage(rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QtGui.QImage.Format_RGB888)
            ).scaled(
                self.width(), self.height(), Qt.KeepAspectRatioByExpanding
            )
            self.setPixmap(qt_img)

        painter = QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 5))
        rect = QRect(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)
        if qt_img is not None:
            painter.drawPixmap(QRect(0, 0, qt_img.width(), qt_img.height()), qt_img)
        if 2 <= len(self.list_point) < 4:
            painter.drawLine(self.list_point[0][0],self.list_point[0][1] ,self.list_point[1][0],self.list_point[1][1])
        if len(self.list_point) == 4:
            painter.drawLine(self.list_point[0][0],self.list_point[0][1] ,self.list_point[1][0],self.list_point[1][1])
            painter.drawLine(self.list_point[2][0], self.list_point[2][1],self.list_point[3][0],self.list_point[3][1])
        # painter.drawRect(rect)
        self.update()

    def slot_get_image(self,image):
        self.image = image
        self.coors = []
        self.points = []
        print("shape image: ",self.image.shape)

    def origin(self):
        self.coors = []
        self.points = []

    def save_coors(self):
        with open("coors_polygon.txt","w+") as f:
            for coor in self.list_point:
                x,y = coor[0], coor[1]
                x = x / self.width()
                y = y / self.height()
                f.write("{} {}\n".format(x,y))