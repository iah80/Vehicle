from PyQt5 import uic, QtCore, QtWidgets, QtGui
from widget_camera_items import CameraItems
from widget_table_violation import Violation
from draw_polygon import Polygon
from thread_process.vehicle_violation import VehicleViolation
# from widget_setup_camera import WidgetSetupCamera


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'E:\python\Nhom15\resource\main_window.ui',self)
        self.show()
        self.poly = Polygon()
        self.table_vio = Violation()
        self.grid_layout_camera = QtWidgets.QGridLayout()
        self.grid_layout_camera.setContentsMargins(0, 0, 0, 0)
        self.frame_cameras.setLayout(self.grid_layout_camera)
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.setup_camera()
        self.connect_sinals()
        self.image = None
        # self.widget_setup_camera = WidgetSetupCamera()

    def connect_sinals(self):
        # self.btn_setup.clicked.connect(self.setup_camera)
        self.btn_vio.clicked.connect(self.slot_show_violation)
        self.btn_draw.clicked.connect(self.slot_draw_polygon)

    def slot_get_image(self,image):
        self.image = image

    def slot_draw_polygon(self):
        self.poly.show()
        self.poly.emit_image(self.image)

    def setup_camera(self):
        cam = CameraItems()
        cam.sig_emit_image.connect(self.slot_get_image)
        cam.sig_emit_info.connect(self.slot_notice)
        self.grid_layout_camera.addWidget(cam,0,0)

    def slot_show_violation(self):
        self.table_vio.show()
        self.table_vio.update_table()

    def slot_notice(self,info):
        vv = VehicleViolation()
        vv.setInfo(info)
        self.scrollAreaWidgetContents.layout().addWidget(vv)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())