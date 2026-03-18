# crowd_evacuation_simulator
Evacuation simulator project inspired by SoftSwarm labs. Monitors the time it takes for agents to leave a 2d room based on the number of obstacles, agents, and room size.

# ToDo:
1. Fix agent and obstacle with the same position leaving agent stranded. The agent needs to generate a random normalized direction vector to escape from the object rather than a 0 vector.
2. Make it so that obstacles are generated first, agents cannot be randomly generated inside an obstacle in the first place.
3. Multiple exits
4. Improve speed for large amounts of agents
5. MyPy, Ruff, Pre-Commit, Pytest, PyTest coverage... maybe hypothesis
