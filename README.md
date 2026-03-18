# crowd_evacuation_simulator
Evacuation simulator project inspired by SoftSwarm labs. Monitors the time it takes for agents to leave a 2d room based on the number of obstacles, agents, and room size.

# ToDo:
1. Fix agent and obstacle with the same position leaving agent stranded. The agent needs to generate a random normalized direction vector to escape from the object rather than a 0 vector.
2. Make it so that obstacles are generated first, agents cannot be randomly generated inside an obstacle in the first place. Use a set to list obstacle and other agent positions for O(1) lookup?
3. Multiple exits
4. Improve speed for large amounts of agents
5. MyPy, Ruff, Pre-Commit, Pytest, PyTest coverage... maybe hypothesis
6. C extension so that the simulation.step() function runs quicker?
7. Do not hardcode margins
8. Use conftest for fixtures.
9. Experiment.py file that runs multiple simulations with random variables.
