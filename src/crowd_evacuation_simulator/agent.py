import numpy as np
from .exit import Exit
from .obstacle import Obstacle

class Agent:
    """Single pedestrian in the crowd evacuation simulation."""
    def __init__(self, position: np.ndarray | list[float], speed: float = 1.5) -> None:
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
        norm: float = np.linalg.norm(diff)
        if norm == 0:
            return np.zeros(2)
        return diff / norm

    def apply_force(self, force: np.ndarray, dt: float) -> None:
        """Move the agent one timestep in the direction of the net force applied on it.

        Args: 
            force (np.ndarray): Net force vector acting on the agent.
            dr (float): Timestep duration in seconds.
        """
        norm: float = np.linalg.norm(force)
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
        distances = [np.linalg.norm(self.position - exit.position) for exit in exits]
        return exits[int(np.argmin(distances))]

    def repulsion_from_agent(self, other: Agent, strength: float =3.0) -> np.ndarray:
        """Return repulsion force vector away from another agent.
        
        The magnitude is inversely proportional to distance so nearby agents push harder than farther ones.

        Args:
            other (Agent): The agent to repel from.
            strength (float): Scalar multiplier for the force magnitude.

        Returns:
            np.ndarray: A 2D array representing the repulsion force vector pointing away from the other agent.
        """
        diff: np.ndarray = self.position - other.position
        distance: np.ndarray = np.linalg.norm(diff)
        direction: np.ndarray =  diff / distance

        # TODO: replace zero vector with random direction for more realistic collision.
        if distance == 0:
            return np.zeros(2)
        
        # Divide by distance again since the closer something is the stronger the repulsion - inverse.
        return (strength * direction) / distance
    
    def repulsion_from_obstacle(self, obstacle: Obstacle, strength: float = 3.0) -> np.ndarray:
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
        direction: np.ndarray =  diff / distance

        # TODO: replace zero vector with random direction when distance is zero.
        if distance == 0 or distance > obstacle.radius + 2.0:
            return np.zeros(2)

        return (strength * direction) / distance

    def repulsion_from_wall(self, width: float, height: float, strength: float = 2.0, threshold: float = 1.0) -> np.ndarray:
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
            force[0] += strength / x
        # Right wall
        if x > width - threshold:
            force[0] -= strength / x
        # Bottom wall
        if y < threshold:
            force[1] += strength / y
        # Top wall
        if y > height - threshold:
            force[1] -= strength / y

        return force



        





