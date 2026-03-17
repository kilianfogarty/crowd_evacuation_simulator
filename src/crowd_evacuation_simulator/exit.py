import numpy as np
from .agent import Agent

class Exit:
    """A point for agents to exit in the environment."""
    def __init__(self, position: np.ndarray | list[float], radius: float) -> None:
        self.position: np.ndarray = np.array(position, dtype=float)
        self.radius: float = radius

    def check_if_at_exit(self, agent: Agent) -> bool:
        """Return True if agent is within or on the exit radius."""
        distance: float = np.linalg.norm(agent.position - self.position)
        return bool(distance <= self.radius)
