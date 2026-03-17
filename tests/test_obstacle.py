import numpy as np
from crowd_evacuation_simulator.agent import Agent
from crowd_evacuation_simulator.environment import Environment
from crowd_evacuation_simulator.obstacle import Obstacle

class TestObstacle:

    def test_obstacle_initialization(self) -> None:
        obstacle: Obstacle = Obstacle([5,5], radius=1.0)
        assert np.allclose(obstacle.position, [5.0,5.0])
        assert np.allclose(obstacle.radius, 1.0)
        