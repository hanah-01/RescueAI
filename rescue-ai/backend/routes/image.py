from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
from services.yolo_service import YOLOService
from services.gemma_service import GemmaService
from services.clip_service import SceneClassifier
from rag import retrieve

router = APIRouter()
yolo = YOLOService()
gemma = GemmaService()
clip_classifier = SceneClassifier()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def build_prompt(objects, scene, rag_context, user_query=None):
    if user_query:
        query_text = f"\nUser Question: {user_query}"
    else:
        query_text = ""
    
    return f"""
You are RescueAI.

Detected objects:
{objects}

Scene classification:
{scene}

Context:
{rag_context}

Tasks:
1. What is happening?
2. What is the disaster?
3. What are the risks?
4. Give 5 clear survival steps

Be specific and practical.
{query_text}
"""

@router.post("/upload")
async def analyze_image(file: UploadFile = File(...), message: str = Form(None)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    objects = yolo.analyze(path)
    
    scene_label, confidence = clip_classifier.classify(path)
    
    disaster_filter = scene_label if scene_label not in ["uncertain", "unknown", "normal"] else None

    rag_query = f"Scene: {scene_label}. Objects detected: {objects}. User question: {message}"
    rag_context_formatted = retrieve(rag_query, disaster_filter=disaster_filter)

    prompt = build_prompt(objects, f"{scene_label} ({confidence:.2f})", rag_context_formatted, message)
    advice = gemma.generate(prompt)

    if os.path.exists(path):
        os.remove(path)

    obj_str = ", ".join(objects) if objects else "none"
    return {
        "reply": f"Detected: {obj_str}\nScene: {scene_label} ({confidence:.2f})\n\nAdvice:\n{advice}"
    }

