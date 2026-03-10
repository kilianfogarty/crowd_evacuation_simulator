import numpy as np

from src.crowd_evacuation_simulator.agent import Agent

class Exit:
    def __init__(self, position: np.ndarray | list[float], radius: float) -> None:
        self.position: np.ndarray = np.array(position, dtype=float)
        self.radius: float = radius

    def check_if_agent_at_exit(self, agent: Agent) -> bool:
        distance: float = np.linalg.norm(agent.position - self.position)
        return distance < self.radius
