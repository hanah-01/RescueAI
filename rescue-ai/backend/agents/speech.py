import whisper

class SpeechAgent:
    def __init__(self):
        self.model = whisper.load_model("tiny") 

    def transcribe(self, audio_path: str) -> str:
        try:
            result = self.model.transcribe(audio_path)
            return result["text"].strip()
        except Exception as e:
            return ""
