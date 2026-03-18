import csv
import os
import sqlite3


class Database:
    """Handles persistence of simulation run results to SQLite database."""

    def __init__(self, path: str = "results/simulation.db") -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self) -> None:
        """Creates the evacuation_runs table if it does not already exist."""
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evacuation_runs (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                num_agents       INTEGER NOT NULL,
                num_obstacles    INTEGER NOT NULL,
                room_width       REAL    NOT NULL,
                room_height      REAL    NOT NULL,
                seed             INTEGER NOT NULL,
                evacuation_time  REAL,
                all_evacuated    INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def write_run(
        self,
        num_agents: int,
        num_obstacles: int,
        room_width: float,
        room_height: float,
        seed: int,
        evacuation_time: float | None,
        all_evacuated: bool,
    ) -> None:
        """Insert one simulation run into the database.

        Args:
            num_agents (int): Number of agents in the run.
            num_obstacles (int): Number of obstacles in the run.
            room_width (float): Width of the environment.
            room_height (float): Height of the environment.
            seed (int): Random seed used for this run.
            evacuation_time (float | None): Time for all agents to evacuate,
            or None if max_steps was reached before full evacuation.
            all_evacuated (bool): Whether all agents evacuated successfully.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO evacuation_runs
                (num_agents, num_obstacles, room_width, room_height, seed, evacuation_time, all_evacuated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                num_agents,
                num_obstacles,
                room_width,
                room_height,
                seed,
                evacuation_time,
                int(all_evacuated),
            ),
        )
        self.connection.commit()

    def export_csv(self, path: str = "results/results.csv") -> None:
        """Exports all runs to a CSV file at the given path.

        Args:
            path (str): Destination file path for the CSV output.
        """

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM evacuation_runs")
        rows = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()
