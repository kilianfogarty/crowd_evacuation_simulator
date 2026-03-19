"""Integration tests for the crowd evacuation simulator.

These tests run full end-to-end simulations and verify high-level outcomes.
The regression test specifically chooses a seed and asserts the result is deterministic.
"""

from __future__ import annotations

import os
import tempfile

import numpy as np
from crowd_evacuation_simulator import (
    Database,
    Environment,
    EnvironmentFactory,
    Simulation,
)


class TestIntegration:
    def test_result_stored_accurately(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")

            env: Environment = EnvironmentFactory.build_environment(
                width=20, height=20, num_agents=10, num_obstacles=0, seed=0
            )
            sim: Simulation = Simulation(env, dt=0.1)
            evac_time: float | None = sim.run()

            db: Database = Database(path=db_path)
            db.write_run(
                num_agents=10,
                num_obstacles=0,
                room_width=20,
                room_height=20,
                seed=0,
                evacuation_time=evac_time,
                all_evacuated=sim.all_evacuated,
            )
            cursor = db.connection.cursor()
            cursor.execute("SELECT evacuation_time, all_evacuated FROM evacuation_runs")
            row = cursor.fetchone()
            db.close()

            assert sim.all_evacuated is True
            assert evac_time is not None
            assert np.allclose(row[0], evac_time)
            assert row[1] == 1

    def test_fixed_seed_deterministic(self) -> None:
        """Same seed must produce identical evacuation times across multiple runs."""

        def run_once() -> float | None:
            env = EnvironmentFactory.build_environment(
                width=20, height=20, num_agents=5, num_obstacles=0, seed=7
            )
            return Simulation(env, dt=0.1).run()

        simulation_result_a: float | None = run_once()
        simulation_result_b: float | None = run_once()
        simulation_result_c: float | None = run_once()

        assert simulation_result_a is not None
        assert simulation_result_b is not None
        assert simulation_result_c is not None
        assert (
            np.allclose(simulation_result_a, simulation_result_b)
            and np.allclose(simulation_result_b, simulation_result_c)
            and np.allclose(simulation_result_a, simulation_result_c)
        )
