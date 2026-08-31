"""
Project Repository Data Access Layer.
"""

from typing import List, Optional
from taskflow.models.project import Project
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "projects", Project)

    def get_by_workspace(self, workspace_id: str) -> List[Project]:
        return self.filter(lambda p: p.workspace_id == workspace_id)

    def get_by_key(self, key: str) -> Optional[Project]:
        k_clean = key.upper().strip()
        return self.find_one(lambda p: p.key == k_clean)

    def get_active_projects(self, workspace_id: str) -> List[Project]:
        return self.filter(lambda p: p.workspace_id == workspace_id and p.status in ("PLANNING", "ACTIVE"))
