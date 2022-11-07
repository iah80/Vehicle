from sort.sort import Sort
from yolov5.models.experimental import attempt_load
from yolov5.utils.augmentations import letterbox
from yolov5.utils.general import check_img_size, non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device
import numpy as np
import torch


class Detection:
    def __init__(self):
        self.imgsz = 640  # inference size (height, width)
        self.conf_thresh = 0.35  # confidence threshold
        self.iou_thres = 0.35  # NMS IOU threshold
        self.max_det = 20  # maximum detections per image
        self.device = "0"  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        self.classes = [2]  # filter by class: --class 0, or --class 0 2 3
        self.agnostic_nms = False  # class-agnostic NMS
        self.half = False  # use FP16 half-precision inference
        self.dnn = False  # use OpenCV DNN for ONNX inference
        self.model = "yolov5s.pt"

    def set_property(self,conf_thresh,classes):
        self.conf_thresh = conf_thresh
        self.classes = classes

    def setup_model(self, model):
        self.device = select_device(self.device)
        self.model = attempt_load(model, device=self.device)  # load FP32 model
        stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(self.imgsz, s=stride)  # check img_size
        if self.half:
            self.model.half()  # to FP16

    def detect(self, image):
        bboxes = []
        with torch.no_grad():
            img = letterbox(image, new_shape=self.imgsz)[0]
            img = img[:, :, ::-1].transpose(2, 0, 1)
            img = np.ascontiguousarray(img)
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            # Inference
            pred = self.model(img, augment=False)[0]
            # Apply NMS
            pred = non_max_suppression(pred, self.conf_thresh, self.iou_thres, self.classes,
                                       self.agnostic_nms,
                                       max_det=self.max_det)
            for i, det in enumerate(pred):  # detections per image
                if det is not None and len(det):

                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_boxes(
                        img.shape[2:], det[:, :4], image.shape).round()
                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        x1, y1, x2, y2 = list(map(int, xyxy))
                        bboxes.append([x1, y1, x2, y2, int(cls), float(conf)])
        return bboxes


class Tracking(Detection):
    def __init__(self, model):
        super().__init__()
        self._tracker = Sort(max_age=70, min_hits=0, iou_threshold=0.3)
        self.setup_model(model)

    def track(self, image):
        track_dict = {}
        bboxes = self.detect(image)
        dets_to_sort = np.empty((0, 6))
        for x1, y1, x2, y2, cls, conf in bboxes:
            dets_to_sort = np.vstack((dets_to_sort, np.array([x1, y1, x2, y2, conf, cls])))

        tracked_det = self._tracker.update(dets_to_sort)
        if len(tracked_det) > 0:
            bbox_xyxy = tracked_det[:, :4]
            indentities = tracked_det[:, 8]
            categories = tracked_det[:, 4]
            for i in range(len(bbox_xyxy)):
                x1, y1, x2, y2 = list(map(lambda x: max(0, int(x)), bbox_xyxy[i]))
                id = int(indentities[i])
                track_dict[id] = [x1, y1, x2, y2, categories[i]]
        return track_dict