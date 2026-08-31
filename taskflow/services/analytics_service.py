"""
Analytics Service.
"""

from typing import Dict, Any
from taskflow.repositories.project_repository import ProjectRepository
from taskflow.repositories.task_repository import TaskRepository
from taskflow.analytics.metrics_calculator import MetricsCalculator


class AnalyticsService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo

    def get_workspace_analytics(self, workspace_id: str) -> Dict[str, Any]:
        projects = self.project_repo.get_by_workspace(workspace_id)
        tasks = self.task_repo.get_by_workspace(workspace_id)

        total_projects = len(projects)
        active_projects = sum(1 for p in projects if p.status == "ACTIVE")
        total_tasks = len(tasks)
        done_tasks = sum(1 for t in tasks if t.status == "DONE")
        overdue_tasks = sum(1 for t in tasks if t.is_overdue())

        completion_rate = round((done_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0.0

        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "total_tasks": total_tasks,
            "done_tasks": done_tasks,
            "overdue_tasks": overdue_tasks,
            "completion_rate": completion_rate,
        }
