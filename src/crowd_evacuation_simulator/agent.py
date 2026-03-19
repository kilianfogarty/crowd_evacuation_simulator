from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .exit import Exit
    from .obstacle import Obstacle

DEFAULT_AGENT_SPEED: float = 1.5
DEFAULT_REPULSION_STRENGTH_OTHER_AGENT: float = 1.5
DEFAULT_REPULSION_STRENGTH_OBSTACLE: float = 3.0
DEFAULT_REPULSION_STRENGTH_WALL: float = 5.0
DEFAULT_WALL_THRESHOLD: float = 1.5


class Agent:
    """Single pedestrian in the crowd evacuation simulation."""

    def __init__(
        self,
        position: np.ndarray | list[float],
        speed: float = DEFAULT_AGENT_SPEED,
    ) -> None:
        self.position: np.ndarray = np.array(position, dtype=float)
        self.speed: float = speed
        self.evacuated: bool = False

    def direction_to(self, target: np.ndarray) -> np.ndarray:
        """Return unit vector from agent position to go towards target

        Returns a zero vector if the agent is already at the target.

        Args:
            target (np.ndarray): the 2D target position

        Returns:
            np.ndarray: A 2D unit vector or a zero vector if the distance to target is zero.
        """
        diff: np.ndarray = target - self.position
        norm: float = float(np.linalg.norm(diff))
        if norm == 0:
            return np.zeros(2)
        return diff / norm

    def apply_force(self, force: np.ndarray, dt: float) -> None:
        """Move the agent one timestep in the direction of the net force applied on it.

        Args:
            force (np.ndarray): Net force vector acting on the agent.
            dt (float): Timestep duration in seconds.
        """
        norm: float = float(np.linalg.norm(force))
        if norm == 0:
            return
        # Direction is a unit vector. Magnitude is controlled by agent speed field.
        direction = force / norm
        self.position += direction * self.speed * dt

    def nearest_exit(self, exits: list[Exit]) -> Exit:
        """Return the closest exit based on Euclidean distance.

        Args:
            exits (list[Exit]): List of exits from an environment field.

        Returns:
            Exit: The exit nearest to the agent's current position.

        Raises:
            ValueError: If the provided list of exits is empty.
        """
        if not exits:
            raise ValueError("No exits in provided list from environment")
        distances = [
            np.linalg.norm(self.position - exit.position) for exit in exits
        ]
        return exits[int(np.argmin(distances))]

    def repulsion_from_agent(
        self,
        other: Agent,
        strength: float = DEFAULT_REPULSION_STRENGTH_OTHER_AGENT,
    ) -> np.ndarray:
        """Return repulsion force vector away from another agent.

        The magnitude is inversely proportional to distance so nearby agents push harder than farther ones.

        Args:
            other (Agent): The agent to repel from.
            strength (float): Scalar multiplier for the force magnitude.

        Returns:
            np.ndarray: A 2D array representing the repulsion force vector pointing away from the other agent.
        """
        diff: np.ndarray = self.position - other.position
        distance: float = float(np.linalg.norm(diff))

        if np.allclose(distance, 0):
            angle: float = np.random.uniform(
                0, 2 * np.pi
            )  # angle can be from 0 -> 2pi
            return np.array([np.cos(angle), np.sin(angle)])

        direction: np.ndarray = diff / distance

        # Divide by distance again since the closer something is the stronger the repulsion - inverse.
        return (strength * direction) / distance

    def repulsion_from_obstacle(
        self,
        obstacle: Obstacle,
        strength: float = DEFAULT_REPULSION_STRENGTH_OBSTACLE,
    ) -> np.ndarray:
        """Return repulsion force vector away from an obstacle.

        Returns a zero vector if the agent is beyond the obstacle radius + 2.0 units.

        Args:
            obstacle (Obstacle): The obstacle to repel from.
            strength (float): Scalar multiplier for the force magnitude.

        Returns:
            np.ndarray: A 2D array representing the repulsion force vector pointing away from the obstacle.
        """
        diff = self.position - obstacle.position
        distance = np.linalg.norm(diff)

        if np.allclose(distance, 0):
            angle: float = np.random.uniform(
                0, 2 * np.pi
            )  # angle can be from 0 -> 2pi
            return np.array([np.cos(angle), np.sin(angle)])

        if distance > obstacle.radius + 2.0:
            return np.zeros(2)

        direction: np.ndarray = diff / distance

        return (strength * direction) / distance

    def repulsion_from_wall(
        self,
        width: float,
        height: float,
        strength: float = DEFAULT_REPULSION_STRENGTH_WALL,
        threshold: float = DEFAULT_WALL_THRESHOLD,
    ) -> np.ndarray:
        """Return repulsion force pushing the agent away from room boundaries.

        Each wall contributes an inward force when the agent is within
        threshold units of that edge.

        Args:
            width (float): Room width in simulation units.
            height (float): Room height in simulation units.
            strength (float): Scalar multiplier for the wall force.
            threshold (float): Distance from a wall at which repulsion begins.

        Returns:
            np.ndarray: A 2D array representing the net wall repulsion force vector.
        """
        force: np.ndarray = np.zeros(2)
        x, y = self.position

        # Left wall
        if x < threshold:
            force[0] += strength / max(x, 1e-5)
        # Right wall
        if x > width - threshold:
            force[0] -= strength / max(width - x, 1e-5)
        # Bottom wall
        if y < threshold:
            force[1] += strength / max(y, 1e-5)
        # Top wall
        if y > height - threshold:
            force[1] -= strength / max(height - y, 1e-5)

        return force
