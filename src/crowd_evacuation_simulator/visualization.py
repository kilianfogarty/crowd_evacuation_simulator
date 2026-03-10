import matplotlib.pyplot as plt
from environment import Environment

class Visualizer:
    def __init__(self, environment: Environment) -> None:
        self.environment: Environment = environment
    
    def plot(self) -> None:
        plt.clf() #Clears anything already present

        for agent in self.environment.agents:
            if not agent.evacuated:
                plt.scatter(agent.position[0], agent.position[1])
        
        for exit in self.environment.exits:
            plt.scatter(
                exit.position[0],
                exit.position[1],
                marker="s",
                s=100
            )

        plt.xlim(0, self.environment.width)
        plt.xlim(0, self.environment.height)

        plt.pause(0.01)

