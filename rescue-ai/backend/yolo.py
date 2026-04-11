from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def analyze_image(path):
    results = model(path)
    detected = []
    
    for r in results:
        for c in r.boxes.cls:
            detected.append(model.names[int(c)])
    
    return list(set(detected))
