import asyncio
from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import json
from datetime import datetime
from collections import Counter
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
os.makedirs("data", exist_ok=True)

def determine_severity(scene, person_count, confidence):
    if confidence < 0.3 or scene in ["uncertain", "unknown", "normal"]: 
        return 1, "LOW"
    
    score = 3
    if scene in ["fire", "flood", "earthquake", "tornado", "hurricane", "tsunami"]:
        score += 1
    if person_count > 0:
        score += 1
    if person_count > 2:
        score += 1 
        
    score = min(score, 5)
    levels = {1: "INFO", 2: "LOW", 3: "MEDIUM", 4: "HIGH", 5: "CRITICAL"}
    return score, levels[score]

def build_prompt(obj_str, scene_display, severity, rag_context, user_query=None):
    query_text = f"\nUSER: {user_query}" if user_query else ""
    return f"""You are a disaster triage AI. Be direct and brief on rescue actions, safety.

SCENE: {scene_display}
ENTITIES: {obj_str}
SEVERITY: {severity}

CONTEXT:
{rag_context}
{query_text}

OUTPUT FORMAT:
Explanation: [1 brief sentence]
Disaster: [Name]
Actions:
1. [Action 1]
2. [Action 2]
3. [Action 3]"""

@router.post("/upload")
async def analyze_image(file: UploadFile = File(...), message: str = Form(None)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    loop = asyncio.get_event_loop()
    objects_task = loop.run_in_executor(None, yolo.analyze, path)
    clip_task = loop.run_in_executor(None, clip_classifier.classify, path)
    
    objects, (scene_label, confidence) = await asyncio.gather(objects_task, clip_task)

    obj_counts = Counter(objects)
    person_count = obj_counts.get("person", 0)
    
    if obj_counts:
        obj_str = ", ".join([f"{count} {obj}{'s' if count>1 else ''}" for obj, count in obj_counts.items()])
    else:
        obj_str = "No specific entities detected"
    
    if confidence < 0.5 and scene_label not in ["uncertain", "unknown", "normal"]:
        scene_display = f"Possible {scene_label} (Low certainty)"
    else:
        scene_display = f"{scene_label}"
        
    sev_score, sev_label = determine_severity(scene_label, person_count, confidence)

    disaster_filter = scene_label if scene_label not in ["uncertain", "unknown", "normal"] else None

    rag_query = f"Scene: {scene_display}. Objects: {obj_str}. User: {message}"
    rag_context_formatted = retrieve(rag_query, disaster_filter=disaster_filter)

    prompt = build_prompt(obj_str, scene_display, sev_label, rag_context_formatted, message)
    raw_advice = gemma.generate(prompt)

    clean_advice = raw_advice.replace("**", "").replace("*", "")

    if os.path.exists(path):
        os.remove(path)
        
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "scene": scene_label,
        "confidence": float(confidence),
        "objects": dict(obj_counts),
        "severity_score": sev_score,
        "severity_label": sev_label,
        "response": clean_advice
    }
    with open("data/telemetry_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {
        "objects": obj_str,
        "scene": scene_display,
        "severity": sev_label,
        "advice": clean_advice,
        "reply": clean_advice
    }

