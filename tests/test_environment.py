import numpy as np
from crowd_evacuation_simulator.environment import Environment
from crowd_evacuation_simulator.agent import Agent
from crowd_evacuation_simulator.exit import Exit

class TestEnvironment:

    def test_environment_initialization(self):
        environment: Environment = Environment(width=30, height=40)

        assert environment.width == 30
        assert environment.width == 40
        assert environment.agents == []
        assert environment.exits == []

    def test_add_agent(self):
        environment: Environment = Environment(width=30, height=40)
        agent: Agent = Agent([1,2])

        environment.add_agent(agent)

        assert len(environment.agents) == 1
        assert environment.agents[0] is agent

    def test_add_exit(self):
        environment: Environment = Environment(width=30, height=40)
        exit: Exit = Exit([1,2])

        environment.add_exit(exit)

        assert len(environment.exits) == 1
        assert environment.exits[0] is exit


