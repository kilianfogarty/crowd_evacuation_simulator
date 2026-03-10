from numpy import np 
from typing import List
from src.crowd_evacuation_simulator.agent import Agent
from src.crowd_evacuation_simulator.agent import Exit

class Environment:
    def __init__(self, width: float, height: float) -> None:
        self.width: float = width
        self.height: float = height
        self.agents: List[Agent] = []
        self.exits: List[Exit] = []

    def add_agents(self, agent: Agent) -> None:
        self.agents.append(agent)

    def add_exit(self, exit_obj: Exit) -> None:
        self.exits.append(exit_obj)
