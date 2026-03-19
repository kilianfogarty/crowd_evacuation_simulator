"""Shared fixtures for the crowd evacuation simulator test suite."""

from __future__ import annotations

from typing import Generator

import os
import tempfile

import pytest

from crowd_evacuation_simulator import (
    Agent,
    Database,
    Environment,
    Exit,
    Simulation,
)
from crowd_evacuation_simulator.environment_factory import EnvironmentFactory


# environment fixtures


@pytest.fixture
def basic_environment() -> Environment:
    """Standard 20x20 environment with 10 agents and no obstacles."""
    return EnvironmentFactory.build_environment(
        width=20, height=20, num_agents=10, num_obstacles=0, seed=0
    )


@pytest.fixture
def environment_with_obstacles() -> Environment:
    """Standard 20x20 environment with 10 agents and 3 obstacles."""
    return EnvironmentFactory.build_environment(
        width=20, height=20, num_agents=10, num_obstacles=3, seed=0
    )


@pytest.fixture
def empty_environment() -> Environment:
    """Empty 20x20 environment with one exit and no agents or obstacles."""
    env = Environment(20, 20)
    env.add_exit(Exit([18, 10], radius=1.0))
    return env


# agent fixtures


@pytest.fixture
def single_agent() -> Agent:
    """A single agent at the left-centre of a 20x20 room."""
    return Agent([1, 1], speed=1.0)


@pytest.fixture
def agent_at_exit() -> Agent:
    """An agent already positioned at the exit."""
    return Agent([18, 10])


# simulation fixtures


@pytest.fixture
def basic_simulation(basic_env: Environment) -> Simulation:
    """A ready-to-run simulation using the basic environment."""
    return Simulation(basic_env, dt=0.1)


# database fixtures


@pytest.fixture
def temp_db() -> Generator[Database, None, None]:
    """A temporary database that always closes before the temp directory is deleted.

    Uses yield so teardown runs even if the test raises an exception —
    this prevents the Windows PermissionError when SQLite holds a file lock.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(path=db_path)
        yield db
        db.close()


@pytest.fixture
def populated_db(temp_db: Database) -> Database:
    """A temporary database pre-populated with three simulation runs."""
    temp_db.write_run(10, 0, 20.0, 20.0, 0, 18.3, True)
    temp_db.write_run(30, 2, 20.0, 20.0, 1, 47.1, True)
    temp_db.write_run(50, 5, 20.0, 20.0, 2, None, False)
    return temp_db
