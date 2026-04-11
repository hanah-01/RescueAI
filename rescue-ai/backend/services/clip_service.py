
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

class SceneClassifier:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        self.labels = [
            "a building on fire with flames",
            "thick smoke in the air",
            "a flooded street with water everywhere",
            "collapsed buildings after an earthquake",
            "a normal everyday scene"
        ]
        
        self.mapping = {
            "a building on fire with flames": "fire",
            "thick smoke in the air": "smoke",
            "a flooded street with water everywhere": "flood",
            "collapsed buildings after an earthquake": "earthquake",
            "a normal everyday scene": "normal"
        }

    def classify(self, image_path):
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            return "invalid_image", 0.0

        inputs = self.processor(
            text=self.labels,
            images=image,
            return_tensors="pt",
            padding=True
        )
        
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = outputs.logits_per_image.softmax(dim=1)
        
        idx = probs.argmax().item()
        confidence = probs[0][idx].item()
        
        if confidence < 0.3:
            return "uncertain", confidence
            
        full_phrase = self.labels[idx]
        clean_label = self.mapping.get(full_phrase, "unknown")
        
        return clean_label, confidence

