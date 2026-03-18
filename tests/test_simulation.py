import numpy as np
from crowd_evacuation_simulator import Agent, Environment, Exit, Simulation


class TestSimulation:
    # init
    def test_simulation_default_initialization(self) -> None:
        environment: Environment = Environment(10, 10)
        simulation: Simulation = Simulation(environment)
        assert simulation.environment is environment
        assert np.allclose(simulation.dt, 0.1)
        assert np.allclose(simulation.time, 0.0)
        assert simulation.max_steps == 2000
        assert simulation.steps == 0

    def test_simulation_custom_initialization(self) -> None:
        environment: Environment = Environment(10, 10)
        simulation: Simulation = Simulation(environment, dt=1.0, max_steps=1000)
        assert simulation.environment is environment
        assert np.allclose(simulation.dt, 1.0)
        assert np.allclose(simulation.time, 0.0)
        assert simulation.max_steps == 1000
        assert simulation.steps == 0

    # all_evacuated
    def test_all_evacuated_true_when_all_agents_evacuated(self) -> None:
        env = Environment(10, 10)
        env.add_exit(Exit([0, 0], radius=2.0))
        env.add_agent(Agent([0, 0]))
        env.add_agent(Agent([0, 0]))
        sim = Simulation(env)
        sim.step()
        assert sim.all_evacuated is True

    def test_all_evacuated_false_when_no_agents_evacuated(self) -> None:
        env = Environment(10, 10)
        env.add_exit(Exit([9, 9], radius=0.5))
        env.add_agent(Agent([0, 0]))
        sim = Simulation(env)
        assert sim.all_evacuated is False

    def test_all_evacuated_false_when_some_agents_remaining(self) -> None:
        env = Environment(10, 10)
        env.add_exit(Exit([0, 0], radius=0.5))
        env.add_agent(Agent([0, 0]))  # at exit
        env.add_agent(Agent([9, 9]))  # far from exit
        sim = Simulation(env)
        sim.step()
        assert sim.all_evacuated is False

    # finished
    def test_finished_true_when_all_evacuated(self) -> None:
        env = Environment(10, 10)
        env.add_exit(Exit([0, 0], radius=2.0))
        env.add_agent(Agent([0, 0]))
        sim = Simulation(env)
        sim.step()
        assert sim.finished is True

    def test_finished_true_when_max_steps_reached(self) -> None:
        env = Environment(10, 10)
        env.add_exit(Exit([9, 9], radius=0.5))
        env.add_agent(Agent([0, 0], speed=0.001))
        sim = Simulation(env, max_steps=5)
        for i in range(5):
            sim.step()
        assert sim.finished is True

    def test_finished_false_before_evacuation_or_max_steps(self) -> None:
        env = Environment(10, 10)
        env.add_exit(Exit([9, 9], radius=0.5))
        env.add_agent(Agent([0, 0]))
        sim = Simulation(env, max_steps=1000)
        assert sim.finished is False

    # step
    def test_step_moves_agent_toward_exit(self) -> None:
        env = Environment(20, 20)
        agent = Agent([2, 10], speed=1.0)
        exit = Exit([18, 10], radius=1.0)
        env.add_agent(agent)
        env.add_exit(exit)
        sim = Simulation(env, dt=1.0)

        distance_before = np.linalg.norm(agent.position - exit.position)
        sim.step()
        distance_after = np.linalg.norm(agent.position - exit.position)

        assert distance_before > distance_after

    def test_step_marks_agent_evacuated_at_exit(self) -> None:
        env = Environment(10, 10)
        agent = Agent([0, 0])
        env.add_agent(agent)
        env.add_exit(Exit([0, 0], radius=1.0))
        sim = Simulation(env)
        sim.step()
        assert agent.evacuated is True

    def test_step_skips_evacuated_agents(self) -> None:
        env = Environment(10, 10)
        agent = Agent([0, 0])
        agent.evacuated = True
        env.add_agent(agent)
        env.add_exit(Exit([9, 9], radius=0.5))
        sim = Simulation(env)
        position_before = agent.position.copy()
        sim.step()
        assert np.allclose(agent.position, position_before)

    def test_step_increments_time(self) -> None:
        env = Environment(10, 10)
        env.add_exit(Exit([5, 5], radius=1.0))
        env.add_agent(Agent([0, 0]))
        sim = Simulation(env, dt=0.1)
        sim.step()
        assert np.allclose(sim.time, 0.1)

    def test_step_increments_step_counter(self) -> None:
        env = Environment(10, 10)
        env.add_exit(Exit([5, 5], radius=1.0))
        env.add_agent(Agent([0, 0]))
        sim = Simulation(env)
        sim.step()
        assert sim.steps == 1

    def test_step_with_multiple_agents_all_move(self) -> None:
        env = Environment(20, 20)
        env.add_exit(Exit([18, 18], radius=1.0))
        agents = [Agent([2, i]) for i in range(5)]
        for agent in agents:
            env.add_agent(agent)
        positions_before = [agent.position.copy() for agent in agents]
        sim = Simulation(env, dt=1.0)
        sim.step()
        for agent, before in zip(agents, positions_before):
            assert not np.allclose(agent.position, before)

    # run
    def test_run_returns_evacuation_time_on_success(self) -> None:
        env = Environment(20, 20)
        env.add_exit(Exit([18, 10], radius=1.0))
        env.add_agent(Agent([2, 10], speed=2.0))
        sim = Simulation(env)
        evac_time = sim.run()
        assert evac_time is not None
        assert evac_time > 0

    def test_run_returns_none_when_max_steps_reached(self) -> None:
        env = Environment(20, 20)
        env.add_exit(Exit([18, 10], radius=0.5))
        env.add_agent(Agent([2, 10], speed=0.001))
        sim = Simulation(env, max_steps=5)
        assert sim.run() is None

    def test_run_all_agents_evacuated_on_completion(self) -> None:
        env = Environment(20, 20)
        env.add_exit(Exit([18, 10], radius=1.0))
        for i in range(5):
            env.add_agent(Agent([2, i * 2], speed=2.0))
        sim = Simulation(env)
        sim.run()
        assert sim.all_evacuated is True
