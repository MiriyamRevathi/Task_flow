"""
Analytics Metrics Calculator.
Calculates project completion rates, overdue percentages, task velocity, and workload distribution.
"""

from typing import List, Dict, Any
from taskflow.models.task import Task
from taskflow.models.project import Project


class MetricsCalculator:
    @staticmethod
    def calculate_project_metrics(project: Project, tasks: List[Task]) -> Dict[str, Any]:
        total_tasks = len(tasks)
        if total_tasks == 0:
            return {
                "total_tasks": 0,
                "done_tasks": 0,
                "completion_rate": 0.0,
                "overdue_tasks": 0,
                "overdue_rate": 0.0,
                "blocked_tasks": 0,
                "blocked_rate": 0.0,
            }

        done_count = sum(1 for t in tasks if t.status == "DONE")
        overdue_count = sum(1 for t in tasks if t.is_overdue())
        blocked_count = sum(1 for t in tasks if t.status == "BLOCKED")

        return {
            "total_tasks": total_tasks,
            "done_tasks": done_count,
            "completion_rate": round((done_count / total_tasks) * 100.0, 1),
            "overdue_tasks": overdue_count,
            "overdue_rate": round((overdue_count / total_tasks) * 100.0, 1),
            "blocked_tasks": blocked_count,
            "blocked_rate": round((blocked_count / total_tasks) * 100.0, 1),
        }
