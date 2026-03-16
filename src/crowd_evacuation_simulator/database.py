import sqlite3

class Database:
    def __init__(self, path="simulation.db"):
        self.connect = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self):
        cursor = self.connect.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evacuation_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_agents INTEGER,
                num_obstacles INTEGER,
                room_width REAL,
                room_height REAL,
                evacuation_time REAL
            )
        """)
        self.connect.commit()