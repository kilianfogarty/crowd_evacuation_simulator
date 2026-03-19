# crowd_evacuation_simulator
Evacuation simulator project inspired by SoftSwarm labs. Monitors the time it takes for agents to leave a 2d room based on the number of obstacles, agents, and room size.

# ToDo:
- Make it so that obstacles are generated first, agents cannot be randomly generated inside an obstacle or existing agent in the first place. Use a set to list obstacle and other agent positions for O(1) lookup?
- Multiple exits
- SciPy KDTree?
- Continue implementing fixtures.
- Experiment.py file that runs multiple simulations with random variables.
- Update Readme
- Allow user to select location of the single exit
