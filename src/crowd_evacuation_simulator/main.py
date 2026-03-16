import numpy as np
import matplotlib.pyplot as plt
import random

from .environment import Environment
from .agent import Agent
from .exit import Exit
from .simulation import Simulation
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

