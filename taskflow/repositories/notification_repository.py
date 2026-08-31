"""
Notification Repository Data Access Layer.
"""

from typing import List
from taskflow.models.notification import Notification
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "notifications", Notification)

    def get_by_user(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        if unread_only:
            return self.filter(lambda n: n.user_id == user_id and not n.read)
        return self.filter(lambda n: n.user_id == user_id)

    def mark_all_as_read(self, user_id: str):
        notifications = self.get_by_user(user_id, unread_only=True)
        for n in notifications:
            n.read = True
            self.save(n)
