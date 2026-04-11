import requests

class GemmaService:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "gemma:2b"

    def generate(self, prompt):
        res = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        return res.json()["response"]
