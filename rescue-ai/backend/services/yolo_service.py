from ultralytics import YOLO

class YOLOService:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def analyze(self, image_path):
        results = self.model(image_path)
        detected = []
        for r in results:
            for cls in r.boxes.cls:
                detected.append(self.model.names[int(cls)])
        return list(set(detected))
