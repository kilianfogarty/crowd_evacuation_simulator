# crowd_evacuation_simulator
Evacuation simulator project inspired by SoftSwarm labs. Monitors the time it takes for agents to leave a 2d room based on the number of obstacles, agents, and room size.

# ToDo:
2. Make it so that obstacles are generated first, agents cannot be randomly generated inside an obstacle or existing agent in the first place. Use a set to list obstacle and other agent positions for O(1) lookup?
3. Multiple exits
5. C extension so that the simulation.step() function runs quicker?
6. Do not hardcode margins
7. Use conftest for fixtures.
8. Experiment.py file that runs multiple simulations with random variables.
