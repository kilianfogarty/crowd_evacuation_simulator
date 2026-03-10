from .agent import Agent
from .environment import Environment
from .exit import Exit

class Simulation:
    def __init__(self, environment: Environment, dt: float = 0.1) -> None:
        self.environment: Environment = environment
        self.dt: float = dt
        self.time: float = 0

    def step(self) -> None:
        for agent in self.environment.agents:

            if agent.evacuated:
                continue

            exit: Exit = self.environment.exits[0]

            agent.step_toward(exit.position, self.dt)

            if exit.check_if_at_exit(agent):
                agent.evacuated = True

        self.time += self.dt
        


