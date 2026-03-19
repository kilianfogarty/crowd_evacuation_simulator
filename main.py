"""Run a batch of crowd evacuation simulations with configurable parameters.

Usage examples:
    python main.py
    python main.py --max-agents 50 --max-obstacles 3 --seeds 10
    python main.py --max-agents 30 --max-obstacles 3 --seeds 18 --exit-x 10 --exit-y 1
    python main.py --max-agents 100 --width 30 --height 30 --dt 0.05 --max-steps 5000
"""

from __future__ import annotations

import argparse

from crowd_evacuation_simulator import (
    Database,
    EnvironmentFactory,
    Simulation,
)


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Batch runner for the crowd evacuation simulation."
    )

    # entity ranges
    parser.add_argument(
        "--max-agents",
        type=int,
        default=30,
        help="Run simulation from 1 to this many agents (default: 30)",
    )
    parser.add_argument(
        "--max-obstacles",
        type=int,
        default=0,
        help="Run simulation from 0 to this many obstacles (default: 0)",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=1,
        help="Number of random seeds to run per configuration (default: 1)",
    )

    # room
    parser.add_argument(
        "--width",
        type=float,
        default=20.0,
        help="Room width in simulation units (default: 20)",
    )
    parser.add_argument(
        "--height",
        type=float,
        default=20.0,
        help="Room height in simulation units (default: 20)",
    )

    # exit
    parser.add_argument(
        "--exit-x",
        type=float,
        default=None,
        help="Exit x position (default: bottom wall center)",
    )
    parser.add_argument(
        "--exit-y",
        type=float,
        default=None,
        help="Exit y position (default: bottom wall center)",
    )
    parser.add_argument(
        "--exit-radius",
        type=float,
        default=1.0,
        help="Exit radius (default: 1.0)",
    )

    # sim
    parser.add_argument(
        "--dt",
        type=float,
        default=0.1,
        help="Timestep in seconds (default: 0.1)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=2000,
        help="Max timesteps before quitting (default: 2000)",
    )

    return parser.parse_args()


def run_single(
    num_agents: int,
    num_obstacles: int,
    seed: int,
    width: float,
    height: float,
    exit_x: float | None,
    exit_y: float | None,
    exit_radius: float,
    dt: float,
    max_steps: int,
) -> tuple[float | None, bool, int]:
    """Run a single simulation and return the result.

    Args:
        num_agents (int): Number of agents to place.
        num_obstacles (int): Number of obstacles to place.
        seed (int): Random seed for this run.
        width (float): Room width.
        height (float): Room height.
        exit_x (float | None): Exit x position, or None for default.
        exit_y (float | None): Exit y position, or None for default.
        exit_radius (float): Exit radius.
        dt (float): Timestep in seconds.
        max_steps (int): Maximum steps before stopping.

    Returns:
        tuple: (evacuation_time, all_evacuated, num_evacuated)
    """
    env = EnvironmentFactory.build_environment(
        width=width,
        height=height,
        num_agents=num_agents,
        num_obstacles=num_obstacles,
        seed=seed,
        exit_x=exit_x,
        exit_y=exit_y,
        exit_radius=exit_radius,
    )
    sim = Simulation(env, dt=dt, max_steps=max_steps)
    evac_time = sim.run()
    num_evacuated = sum(a.evacuated for a in env.agents)
    return evac_time, sim.all_evacuated, num_evacuated


def main() -> None:
    args = parse_args()

    agent_counts: range = range(1, args.max_agents + 1)
    obstacle_counts: range = range(1, args.max_obstacles + 1)
    seeds: range = range(args.seeds)

    non_zeros = [
        x for x in [len(agent_counts), len(obstacle_counts), len(seeds)] if x != 0
    ]
    total_runs: int = 1

    for num in non_zeros:
        total_runs *= num

    print(
        f"Running {total_runs} simulations ->"
        f"agents 1–{args.max_agents}, "
        f"obstacles 0–{args.max_obstacles}, "
        f"{args.seeds} seed(s) each"
    )
    print(
        f"Room area: {args.width}x{args.height}  "
        f"exit: ({args.exit_x or args.width / 2.0:.1f}, "
        f"{args.exit_y or (args.height - (args.height - 2)):.1f})  "
        f"radius: {args.exit_radius}"
    )

    db = Database()

    completed: int = 0

    for num_agents in agent_counts:
        for num_obstacles in obstacle_counts:
            for seed in seeds:
                evac_time, all_evacuated, num_evacuated = run_single(
                    num_agents=num_agents,
                    num_obstacles=num_obstacles,
                    seed=seed,
                    width=args.width,
                    height=args.height,
                    exit_x=args.exit_x,
                    exit_y=args.exit_y,
                    exit_radius=args.exit_radius,
                    dt=args.dt,
                    max_steps=args.max_steps,
                )

                db.write_run(
                    num_agents=num_agents,
                    num_obstacles=num_obstacles,
                    room_width=args.width,
                    room_height=args.height,
                    seed=seed,
                    evacuation_time=evac_time,
                    all_evacuated=all_evacuated,
                )

                completed += 1
                if evac_time is not None:
                    print(
                        f"[{completed}/{total_runs}] "
                        f"agents={num_agents}  "
                        f"obstacles={num_obstacles}  "
                        f"seed={seed}  "
                        f"-> {evac_time:.1f}s"
                    )
                else:
                    print(
                        f"[{completed}/{total_runs}] "
                        f"agents={num_agents}  "
                        f"obstacles={num_obstacles}  "
                        f"seed={seed}  "
                        f"-> incomplete ({num_evacuated}/{num_agents} evacuated)"
                    )

    db.close()
    print("Finished. Result logged to results/simulation.db")


if __name__ == "__main__":
    main()
