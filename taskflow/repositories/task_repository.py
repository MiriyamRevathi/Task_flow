"""
Task Repository Data Access Layer.
"""

from typing import List
from taskflow.models.task import Task
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class TaskRepository(BaseRepository[Task]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "tasks", Task)

    def get_by_project(self, project_id: str) -> List[Task]:
        return self.filter(lambda t: t.project_id == project_id)

    def get_by_workspace(self, workspace_id: str) -> List[Task]:
        return self.filter(lambda t: t.workspace_id == workspace_id)

    def get_by_assignee(self, assignee_id: str) -> List[Task]:
        return self.filter(lambda t: t.assignee_id == assignee_id)

    def get_by_status(self, project_id: str, status: str) -> List[Task]:
        return self.filter(lambda t: t.project_id == project_id and t.status == status)

    def get_overdue_tasks(self, workspace_id: str) -> List[Task]:
        return [t for t in self.get_by_workspace(workspace_id) if t.is_overdue()]
