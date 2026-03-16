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

    def test_step_moves_agent_toward_exit(self) -> None:
        environment: Environment = Environment(10,10)
        agent: Agent = Agent([3,3], speed=1.0)
        exit: Exit = Exit([0,0], radius=0.5)

        environment.add_agent(agent)
        environment.add_exit(exit)
        simulation: Simulation = Simulation(environment, dt=1.0)

        simulation.step()

        distance_before_step = np.linalg.norm(np.array([3,3]) - exit.position)
        distance_after_step = np.linalg.norm(agent.position - exit.position)

        assert distance_before_step > distance_after_step

    def test_agent_evacuates_upon_reaching_exit(self):
        environment: Environment = Environment(10,10)
        agent: Agent = Agent([0,0], speed=1.0)
        exit: Exit = Exit([0,0], radius=0.5)

        environment.add_agent(agent)
        environment.add_exit(exit)
        simulation: Simulation = Simulation(environment, dt=1.0)

        simulation.step()  

        assert agent.evacuated is True

    def test_multiple_agents_evacuate(self):
        environment: Environment = Environment(10,10)
        exit: Exit = Exit([0,0], radius=0.5)

        agents: list[Agent] = [Agent([3,4]), Agent([3,5]), Agent([2,4]), Agent([4,4]), Agent([3,3])]
        for agent in agents:
            environment.add_agent(agent)
        environment.add_exit(exit)
        
        simulation: Simulation = Simulation(environment, dt=1.0)

        while not all(agent.evacuated for agent in agents):
            simulation.step()

        for agent in agents:
            assert agent.evacuated is True

    def test_time_updates_after_step(self):
        environment: Environment = Environment(10,10)
        agent: Agent = Agent([0,0], speed=1.0)
        exit: Exit = Exit([0,0], radius=0.5)

        environment.add_agent(agent)
        environment.add_exit(exit)
        simulation: Simulation = Simulation(environment, dt=1.0)
        initial_time = simulation.time

        simulation.step()

        assert np.allclose((initial_time + simulation.dt), simulation.time)

