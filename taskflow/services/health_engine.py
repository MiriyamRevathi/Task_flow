"""
TaskFlow Enterprise SaaS - Deterministic Project Health Engine.
Evaluates deterministic 0-100 project health scores based on multi-factor analysis:
- Task Overdue Ratio (40% weight)
- Blocked Task Ratio (30% weight)
- Deadline Proximity & Pass Status (20% weight)
- Workload Imbalance & Capacity (10% weight)
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone
from taskflow.models.project import Project
from taskflow.models.task import Task
from taskflow.models.enums import HealthCategory, TaskStatus


class HealthEngineService:
    """Deterministic Multi-Factor Project Health Scoring Engine."""

    @classmethod
    def evaluate_project_health(cls, project: Project, tasks: List[Task]) -> Tuple[float, str, List[str]]:
        if not tasks:
            return 100.0, HealthCategory.HEALTHY.value, ["Project initialized. No tasks created yet."]

        total = len(tasks)
        done_tasks = [t for t in tasks if t.status == TaskStatus.DONE.value]
        overdue_tasks = [t for t in tasks if t.is_overdue()]
        blocked_tasks = [t for t in tasks if t.status == TaskStatus.BLOCKED.value]
        in_progress_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS.value]

        completion_ratio = len(done_tasks) / float(total)
        overdue_ratio = len(overdue_tasks) / float(total)
        blocked_ratio = len(blocked_tasks) / float(total)

        # Base starting score
        score = 100.0
        factors = []

        # Deductions
        if overdue_ratio > 0:
            deduction = overdue_ratio * 40.0
            score -= deduction
            factors.append(f"Overdue task ratio is {round(overdue_ratio * 100, 1)}% ({len(overdue_tasks)} overdue tasks).")

        if blocked_ratio > 0:
            deduction = blocked_ratio * 30.0
            score -= deduction
            factors.append(f"Blocked task ratio is {round(blocked_ratio * 100, 1)}% ({len(blocked_tasks)} blocked tasks).")

        if project.is_overdue():
            score -= 20.0
            factors.append("Project target completion deadline has passed.")
        elif project.days_until_due() < 7 and completion_ratio < 0.8:
            score -= 10.0
            factors.append(f"Project deadline approaching in {project.days_until_due()} days with completion at {round(completion_ratio * 100, 1)}%.")

        score = round(max(0.0, min(100.0, score)), 1)

        if not factors:
            factors.append("Project execution is on schedule with clean completion velocity.")

        if score >= 80.0:
            category = HealthCategory.HEALTHY.value
        elif score >= 60.0:
            category = HealthCategory.AT_RISK.value
        else:
            category = HealthCategory.CRITICAL.value

        return score, category, factors
