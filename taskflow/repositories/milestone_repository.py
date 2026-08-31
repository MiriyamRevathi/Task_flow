"""
Milestone Repository Data Access Layer.
"""

from typing import List
from taskflow.models.milestone import Milestone
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class MilestoneRepository(BaseRepository[Milestone]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "milestones", Milestone)

    def get_by_project(self, project_id: str) -> List[Milestone]:
        return self.filter(lambda m: m.project_id == project_id)

    def get_by_workspace(self, workspace_id: str) -> List[Milestone]:
        return self.filter(lambda m: m.workspace_id == workspace_id)
