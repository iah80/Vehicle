from PyQt5 import uic, QtCore, QtWidgets, QtGui
from widget_camera_items import CameraItems
from widget_table_violation import Violation
# from widget_setup_camera import WidgetSetupCamera


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'E:\python\Nhom15\resource\main_window.ui',self)
        self.show()
        self.table_vio = Violation()
        self.grid_layout_camera = QtWidgets.QGridLayout()
        self.grid_layout_camera.setContentsMargins(0, 0, 0, 0)
        self.frame_cameras.setLayout(self.grid_layout_camera)
        self.setup_camera()
        self.connect_sinals()
        # self.widget_setup_camera = WidgetSetupCamera()

    def connect_sinals(self):
        # self.btn_setup.clicked.connect(self.setup_camera)
        self.btn_vio.clicked.connect(self.slot_show_violation)

    def setup_camera(self):
        cam = CameraItems()
        self.grid_layout_camera.addWidget(cam,0,0)

    def slot_show_violation(self):
        self.table_vio.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())