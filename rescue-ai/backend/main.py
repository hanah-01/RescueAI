from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from agent import process_chat_message

app = FastAPI(title="Rescue AI API")

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    response = process_chat_message(request.message)
    return {"reply": response}

@app.post("/api/upload")
async def upload_endpoint(file: UploadFile = File(...), message: str = Form(None)):
    # Placeholder for image handling logic
    return {"reply": f"Received image {file.filename} and message: {message}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)