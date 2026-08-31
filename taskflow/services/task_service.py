"""
Task Management Service.
Handles task workflows, subtasks, checklists, dependencies, and comments.
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timezone
from taskflow.repositories.task_repository import TaskRepository
from taskflow.repositories.project_repository import ProjectRepository
from taskflow.models.task import Task
from taskflow.models.enums import TaskStatus, TaskPriority
from taskflow.utils.id_generator import generate_id


class TaskService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def get_workspace_tasks(self, workspace_id: str) -> List[Task]:
        return self.task_repo.get_by_workspace(workspace_id)

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return self.task_repo.get_by_id(task_id)

    def create_task(
        self,
        project_id: str,
        workspace_id: str,
        title: str,
        creator_id: str,
        description: str = "",
        assignee_id: Optional[str] = None,
        priority: str = "MEDIUM",
        due_date: Optional[str] = None,
        estimated_hours: float = 0.0,
    ) -> Tuple[Optional[Task], str]:
        if not title:
            return None, "Task title is required."

        task_id = generate_id("task")
        new_task = Task(
            id=task_id,
            project_id=project_id,
            workspace_id=workspace_id,
            title=title,
            description=description,
            creator_id=creator_id,
            assignee_id=assignee_id,
            priority=priority,
            due_date=due_date,
            estimated_hours=estimated_hours,
        )
        self.task_repo.save(new_task)
        return new_task, "Task created successfully."

    def update_task_status(self, task_id: str, new_status: str) -> Tuple[Optional[Task], str]:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None, "Task not found."

        old_status = task.status
        task.status = new_status
        if new_status == TaskStatus.DONE.value and old_status != TaskStatus.DONE.value:
            task.completed_at = datetime.now(timezone.utc).isoformat()

        self.task_repo.save(task)
        return task, f"Task status updated from {old_status} to {new_status}."

    def add_comment(self, task_id: str, author_id: str, author_name: str, content: str) -> bool:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return False

        comment = {
            "id": generate_id("cmt"),
            "author_id": author_id,
            "author_name": author_name,
            "content": content,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        task.comments.append(comment)
        self.task_repo.save(task)
        return True
