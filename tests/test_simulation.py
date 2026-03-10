import numpy as np
from crowd_evacuation_simulator.agent import Agent
from crowd_evacuation_simulator.environment import Environment
from crowd_evacuation_simulator.exit import Exit
from crowd_evacuation_simulator.simulation import Simulation

class TestSimulation:

    def test_simulation_initialization(self) -> None:
        environment: Environment = Environment(10,10)
        simulation: Simulation = Simulation(environment, dt=0.5)

        assert simulation.environment is environment
        assert np.allclose(simulation.dt, 0.5)
        assert np.allclose(simulation.time, 0)