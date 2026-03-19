# Crowd Evacuation Simulator
Simulates crowd evacuation in a 2D room. Agents navigate toward an exit
while avoiding other agents, obstacles, and walls. Results are logged to a
SQLite database after every run.

## Download
No Python required. Download `simulate.exe` from the
[latest release](https://github.com/kilianfogarty/crowd_evacuation_simulator/releases)
and run it from a terminal. WINDOWS ONLY.

## Usage
Open PowerShell or Command Prompt in the folder where you saved `simulate.exe`:
```powershell
# run with defaults
.\simulate.exe

# custom simulation
.\simulate.exe --max-agents 30 --exit-x 10 --exit-y 5 --exit-radius 2.0

# see all options
.\simulate.exe --help
```

Results are saved automatically to a `results/` folder in the same
directory as the executable.

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

## Exporting results to CSV
After running simulations, `results/simulation.db` and `results/results.csv` contains all your data.

## For Python users
```bash
git clone https://github.com/kilianfogarty/crowd_evacuation_simulator.git
cd crowd_evacuation_simulator
pip install -e .
python main.py --max-agents 30 --seeds 5
```

Run tests:
```bash
pytest
```
