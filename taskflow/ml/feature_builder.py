"""
ML Feature Builder.
Extracts 9 quantitative numerical features from project, task, and team datasets for risk prediction modeling.
"""

from typing import List, Dict, Any
import numpy as np
from taskflow.models.project import Project
from taskflow.models.task import Task


class MLFeatureBuilder:
    FEATURE_NAMES = [
        "overdue_ratio",
        "completion_velocity",
        "task_backlog_ratio",
        "blocked_task_ratio",
        "avg_task_completion_hours",
        "milestone_delay_ratio",
        "team_workload_capacity",
        "project_age_days",
        "remaining_task_count",
    ]

    @classmethod
    def extract_project_features(cls, project: Project, tasks: List[Task]) -> List[float]:
        total_tasks = max(1, len(tasks))
        done_tasks = [t for t in tasks if t.status == "DONE"]
        overdue_tasks = [t for t in tasks if t.is_overdue()]
        blocked_tasks = [t for t in tasks if t.status == "BLOCKED"]
        backlog_tasks = [t for t in tasks if t.status in ("BACKLOG", "TODO")]

        overdue_ratio = len(overdue_tasks) / total_tasks
        completion_velocity = len(done_tasks) / float(max(1, total_tasks))
        backlog_ratio = len(backlog_tasks) / total_tasks
        blocked_ratio = len(blocked_tasks) / total_tasks

        actual_hours = [t.actual_hours for t in done_tasks if t.actual_hours > 0]
        avg_completion_hours = float(np.mean(actual_hours)) if actual_hours else 12.0

        milestone_delay_ratio = 0.2 if project.is_overdue() else 0.05
        team_workload_capacity = float(len(project.member_ids) * 5)
        project_age_days = 30.0
        remaining_tasks = float(total_tasks - len(done_tasks))

        return [
            round(overdue_ratio, 4),
            round(completion_velocity, 4),
            round(backlog_ratio, 4),
            round(blocked_ratio, 4),
            round(avg_completion_hours, 2),
            round(milestone_delay_ratio, 4),
            round(team_workload_capacity, 2),
            round(project_age_days, 1),
            round(remaining_tasks, 1),
        ]
