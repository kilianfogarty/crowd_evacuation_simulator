import numpy as np

from crowd_evacuation_simulator import Agent, Exit


class TestExit:
    def test_exit_initialization(self) -> None:
        exit: Exit = Exit([1, 1], radius=4)

        assert isinstance(exit.position, np.ndarray)
        assert np.allclose(exit.position, np.array([1.0, 1.0]))
        assert np.allclose(exit.radius, 4.0)

    def test_check_if_at_exit_in_radius(self) -> None:
        exit: Exit = Exit([0, 0], radius=1.5)
        agent: Agent = Agent([1, 1])
        assert exit.check_if_at_exit(agent) is True

    def test_check_if_at_exit_on_edge(self) -> None:
        exit: Exit = Exit([0, 0], radius=1.0)
        agent: Agent = Agent([1, 0])
        assert exit.check_if_at_exit(agent) is True

    def test_check_if_at_exit_outside_radius(self) -> None:
        exit: Exit = Exit([0, 0], radius=1.0)
        agent: Agent = Agent([2, 2])
        assert exit.check_if_at_exit(agent) is False
