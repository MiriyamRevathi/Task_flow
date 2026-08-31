"""
Report Repository Data Access Layer.
"""

from typing import List
from taskflow.models.report import Report
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class ReportRepository(BaseRepository[Report]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "reports", Report)

    def get_by_workspace(self, workspace_id: str) -> List[Report]:
        return self.filter(lambda r: r.workspace_id == workspace_id)
