from fastapi import APIRouter, UploadFile, File
import shutil
import os
from agents.agent_pipeline import AgentOrchestrator

router = APIRouter()
orchestrator = AgentOrchestrator()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/audio")
async def upload_audio(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    final_response, _, _, _ = orchestrator.run_pipeline(audio_path=path)

    if os.path.exists(path):
        os.remove(path)

    return final_response
