"""
Velocity Engine.
Computes completion velocity metrics.
"""

from typing import List
from taskflow.models.task import Task


class VelocityEngine:
    @staticmethod
    def calculate_weekly_velocity(tasks: List[Task]) -> float:
        done_tasks = [t for t in tasks if t.status == "DONE"]
        if not done_tasks:
            return 0.0
        total_hours = sum(t.estimated_hours or 1.0 for t in done_tasks)
        return round(total_hours / 4.0, 1)  # Average per week
