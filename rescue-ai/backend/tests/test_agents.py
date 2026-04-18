def test_risk():
    from backend.agents.risk import RiskAgent
    agent = RiskAgent()
    
    scene_data = {"scene": "flood", "requires_action": True}
    perception_data = {"has_people": True}
    
    print("Testing Risk Agent:")
    result = agent.assess_risk(scene_data, perception_data)
    print(result)

if __name__ == "__main__":
    test_risk()