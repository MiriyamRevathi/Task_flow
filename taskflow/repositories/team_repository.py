"""
Team Repository Data Access Layer.
"""

from typing import List
from taskflow.models.team import Team
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class TeamRepository(BaseRepository[Team]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "teams", Team)

    def get_by_workspace(self, workspace_id: str) -> List[Team]:
        return self.filter(lambda t: t.workspace_id == workspace_id)
