import sqlite3

class Database:
    def __init__(self, path="simulation.db"):
        self.connect = sqlite3.connext(path)
        self.create_tables

    def create_tables(self):
        cursor = self.connect.cursor
        