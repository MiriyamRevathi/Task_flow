"""
Project Lifecycle Service.
"""

from typing import List, Optional, Tuple, Dict, Any
from taskflow.repositories.project_repository import ProjectRepository
from taskflow.repositories.task_repository import TaskRepository
from taskflow.models.project import Project
from taskflow.models.enums import ProjectStatus, ProjectPriority
from taskflow.utils.id_generator import generate_id
from taskflow.utils.string_utils import generate_project_key


class ProjectService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo

    def get_workspace_projects(self, workspace_id: str) -> List[Project]:
        return self.project_repo.get_by_workspace(workspace_id)

    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        return self.project_repo.get_by_id(project_id)

    def create_project(
        self,
        workspace_id: str,
        org_id: str,
        name: str,
        description: str,
        owner_id: str,
        priority: str = "MEDIUM",
        budget: float = 0.0,
        start_date: Optional[str] = None,
        due_date: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Tuple[Optional[Project], str]:
        if not name:
            return None, "Project name is required."

        proj_id = generate_id("proj")
        key = generate_project_key(name)

        new_proj = Project(
            id=proj_id,
            workspace_id=workspace_id,
            organization_id=org_id,
            name=name,
            key=key,
            description=description,
            owner_id=owner_id,
            priority=priority,
            budget=budget,
            start_date=start_date,
            due_date=due_date,
            tags=tags or [],
        )
        self.project_repo.save(new_proj)
        return new_proj, "Project created successfully."

    def update_progress(self, project_id: str) -> float:
        proj = self.project_repo.get_by_id(project_id)
        if not proj:
            return 0.0
        tasks = self.task_repo.get_by_project(project_id)
        if not tasks:
            proj.progress_percentage = 0.0
        else:
            done_count = sum(1 for t in tasks if t.status == "DONE")
            proj.progress_percentage = round((done_count / len(tasks)) * 100.0, 1)

        self.project_repo.save(proj)
        return proj.progress_percentage
