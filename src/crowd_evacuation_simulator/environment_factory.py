from __future__ import annotations

import numpy as np

from .agent import Agent
from .environment import Environment
from .exit import Exit
from .obstacle import Obstacle

MARGIN = 0.1
MIN_DISTANCE_FROM_ENTITITY: float = 1.0
MAX_PLACEMENT_ATTEMPTS: int = 50
CELL_SIZE: float = 1.0
DEFAULT_OBSTACLE_RADIUS: float = 1.0


class EnvironmentFactory:
    """Constructs populated environments for simulations."""

    @staticmethod
    def build_environment(
        width: float,
        height: float,
        num_agents: int,
        num_obstacles: int,
        seed: int,
    ) -> Environment:
        """Build and populate an environment with provided agents, obstacles, and exits.

        Args:
            width (float): Room width in simulation units.
            height (float): Room height in simulation units.
            num_agents (int): Number of agents to place.
            num_obstacles (int): Number of obstacles to place.
            seed (int): Random seed for reproducible placement

        Returns:
            Environment: A populated environment ready to simulate.
        """
        rng: np.random.Generator = np.random.default_rng(seed)
        env: Environment = Environment(width, height)

        env.add_exit(Exit([width - 2.0, height / 2.0], radius=1.0))

        x_min, y_min = width * MARGIN, height * MARGIN
        x_max, y_max = width * (1 - MARGIN), height * (1 - MARGIN)

        # NOTE: Cannot use sets to check for membership since floats do not match exactly.
        # NOTE: Overlap is handled on the first step of simulation by a randomized escape direction vector.

        for _ in range(num_obstacles):
            position = rng.uniform([x_min, y_min], [x_max, y_max])
            env.add_obstacle(Obstacle(position, DEFAULT_OBSTACLE_RADIUS))

        for _ in range(num_agents):
            position = rng.uniform([x_min, y_min], [x_max, y_max])
            env.add_agent(Agent(position))

        return env
