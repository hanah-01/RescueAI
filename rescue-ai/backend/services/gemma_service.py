import requests

class GemmaService:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "gemma:2b"

    def generate(self, prompt):
        try:
            res = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120 
            )
            res.raise_for_status()
            return res.json()["response"]
        except requests.exceptions.Timeout:
            return "Explanation: System overload.\nDisaster: Uncertain\nActions:\n1. The system is currently overloaded.\n2. Seek immediate safety based on your surroundings.\n3. Call emergency services."
        except Exception as e:
            return f"Explanation: Connect Failure.\nDisaster: Unknown\nActions:\n1. Model connection failed.\n2. {str(e)}\n3. Await system restart."
