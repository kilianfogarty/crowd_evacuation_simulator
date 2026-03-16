import numpy as np
from .agent import Agent 

class Obstacle:

    def __init__(self, position: np.ndarray | list[float], radius: float) -> None:
        self.position: np.ndarray = np.array(position, dtype=float)
        self.radius: float = radius

    def distance_to_agent(self, agent: Agent) -> float:
        return np.linalg.norm(self.position - agent.position)

    def collides_with_agent(self, agent: Agent) -> bool:
        return agent.distance_to_obstacle(self) <= self.radius