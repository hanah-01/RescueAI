class ResponseAgent:
    def format_response(self, raw_advice: str, scene_data: dict, perception_data: dict, risk_data: dict) -> dict:
        clean_advice = raw_advice.replace("**", "").replace("*", "")
        
        return {
            "objects": perception_data.get("raw_output", ""),
            "scene": scene_data.get("scene_description", "unknown"),
            "severity": risk_data.get("severity", "UNKNOWN"),
            "risk_factors": risk_data.get("risk", "none"),
            "advice": clean_advice,
            "reply": clean_advice,
        }
