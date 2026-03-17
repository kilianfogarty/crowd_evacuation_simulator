import numpy as np
from crowd_evacuation_simulator.environment import Environment
from crowd_evacuation_simulator.agent import Agent
from crowd_evacuation_simulator.exit import Exit
from crowd_evacuation_simulator.obstacle import Obstacle


class TestEnvironment:

    def test_environment_initialization(self) -> None:
        environment: Environment = Environment(width=30, height=40)
        assert environment.width == 30
        assert environment.height == 40
        assert environment.agents == []
        assert environment.exits == []

    def test_add_agent(self) -> None:
        environment: Environment = Environment(width=30, height=40)
        agent: Agent = Agent([1,2])
        environment.add_agent(agent)
        assert len(environment.agents) == 1
        assert environment.agents[0] is agent

    def test_add_exit(self) -> None:
        environment: Environment = Environment(width=30, height=40)
        exit: Exit = Exit([1,2], radius=1)
        environment.add_exit(exit)
        assert len(environment.exits) == 1
        assert environment.exits[0] is exit

    def test_add_obstacle(self) -> None:
        environment: Environment = Environment(width=30, height=40)
        obstacle: Obstacle = Obstacle([5,5], radius=2.0)
        environment.add_obstacle(obstacle)
        assert len(environment.obstacles) == 1
        assert environment.obstacles[0] is obstacle


