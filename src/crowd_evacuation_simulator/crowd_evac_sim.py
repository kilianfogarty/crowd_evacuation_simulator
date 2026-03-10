import numpy as np
import matplotlib.pyplot as plt


class Agent:

    def __init__(self, position):
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(2)
        self.evacuated = False


class Room:

    def __init__(self, width, height, exit_center, exit_width):
        self.width = width
        self.height = height
        self.exit_center = exit_center
        self.exit_width = exit_width


class Simulation:

    def __init__(self, n_agents=100):

        self.dt = 0.05
        self.desired_speed = 2.0
        self.relaxation_time = 0.5

        self.agent_radius = 0.3
        self.repulsion_strength = 10.0
        self.wall_strength = 20.0
        self.noise_strength = 0.1

        self.room = Room(20, 20, 10, 3)

        self.agents = []
        for _ in range(n_agents):
            x = np.random.uniform(0, self.room.width)
            y = np.random.uniform(5, self.room.height)
            self.agents.append(Agent([x, y]))

    # --------------------------

    def driving_force(self, agent):

        exit_pos = np.array([self.room.exit_center, 0])
        direction = exit_pos - agent.position

        dist = np.linalg.norm(direction)

        if dist > 0:
            direction /= dist

        desired_velocity = self.desired_speed * direction

        return (desired_velocity - agent.velocity) / self.relaxation_time

    # --------------------------

    def agent_repulsion(self, agent):

        force = np.zeros(2)

        for other in self.agents:

            if other is agent or other.evacuated:
                continue

            diff = agent.position - other.position
            dist = np.linalg.norm(diff)

            if dist == 0:
                continue

            overlap = 2 * self.agent_radius - dist

            if overlap > 0:
                force += self.repulsion_strength * overlap * diff / dist

        return force

    # --------------------------

    def wall_repulsion(self, agent):

        x, y = agent.position
        force = np.zeros(2)

        r = self.agent_radius

        if x < r:
            force[0] += self.wall_strength * (r - x)

        if x > self.room.width - r:
            force[0] -= self.wall_strength * (x - (self.room.width - r))

        if y > self.room.height - r:
            force[1] -= self.wall_strength * (y - (self.room.height - r))

        if y < r:

            if abs(x - self.room.exit_center) > self.room.exit_width / 2:
                force[1] += self.wall_strength * (r - y)

        return force

    # --------------------------

    def step(self):

        for agent in self.agents:

            if agent.evacuated:
                continue

            F = np.zeros(2)

            F += self.driving_force(agent)
            F += self.agent_repulsion(agent)
            F += self.wall_repulsion(agent)
            F += self.noise_strength * np.random.randn(2)

            agent.velocity += self.dt * F
            agent.position += self.dt * agent.velocity

            if agent.position[1] <= 0:

                if abs(agent.position[0] - self.room.exit_center) < self.room.exit_width / 2:
                    agent.evacuated = True

    # --------------------------

    def run(self, steps=500):

        history = []

        for _ in range(steps):

            self.step()

            positions = [
                agent.position.copy()
                for agent in self.agents
                if not agent.evacuated
            ]

            history.append(np.array(positions))

        return history


# =============================
# Run simulation
# =============================

sim = Simulation(80)

history = sim.run(600)

# =============================
# Visualization
# =============================

plt.figure()

for frame in history[::20]:

    if len(frame) > 0:
        plt.scatter(frame[:, 0], frame[:, 1], s=10)

plt.xlim(0, 20)
plt.ylim(0, 20)

plt.title("Crowd Evacuation Simulation")
plt.show()