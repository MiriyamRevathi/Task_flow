"""
Reporting Service.
Generates comprehensive executive, project, team, productivity, time, and risk reports.
"""

from typing import Dict, Any
from taskflow.repositories.project_repository import ProjectRepository
from taskflow.repositories.task_repository import TaskRepository
from taskflow.repositories.user_repository import UserRepository
from taskflow.repositories.time_repository import TimeRepository


class ReportingService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        task_repo: TaskRepository,
        user_repo: UserRepository,
        time_repo: TimeRepository,
    ):
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.time_repo = time_repo

    def generate_executive_report(self, workspace_id: str) -> Dict[str, Any]:
        projects = self.project_repo.get_by_workspace(workspace_id)
        tasks = self.task_repo.get_by_workspace(workspace_id)
        users = self.user_repo.get_by_workspace(workspace_id)
        time_entries = self.time_repo.get_all()

        total_hours = sum(t.hours for t in time_entries)

        return {
            "report_title": "Executive Enterprise Performance Summary",
            "total_projects": len(projects),
            "total_tasks": len(tasks),
            "total_team_members": len(users),
            "total_hours_logged": round(total_hours, 2),
            "projects_summary": [p.to_dict() for p in projects],
        }
