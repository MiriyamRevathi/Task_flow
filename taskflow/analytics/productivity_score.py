"""
Productivity Scoring Subsystem.
"""

from typing import List
from taskflow.models.task import Task


class ProductivityScore:
    @staticmethod
    def calculate_score(completed_tasks: int, total_tasks: int, overdue_tasks: int) -> float:
        if total_tasks == 0:
            return 100.0
        base = (completed_tasks / total_tasks) * 100.0
        penalty = (overdue_tasks / total_tasks) * 30.0
        return round(max(0.0, min(100.0, base - penalty)), 1)
