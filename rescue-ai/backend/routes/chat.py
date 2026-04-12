from fastapi import APIRouter
from pydantic import BaseModel
from services.gemma_service import GemmaService
from rag import retrieve

router = APIRouter()
gemma = GemmaService()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    context_formatted = retrieve(request.message)

    prompt = f"""You are a disaster response assistant.

CONTEXT:
{context_formatted}
USER QUESTION: {request.message}

TASK:
1. Identify the disaster
2. Explain the danger
3. Give 3 clear actions

Use ONLY the given context.
If unsure, say "uncertain".

Answer in this format:

Disaster:
Danger:
Actions:
"""
    
    advice = gemma.generate(prompt)
    return {"reply": advice}
