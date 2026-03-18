""" Run a single crowd evacuation simulation with configurable parameters.

Usage examples:
    python main.py
    python main.py --agents 50 --obstacles 3 --seed 42
    python main.py --agents 100 --obstacles 5 --seed 0 --dt 0.05
"""

from __future__ import annotations
import argparse
import numpy as np
from crowd_evacuation_simulator import Agent, Database, Environment, Exit, Obstacle, Simulation

def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="A single run of a crowd evacuation simulation."
    )
    parser.add_argument("--agents", type=int, default=30, help="Number of agents (default: 30)")
    parser.add_argument("--obstacles", type=int, default=0, help="Number of obstacles (default: 0)")
    parser.add_argument("--width", type=float, default=20.0, help="Room width in simulation units (default: 20)")
    parser.add_argument("--height", type=float, default=20.0, help="Room height in simulation units (default: 20)")
    parser.add_argument("--seed", type=int, default=0, help="Random seed (default: 0)")
    parser.add_argument("--dt", type=float, default=0.1, help="Timestep in seconds (default: 0.1)")
    parser.add_argument("--max-steps", type=int, default=2000, help="Max timesteps before quitting (default: 2000)")
    return parser.parse_args()

def build_environment(
        width: float,
        height: float,
        num_agents: int,
        num_obstacles: int,
        seed: int 
    ) -> Environment:
    """Build and populate an environment with provided agents, obstacles, and exits.
    
    Args:
        width (float): Room width in simulation units.
        height (float): Room height in simulation units.
        num_agents (int): Number of agents to place.
        num_obstacles (int): Number of obstacles to place.
        seed (int): Random seed for reproducible placement

    Returns:
        Environment: A populated environment ready to simulate.
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    env: Environment = Environment(width, height)

    env.add_exit(Exit([width - 2.0, height / 2.0], radius=1.0))

    margin = 0.1
    x_min, y_min = width * margin, height * margin
    x_max, y_max = width * (1 - margin), height * (1 - margin)

    for _ in range(num_agents):
        position = rng.uniform([x_min, y_min], [x_max, y_max])
        env.add_agent(Agent(position))

    for _ in range(num_obstacles):
        position = rng.uniform([x_min, y_min], [x_max, y_max])
        env.add_obstacle(Obstacle(position, radius=0.8))

    return env

def main() -> None:
    args = parse_args()

    env = build_environment(
        width=args.width,
        height=args.height,
        num_agents=args.agents,
        num_obstacles=args.obstacles,
        seed=args.seed
    )

    sim: Simulation = Simulation(env, dt=args.dt, max_steps=args.max_steps)
    evac_time: float | None = sim.run()

    if evac_time is not None:
        print(
            f"All {args.agents} agents evacuated in {evac_time:.1f}s "
            f"(obstacles = {args.obstacles}, seed = {args.seed})"
        )
    else:
        evacuated: int = sum(agent.evacuated for agent in env.agents)
        print(
            f"Reached max steps — {evacuated}/{args.agents} agents evacuated "
            f"(obstacles = {args.obstacles}, seed = {args.seed})"
        )
    
    db = Database()
    db.write_run(
        num_agents=args.agents,
        num_obstacles=args.obstacles,
        room_width=args.width,
        room_height=args.height,
        seed=args.seed,
        evacuation_time=evac_time,
        all_evacuated=sim.all_evacuated,
    )
    db.close()
    print("Result logged to results/simulation.db")


if __name__ == "__main__":
    main()