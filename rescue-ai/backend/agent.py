import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_gemma(prompt: str) -> str:
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": "gemma:2b",
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]

def process_chat_message(message: str, context: str = "") -> str:
    system_prompt = """You are RescueAI, an offline disaster response assistant.

Rules:
- Give maximum 5 steps
- Be short and practical
- Focus on survival actions
- No long explanations"""
    
    if context:
        full_prompt = f"{system_prompt}\n\nContext: {context}\n\nAnswer using this information.\nQuestion: {message}"
    else:
        full_prompt = f"{system_prompt}\n\nQuestion: {message}"
        
    return ask_gemma(full_prompt)
