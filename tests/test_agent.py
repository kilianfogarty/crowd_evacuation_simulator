import numpy as np
import pytest
from crowd_evacuation_simulator import Agent
from crowd_evacuation_simulator import Exit
from crowd_evacuation_simulator import Obstacle

class TestAgent:

    # init
    def test_agent_default_initialization(self) -> None:
        agent: Agent = Agent([1,2])
        assert agent.speed == 1.5
        assert agent.evacuated == False

    def test_agent_custom_speed_initialization(self) -> None:
        agent: Agent = Agent([1,2], speed = 2.0)
        assert agent.speed == 2.0
        assert agent.evacuated == False
    
    # direction_to
    def test_direction_to_new_position(self) -> None:
        agent: Agent = Agent([0,0])
        target = np.array([3,4])
        direction: np.ndarray = agent.direction_to(target)
        expected: np.ndarray = np.array([0.6, 0.8])

        # Comparing floats gets weird, cannot use ==.
        assert np.allclose(direction, expected)

    def test_direction_to_same_position_returns_zero(self) -> None:
        agent: Agent = Agent([1,1])
        target = np.array([1,1])
        direction: np.ndarray = agent.direction_to(target)
        expected: np.ndarray = np.zeros(2)

        # Comparing floats gets weird, cannot use ==
        assert np.allclose(direction, expected)

    # apply_force
    def test_apply_force_moves_agent(self) -> None:
        agent = Agent([0, 0], speed=1.0)
        agent.apply_force(np.array([1.0, 0.0]), dt=1.0)
        assert np.allclose(agent.position, [1.0, 0.0])

    def test_apply_force_zero_no_movement(self) -> None:
        agent = Agent([3, 3], speed=1.0)
        agent.apply_force(np.zeros(2), dt=1.0)
        assert np.allclose(agent.position, [3, 3])

    def test_apply_force_speed_controls_magnitude(self) -> None:
        agent_slow = Agent([0, 0], speed=1.0)
        agent_fast = Agent([0, 0], speed=2.0)
        force = np.array([1.0, 0.0])
        agent_slow.apply_force(force, dt=1.0)
        agent_fast.apply_force(force, dt=1.0)
        assert agent_fast.position[0] > agent_slow.position[0]

    # nearest_exit
    def test_nearest_exit_single_exit(self) -> None:
        agent = Agent([0, 0])
        exits = [Exit([5, 5], radius=1.0)]
        assert agent.nearest_exit(exits) is exits[0]

    def test_nearest_exit_multiple_exit(self) -> None:
        agent = Agent([0, 0])
        exits = [Exit([5, 5], radius=1.0),
                 Exit([2, 2], radius=1.0),
                 Exit([10, 5], radius=1.0),
                 Exit([15, 8], radius=1.0)
                ]
        assert agent.nearest_exit(exits) is exits[1]

    def test_nearest_exit_throws_exception_on_empty_list(self) -> None:
        agent = Agent([0, 0])
        with pytest.raises(ValueError):
            agent.nearest_exit([])

    # repulsion_from_agent
    def test_repulsion_from_agent_points_away(self) -> None:
        agent = Agent([2, 0])
        other = Agent([0, 0])
        force = agent.repulsion_from_agent(other)
        assert force[0] > 0

    def test_repulsion_from_agent_zero_distance_returns_zero(self) -> None:
        agent = Agent([1, 1])
        other = Agent([1, 1])
        assert np.allclose(agent.repulsion_from_agent(other), np.zeros(2))

    def test_repulsion_from_agent_stronger_when_closer(self) -> None:
        agent = Agent([0, 0])
        close = Agent([1, 0])
        far = Agent([3, 0])
        assert np.linalg.norm(agent.repulsion_from_agent(close)) > np.linalg.norm(agent.repulsion_from_agent(far))

    # repulsion_from_obstacle
    def test_repulsion_from_obstacle_points_away(self) -> None:
        agent = Agent([2, 0])
        obstacle = Obstacle([0, 0], radius=1.0)
        force = agent.repulsion_from_obstacle(obstacle)
        assert force[0] > 0

    def test_repulsion_from_obstacle_out_of_range_returns_zero(self) -> None:
        agent = Agent([10, 0])
        obstacle = Obstacle([0, 0], radius=1.0)
        assert np.allclose(agent.repulsion_from_obstacle(obstacle), np.zeros(2))

    def test_repulsion_from_obstacle_stronger_when_closer(self) -> None:
        obstacle = Obstacle([0, 0], radius=1.0)
        close = Agent([1.5, 0])
        far = Agent([2.5, 0])
        assert np.linalg.norm(close.repulsion_from_obstacle(obstacle)) > np.linalg.norm(far.repulsion_from_obstacle(obstacle))

    # repulsion_from_wall
    def test_repulsion_from_left_wall_pushes_right(self) -> None:
        agent = Agent([0.5, 10])
        force = agent.repulsion_from_wall(width=20, height=20)
        assert force[0] > 0

    def test_repulsion_from_right_wall_pushes_left(self) -> None:
        agent = Agent([19.5, 10])
        force = agent.repulsion_from_wall(width=20, height=20)
        assert force[0] < 0

    def test_repulsion_from_bottom_wall_pushes_up(self) -> None:
        agent = Agent([10, 0.5])
        force = agent.repulsion_from_wall(width=20, height=20)
        assert force[1] > 0

    def test_repulsion_from_top_wall_pushes_down(self) -> None:
        agent = Agent([10, 19.5])
        force = agent.repulsion_from_wall(width=20, height=20)
        assert force[1] < 0

    def test_repulsion_from_wall_center_returns_zero(self) -> None:
        agent = Agent([10, 10])
        force = agent.repulsion_from_wall(width=20, height=20)
        assert np.allclose(force, np.zeros(2))

    def test_repulsion_from_wall_corner_pushes_diagonally(self) -> None:
        agent = Agent([0.5, 0.5])
        force = agent.repulsion_from_wall(width=20, height=20)
        assert force[0] > 0
        assert force[1] > 0