import numpy as np
import matplotlib.pyplot as plt
import random

from .src.crowd_evacuation_simulator.environment import Environment
from .src.crowd_evacuation_simulator.agent import Agent
from .src.crowd_evacuation_simulator.exit import Exit
from .src.crowd_evacuation_simulator.simulation import Simulation
from .visualization import Visualization

environment: Environment = Environment(width=20, height=20)
environment.add_exit(Exit([18,10], radius=1))

for i in range(30):
    position: list[float] = [random.random() * environment.height, random.random() * environment.width]
    environment.add_agent(Agent(position))

simulation: Simulation = Simulation(environment)
visualization: Visualization = Visualization(environment)

plt.ion() #Interactivity

for i in range(400):
    simulation.step()
    visualization.plot()

