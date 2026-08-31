"""
Deterministic Project Health Engine.
Calculates deterministic health scores (0-100) and categorizes projects as HEALTHY, AT_RISK, or CRITICAL.
"""

from typing import List, Dict, Any, Tuple
from taskflow.models.project import Project
from taskflow.models.task import Task
from taskflow.models.enums import HealthCategory


class HealthEngineService:
    @classmethod
    def evaluate_project_health(cls, project: Project, tasks: List[Task]) -> Tuple[float, str, List[str]]:
        if not tasks:
            return 100.0, HealthCategory.HEALTHY.value, ["No tasks defined yet."]

        total = len(tasks)
        done_count = sum(1 for t in tasks if t.status == "DONE")
        overdue_count = sum(1 for t in tasks if t.is_overdue())
        blocked_count = sum(1 for t in tasks if t.status == "BLOCKED")

        completion_ratio = done_count / total
        overdue_ratio = overdue_count / total
        blocked_ratio = blocked_count / total

        # Score calculation formula
        score = 100.0
        score -= (overdue_ratio * 40.0)
        score -= (blocked_ratio * 30.0)
        if project.is_overdue():
            score -= 20.0

        score = round(max(0.0, min(100.0, score)), 1)

        factors = []
        if overdue_ratio > 0.15:
            factors.append(f"High overdue task ratio ({round(overdue_ratio * 100)}%)")
        if blocked_ratio > 0.10:
            factors.append(f"Multiple tasks currently BLOCKED ({blocked_count} tasks)")
        if project.is_overdue():
            factors.append("Project due date has passed.")

        if score >= 80.0:
            category = HealthCategory.HEALTHY.value
        elif score >= 60.0:
            category = HealthCategory.AT_RISK.value
        else:
            category = HealthCategory.CRITICAL.value

        return score, category, factors
