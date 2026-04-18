from services.clip_service import SceneClassifier

class SceneAgent:
    def __init__(self):
        self.clip = SceneClassifier()

    def analyze(self, image_path: str) -> dict:
        label, confidence = self.clip.classify(image_path)
        
        is_disaster = label not in ["uncertain", "unknown", "normal"]
        
        return {
            "scene": label,
            "confidence": float(confidence),
            "is_disaster": is_disaster,
            "requires_action": is_disaster and confidence > 0.3,
            "scene_description": f"Possible {label} (Low confidence)" if (is_disaster and confidence < 0.5) else label
        }