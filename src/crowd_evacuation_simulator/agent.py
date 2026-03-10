import numpy as np

class Agent:
    def __init__(self, position: np.ndarray | list[float], speed: float = 1.5):
        self.position: np.ndarray = np.array(position, dtype=float)
        self.speed: float = speed
        self.evacuated: bool = False

    def direction_to(self, target: np.ndarray) -> np.ndarray:
        distance: np.ndarray = target - self.position
        norm: float = np.linalg.norm(distance)

        if norm == 0:
            return np.zeros(2)
        
        return distance / norm

    def step_toward(self, target: np.ndarray, dt: float) -> None:
        direction: np.ndarray = self.direction_to(target)
        velocity: np.ndarray = self.speed * direction
        self.position += velocity * dt


