from src.crowd_evacuation_simulator.agent import Agent

class TestAgent:
    @pytest.fixture
    def agent_instance(self) -> Agent:
        return Agent()
    
    def test_create_agent(self):
        agent: Agent = self.agent_instance
        assert agent != None

    
