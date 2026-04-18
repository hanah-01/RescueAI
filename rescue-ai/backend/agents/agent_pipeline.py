from agents.perception import PerceptionAgent
from agents.scene import SceneAgent
from agents.risk import RiskAgent
from agents.knowledge import KnowledgeAgent
from agents.decision import DecisionAgent
from agents.response import ResponseAgent
from agents.speech import SpeechAgent

class AgentOrchestrator:
    def __init__(self):
        self.perception_agent = PerceptionAgent()
        self.scene_agent = SceneAgent()
        self.risk_agent = RiskAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.decision_agent = DecisionAgent()
        self.response_agent = ResponseAgent()
        self.speech_agent = SpeechAgent()

    def run_pipeline(self, image_path: str = None, user_message: str = None, audio_path: str = None):
        # 1. Speech Transcription
        if audio_path:
            transcription = self.speech_agent.transcribe(audio_path)
            user_message = f"{user_message} (Audio: {transcription})" if user_message else transcription
        
        # 2. Visual Inference
        if image_path:
            perception_data = self.perception_agent.analyze(image_path)
            scene_data = self.scene_agent.analyze(image_path)
            risk_data = self.risk_agent.assess_risk(scene_data, perception_data)    
        else:
            perception_data = {}
            scene_data = {}
            risk_data = {"severity": "UNKNOWN", "score": 0, "risk": "none"}
            
        # 3. Knowledge & Decision
        context = self.knowledge_agent.retrieve_context(scene_data, perception_data, user_message)
        raw_advice = self.decision_agent.decide_action(scene_data, perception_data, risk_data, context, user_message)
        final_response = self.response_agent.format_response(raw_advice, scene_data, perception_data, risk_data)

        if audio_path:
            final_response["transcription"] = user_message

        return final_response, scene_data, perception_data, risk_data
