import numpy as np
from src.crowd_evacuation_simulator.agent import Agent

class TestAgent:

    def test_environment_initialization(self):
        agent: Agent = Agent([1,2])
        assert agent.speed == 1.5
        assert agent.evacuated == False
    
    def test_direction_to_new_position(self):
        agent: Agent = Agent([0,0])
        target = np.array([3,4])

        direction: np.ndarray = agent.direction_to(target)
        expected: np.ndarray = np.array([0.6, 0.8])

        # Comparing floats gets weird, cannot use ==
        assert np.allclose(direction, expected)

    def test_direction_to_same_position(self):
        agent: Agent = Agent([1,1])
        target = np.array([1,1])

        direction: np.ndarray = agent.direction_to(target)
        expected: np.ndarray = np.zeros(2)

        # Comparing floats gets weird, cannot use ==
        assert np.allclose(direction, expected)

    def test_step_toward_moves_agent(self):
        agent: Agent = Agent([1,1], 1.0)
        target = np.array([1,0])
        dt = 1.0

        agent.step_toward(target, dt)

        assert np.allclose(agent.position, np.array([1.0, 0.0]))

    
