"""
Time Tracking Repository Data Access Layer.
"""

from typing import List, Optional
from taskflow.models.time_entry import TimeEntry
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class TimeRepository(BaseRepository[TimeEntry]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "time_entries", TimeEntry)

    def get_by_user(self, user_id: str) -> List[TimeEntry]:
        return self.filter(lambda t: t.user_id == user_id)

    def get_by_task(self, task_id: str) -> List[TimeEntry]:
        return self.filter(lambda t: t.task_id == task_id)

    def get_by_project(self, project_id: str) -> List[TimeEntry]:
        return self.filter(lambda t: t.project_id == project_id)

    def get_running_timer(self, user_id: str) -> Optional[TimeEntry]:
        return self.find_one(lambda t: t.user_id == user_id and t.is_running)
