import numpy as np
from .agent import Agent
from .environment import Environment
from .exit import Exit

class Simulation:
    """Runs the evacuation simulation using the social force model.
    
    Advances agents at each timestep, applying the repulsion forces from
    walls, obstacles, and other agents while factoring in the driving force in the
    desired direction, It then applies that force and checks evacuations until all agents have
    evacuated or the max number of steps has been reached. 
    """
    def __init__(self, environment: Environment, dt: float = 0.1, max_steps: int = 2000) -> None:
        self.environment: Environment = environment
        self.dt: float = dt
        self.time: float = 0.0
        self.max_steps: int = max_steps
        self.steps: int = 0

    @property
    def all_evacuated(self) -> bool:
        return all(agent.evacuated for agent in self.environment.agents)
    
    @property
    def finished(self) -> bool:
        return self.all_evacuated or self.steps >= self.max_steps

    def step(self) -> None:
        """Advances the simulation by one timestep using the social force model.
        
        Each agents is subjected to two types of forces:
            1. Attraction to the nearest exit.
            2. Repulsion from other agents, obstacles, and walls.

        The forces are summed and passed to the apply_force method in Agent which
        converts it into a unit vector used to multiply against the agent's individual set speed.
        """

        env: Environment = self.environment
        active: list[Agent] = [agent for agent in env.agents if not agent.evacuated]

        for agent in active:
            # Exit attraction
            exit_obj: Exit = agent.nearest_exit(env.exits)
            force: np.ndarray = agent.direction_to(exit_obj.position)

            # Agent repulsion
            for other in active:
                if other is not agent:
                    force += agent.repulsion_from_agent(other)
            
            # Object repulsion
            for obstacle in env.obstacles:
                force += agent.repulsion_from_obstacle(obstacle)

            # Wall repulsion
            force += agent.repulsion_from_wall(env.width, env.height)

            agent.apply_force(force, self.dt)

            if exit_obj.check_if_at_exit(agent):
                agent.evacuated = True
        
        self.time += self.dt
        self.steps += 1

    def run(self) -> float | None:
        """Runs simulation to completion or until the max number of steps is reached.
        
        Returns:
            float | None: Evacuation time in seconds if all agents evacuated or None if the
                max number of steps was reached before all agents were evacuated.
        """
        while not self.finished:
            self.step()
        return self.time if self.all_evacuated else None
