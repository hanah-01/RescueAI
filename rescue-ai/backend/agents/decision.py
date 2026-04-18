from services.gemma_service import GemmaService

class DecisionAgent:
    def __init__(self):
        self.gemma = GemmaService()
        
    def decide_action(self, scene_data: dict, perception_data: dict, risk_data: dict, context: str, user_message: str = None) -> str:
        print("[Decision Agent] Generating actions via Gemma LLM...")
        scene_display = scene_data.get("scene_description", "unknown")
        obj_str = perception_data.get("raw_output", "")
        severity = risk_data.get("severity", "UNKNOWN")
        specific_risk = risk_data.get("risk", "unknown")
        
        query_text = f"\nUSER: {user_message}" if user_message else ""
        
        prompt = f"""You are a disaster triage AI. Be direct and brief on rescue actions, safety.

SCENE: {scene_display}
ENTITIES: {obj_str}
SEVERITY: {severity}
SPECIFIC RISKS: {specific_risk}

CONTEXT:
{context}
{query_text}

OUTPUT FORMAT:
Explanation: [1 brief sentence]
Disaster: [Name]
Actions:
1. [Action 1]
2. [Action 2]
3. [Action 3]"""

        return self.gemma.generate(prompt)
