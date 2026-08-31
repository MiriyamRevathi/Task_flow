"""
Notification Service.
"""

from typing import List
from taskflow.repositories.notification_repository import NotificationRepository
from taskflow.models.notification import Notification
from taskflow.utils.id_generator import generate_id


class NotificationService:
    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        return self.notification_repo.get_by_user(user_id, unread_only)

    def create_notification(self, user_id: str, title: str, message: str, type: str = "SYSTEM_ALERT", link_url: str = ""):
        n = Notification(
            id=generate_id("notif"),
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            link_url=link_url,
        )
        self.notification_repo.save(n)
        return n

    def mark_all_read(self, user_id: str):
        self.notification_repo.mark_all_as_read(user_id)
