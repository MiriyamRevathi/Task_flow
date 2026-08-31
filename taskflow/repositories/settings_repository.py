"""
Settings Repository Data Access Layer.
"""

from typing import Optional
from taskflow.models.settings import SystemSettings
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class SettingsRepository(BaseRepository[SystemSettings]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "settings", SystemSettings)

    def get_global_settings(self) -> SystemSettings:
        s = self.get_by_id("global")
        if not s:
            s = SystemSettings(id="global")
            self.save(s)
        return s
