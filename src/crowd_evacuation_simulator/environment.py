from .agent import Agent
from .exit import Exit
from .obstacle import Obstacle

class Environment:
    def __init__(self, width: float, height: float) -> None:
        self.width: float = width
        self.height: float = height
        self.agents: list[Agent] = []
        self.exits: list[Exit] = []
        self.obstacles: list[Obstacle] = []

    def add_agent(self, agent: Agent) -> None:
        self.agents.append(agent)

    def add_exit(self, exit: Exit) -> None:
        self.exits.append(exit)

    def add_obstacle(self, obstacle: Obstacle) -> None:
        self.obstacles.append(obstacle)
