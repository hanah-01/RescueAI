from services.yolo_service import YOLOService
from collections import Counter

class PerceptionAgent:
    """
    Perception Agent (The Eyes - Objects):
    Responsible for identifying objects, entities, and people in the field.
    Returns structured data about what exists in the scene.
    """
    def __init__(self):
        self.yolo = YOLOService()

    def analyze(self, image_path: str) -> dict:
        print("[Perception Agent] Analyzing visual entities...")
        # Note: YOLOService currently returns a unique list of detected objects.
        # We standardize this output for the downstream agents.
        unique_objects = self.yolo.analyze(image_path)
        
        return {
            "objects_list": unique_objects,
            "has_people": "person" in unique_objects,
            "has_vehicles": any(v in unique_objects for v in ["car", "truck", "boat", "bus"]),
            "is_empty": len(unique_objects) == 0,
            "raw_output": ", ".join(unique_objects) if unique_objects else "No objects detected"
        }
