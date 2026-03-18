import numpy as np
from crowd_evacuation_simulator.environment_factory import (
    Environment,
    EnvironmentFactory,
)


class TestEnvironmentFactory:
    # init
    def test_environment_factory_initialization(self) -> None:
        env: Environment = EnvironmentFactory.build_environment(
            width=20, height=20, num_agents=10, num_obstacles=3, seed=0
        )
        assert env.width == 20
        assert env.height == 20
        assert len(env.agents) == 10
        assert len(env.obstacles) == 3
        assert len(env.exits) == 1

    def test_environment_factory_agents_placed_within_margins(self) -> None:
        env = EnvironmentFactory.build_environment(
            width=20, height=20, num_agents=30, num_obstacles=0, seed=0
        )
        margin = 0.1
        x_min, y_min = 20 * margin, 20 * margin
        x_max, y_max = 20 * (1 - margin), 20 * (1 - margin)
        for agent in env.agents:
            assert x_min <= agent.position[0] <= x_max
            assert y_min <= agent.position[1] <= y_max

    def test_obstacles_placed_within_margins(self) -> None:
        env = EnvironmentFactory.build_environment(
            width=20, height=20, num_agents=0, num_obstacles=10, seed=0
        )
        margin = 0.1
        x_min, y_min = 20 * margin, 20 * margin
        x_max, y_max = 20 * (1 - margin), 20 * (1 - margin)
        for obstacle in env.obstacles:
            assert x_min <= obstacle.position[0] <= x_max
            assert y_min <= obstacle.position[1] <= y_max

    # determinism
    def test_same_seed_produces_identical_positions(self) -> None:
        env_a = EnvironmentFactory.build_environment(
            width=20, height=20, num_agents=10, num_obstacles=0, seed=42
        )
        env_b = EnvironmentFactory.build_environment(
            width=20, height=20, num_agents=10, num_obstacles=0, seed=42
        )
        for agent_a, agent_b in zip(env_a.agents, env_b.agents):
            assert np.allclose(agent_a.position, agent_b.position)

    def test_different_seeds_produce_different_positions(self) -> None:
        env_a = EnvironmentFactory.build_environment(
            width=20, height=20, num_agents=10, num_obstacles=0, seed=0
        )
        env_b = EnvironmentFactory.build_environment(
            width=20, height=20, num_agents=10, num_obstacles=0, seed=1
        )
        positions_match = all(
            np.allclose(a.position, b.position)
            for a, b in zip(env_a.agents, env_b.agents)
        )
        assert not positions_match
