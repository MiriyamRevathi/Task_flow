"""
Activity Repository Data Access Layer.
"""

from typing import List
from taskflow.models.activity import Activity
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class ActivityRepository(BaseRepository[Activity]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "activities", Activity)

    def get_by_workspace(self, workspace_id: str, limit: int = 50) -> List[Activity]:
        activities = self.filter(lambda a: a.workspace_id == workspace_id)
        activities.sort(key=lambda a: a.created_at, reverse=True)
        return activities[:limit]

    def get_by_project(self, project_id: str, limit: int = 50) -> List[Activity]:
        activities = self.filter(lambda a: a.project_id == project_id)
        activities.sort(key=lambda a: a.created_at, reverse=True)
        return activities[:limit]
