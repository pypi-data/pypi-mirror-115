"""Contains the new types for the action model learner."""
from typing import List, Literal

from SAM_models.trajectory_component import TrajectoryComponent

Trajectory = List[TrajectoryComponent]
Mode = Literal["production", "development"]
