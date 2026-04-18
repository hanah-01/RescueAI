class RiskAgent:
    """
    Risk Assessment Agent:
    Evaluates life-threat logic based strictly on the deterministic outputs of Perception and Scene agents.
    Outputs structured severity levels without relying on hallucination-prone LLM math.
    """
    def assess_risk(self, scene_data: dict, perception_data: dict) -> dict:
        print("[Risk Agent] Assessing overall risk and severity...")
        scene = scene_data.get("scene", "unknown")
        
        if not scene_data.get("requires_action"):
            return {"severity": "LOW", "risk": "none", "score": 1}
            
        score = 3
        if scene in ["fire", "flood", "earthquake", "tornado", "hurricane", "tsunami"]:
            score += 1
            
        if perception_data.get("has_people"):
            score += 1
            
        score = min(score, 5)
        levels = {1: "INFO", 2: "LOW", 3: "MEDIUM", 4: "HIGH", 5: "CRITICAL"}
        
        risks = []
        if scene == "flood" and perception_data.get("has_people"):
            risks.append("drowning")
            risks.append("hypothermia")
        if scene == "fire" and perception_data.get("has_people"):
            risks.append("burns")
            risks.append("smoke inhalation")
        if scene == "earthquake" and perception_data.get("has_people"):
            risks.append("crush injuries")
            risks.append("falling debris")
            
        return {
            "severity": levels[score],
            "score": score,
            "risk": ", ".join(risks) if risks else f"potential {scene} hazards"
        }
