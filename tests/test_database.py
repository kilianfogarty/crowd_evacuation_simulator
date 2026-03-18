import csv
import os
import tempfile
import pytest
from crowd_evacuation_simulator.database import Database

class TestDatabase:
    
    # init
    def test_database_initialization_creates_connection(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            path = f.name
        try:
            db = Database(path)
            assert db.connection is not None
            db.close()
        finally:
            os.unlink(path)

    def test_initialization_creates_table(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            path = f.name
        try:
            db = Database(path)
            cursor = db.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='evacuation_runs'")
            assert cursor.fetchone() is not None
            db.close()
        finally:
            os.unlink(path)

    # write_run
    def test_write_run_inserts_one_row(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            path = f.name
        try:
            db = Database(path)
            db.write_run(30, 2, 20.0, 20.0, 0, 45.3, True)
            cursor = db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM evacuation_runs")
            assert cursor.fetchone()[0] == 1
            db.close()
        finally:
            os.unlink(path)

    def test_write_run_stores_correct_values(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            path = f.name
        try:
            db = Database(path)
            db.write_run(10, 0, 20.0, 20.0, 1, 22.1, True)
            cursor = db.connection.cursor()
            cursor.execute("SELECT num_agents, num_obstacles, seed, evacuation_time, all_evacuated FROM evacuation_runs")
            row = cursor.fetchone()
            assert row[0] == 10
            assert row[1] == 0
            assert row[2] == 1
            assert abs(row[3] - 22.1) < 0.001
            assert row[4] == 1
            db.close()
        finally:
            os.unlink(path)

    def test_write_run_bool_stored_as_integer(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            path = f.name
        try:
            db = Database(path)
            db.write_run(30, 0, 20.0, 20.0, 0, 40.0, True)
            cursor = db.connection.cursor()
            cursor.execute("SELECT all_evacuated FROM evacuation_runs")
            value = cursor.fetchone()[0]
            assert isinstance(value, int)
            assert value == 1
            db.close()
        finally:
            os.unlink(path)

    def test_write_run_none_evacuation_time(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            path = f.name
        try:
            db = Database(path)
            db.write_run(100, 5, 20.0, 20.0, 2, None, False)
            cursor = db.connection.cursor()
            cursor.execute("SELECT evacuation_time, all_evacuated FROM evacuation_runs")
            row = cursor.fetchone()
            assert row[0] is None
            assert row[1] == 0
            db.close()
        finally:
            os.unlink(path)

    def test_write_run_multiple_rows(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            path = f.name
        try:
            db = Database(path)
            db.write_run(10, 0, 20.0, 20.0, 0, 30.0, True)
            db.write_run(30, 2, 20.0, 20.0, 1, 55.0, True)
            db.write_run(50, 5, 20.0, 20.0, 2, None, False)
            cursor = db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM evacuation_runs")
            assert cursor.fetchone()[0] == 3
            db.close()
        finally:
            os.unlink(path)

    # export csv
    def test_export_csv_creates_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db = Database(os.path.join(tmpdir, "test.db"))
            db.write_run(30, 0, 20.0, 20.0, 0, 40.0, True)
            csv_path = os.path.join(tmpdir, "results.csv")
            db.export_csv(csv_path)
            assert os.path.exists(csv_path)
            db.close()

    def test_export_csv_correct_row_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db = Database(os.path.join(tmpdir, "test.db"))
            db.write_run(30, 0, 20.0, 20.0, 0, 40.0, True)
            db.write_run(30, 2, 20.0, 20.0, 1, 55.0, True)
            csv_path = os.path.join(tmpdir, "results.csv")
            db.export_csv(csv_path)
            with open(csv_path) as f:
                lines = f.readlines()
            assert len(lines) == 3  # header + 2 data rows
            db.close()

    def test_export_csv_has_correct_headers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db = Database(os.path.join(tmpdir, "test.db"))
            db.write_run(30, 0, 20.0, 20.0, 0, 40.0, True)
            csv_path = os.path.join(tmpdir, "results.csv")
            db.export_csv(csv_path)
            with open(csv_path) as f:
                headers = f.readline().strip().split(",")
            assert "num_agents" in headers
            assert "evacuation_time" in headers
            assert "all_evacuated" in headers
            db.close()

    def test_export_csv_empty_database(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db = Database(os.path.join(tmpdir, "test.db"))
            csv_path = os.path.join(tmpdir, "results.csv")
            db.export_csv(csv_path)
            with open(csv_path) as f:
                lines = f.readlines()
            assert len(lines) == 1  # header only
            db.close()