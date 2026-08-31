"""
Calendar Event Repository Data Access Layer.
"""

from typing import List
from taskflow.models.calendar_event import CalendarEvent
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class CalendarRepository(BaseRepository[CalendarEvent]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "calendar_events", CalendarEvent)

    def get_by_workspace(self, workspace_id: str) -> List[CalendarEvent]:
        return self.filter(lambda e: e.workspace_id == workspace_id)

    def get_by_project(self, project_id: str) -> List[CalendarEvent]:
        return self.filter(lambda e: e.project_id == project_id)
