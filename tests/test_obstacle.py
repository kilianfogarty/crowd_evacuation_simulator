import numpy as np
from crowd_evacuation_simulator import Agent
from crowd_evacuation_simulator import Environment
from crowd_evacuation_simulator import Obstacle

class TestObstacle:

    def test_obstacle_initialization(self) -> None:
        obstacle: Obstacle = Obstacle([5,5], radius=1.0)
        assert np.allclose(obstacle.position, [5.0,5.0])
        assert np.allclose(obstacle.radius, 1.0)
        