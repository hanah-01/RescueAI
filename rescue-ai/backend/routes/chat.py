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

    prompt = f"""You are RescueAI, an offline disaster response assistant.      

Rules:
- Give maximum 5 steps
- Be short and practical
- Focus on survival actions
- No long explanations

Context: 
{context_formatted}
Question: {request.message}"""
    
    advice = gemma.generate(prompt)
    return {"reply": advice}
