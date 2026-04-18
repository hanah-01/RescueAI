from rag import retrieve

class KnowledgeAgent:
    def retrieve_context(self, scene_data: dict, perception_data: dict, user_message: str = None) -> str:
        scene_display = scene_data.get("scene_description", "unknown")
        obj_str = perception_data.get("raw_output", "")
        
        disaster_filter = scene_data["scene"] if scene_data.get("is_disaster") else None
        
        query = f"Scene: {scene_display}. Objects: {obj_str}."
        if user_message:
            query += f" User: {user_message}"
            
        context = retrieve(query, disaster_filter=disaster_filter)
        return context
