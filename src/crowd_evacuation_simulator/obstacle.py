from __future__ import annotations

import numpy as np


class Obstacle:
    """A static object in the environment that agents must navigate around."""

    def __init__(self, position: np.ndarray | list[float], radius: float) -> None:
        self.position: np.ndarray = np.array(position, dtype=float)
        self.radius: float = radius
