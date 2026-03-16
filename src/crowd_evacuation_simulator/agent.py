import numpy as np
from .exit import Exit
from .obstacle import Obstacle

class Agent:
    def __init__(self, position: np.ndarray | list[float], speed: float = 1.5) -> None:
        self.position: np.ndarray = np.array(position, dtype=float)
        self.speed: float = speed
        self.evacuated: bool = False

    # Unit vector towards a target
    def direction_to(self, target: np.ndarray) -> np.ndarray:
        distance: np.ndarray = target - self.position
        norm: float = np.linalg.norm(distance)

        if norm == 0:
            return np.zeros(2)
        
        # Divide by norm for unit vector
        return distance / norm

    # Move toward target, given an amount of time
    def step_toward(self, target: np.ndarray, dt: float) -> None:
        direction: np.ndarray = self.direction_to(target)
        velocity: np.ndarray = self.speed * direction
        self.position += velocity * dt

    def distance_to_obstacle(self, obstacle: Obstacle) -> float:
        return np.linalg.norm(self.position - obstacle.position)
    
    def repulsion_from_agent(self, other: Agent, strength: float =3.0):
        diff = self.position - other.position
        distance = np.linalg.norm(diff)

        if distance == 0:
            return np.zeros(2)
        
        return strength * (-self.direction_to(other.position)) / distance
    
    def repulsion_from_obstacle(self, obstacle: Obstacle, strength: float = 3.0):
        diff = self.position - obstacle.position
        distance = np.linalg.norm(diff)

        if distance == 0 or distance > obstacle.radius + 2.0:
            return np.zeros(2)

        return strength * (-self.direction_to(obstacle.position)) / distance

    def nearest_exit(self, exits: list[Exit]) -> Exit:
        if not exits:
            raise ValueError("No exits in provided list from environment")
        distances = [np.linalg.norm(self.position - e.position) for e in exits]
        return exits[np.argmin(distances)]




