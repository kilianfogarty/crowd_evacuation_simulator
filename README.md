# Crowd Evacuation Simulator

Simulates crowd evacuation in a 2D room. Agents navigate toward an exit 
while avoiding other agents, obstacles, and walls. Results are logged to a 
SQLite database for analysis.


## Installation

Requires Python 3.11+.
```bash
git clone https://github.com/kilianfogarty/crowd_evacuation_simulator.git
cd crowd_evacuation_simulator
pip install -e .
```

---

## Usage
```bash
# run with defaults — 1 to 30 agents, no obstacles, 1 seed
python main.py

# vary agents and obstacles across multiple seeds
python main.py --max-agents 50 --max-obstacles 3 --seeds 5

# custom exit position
python main.py --max-agents 30 --exit-x 10 --exit-y 5 --exit-radius 2.0

# larger room
python main.py --max-agents 100 --width 40 --height 40 --seeds 3
```

---

## Options

| Flag | Default | Description |
|---|---|---|
| `--max-agents` | 30 | Simulate 1 up to this many agents |
| `--max-obstacles` | 0 | Simulate 0 up to this many obstacles |
| `--seeds` | 1 | Random seeds per configuration |
| `--width` | 20.0 | Room width |
| `--height` | 20.0 | Room height |
| `--exit-x` | right wall | Exit x coordinate |
| `--exit-y` | mid height | Exit y coordinate |
| `--exit-radius` | 1.0 | Exit radius |
| `--dt` | 0.1 | Timestep in seconds |
| `--max-steps` | 2000 | Steps before stopping |

---

## Results

Every run is logged to `results/simulation.db`. Export to CSV:
```python
from crowd_evacuation_simulator import Database

db = Database()
db.export_csv("results/results.csv")
db.close()
```

---

## Run tests
```bash
pytest
pytest --cov=crowd_evacuation_simulator --cov-report=term-missing
```
