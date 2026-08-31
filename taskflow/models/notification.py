"""
TaskFlow Enterprise SaaS - Notification Domain Model.
Represents system alerts, task assignments, deadline warnings, status changes, and user notifications.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from taskflow.models.enums import NotificationType


class Notification:
    """Notification domain entity representing user system alerts."""

    def __init__(
        self,
        id: str,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = NotificationType.SYSTEM_ALERT.value,
        target_url: str = "",
        actor_id: Optional[str] = None,
        actor_name: str = "",
        is_read: bool = False,
        read_at: Optional[str] = None,
        created_at: Optional[str] = None,
    ):
        self.id = str(id).strip()
        self.user_id = str(user_id).strip()
        self.title = str(title).strip()
        self.message = str(message).strip()
        self.notification_type = (
            notification_type
            if notification_type in NotificationType.choices()
            else NotificationType.SYSTEM_ALERT.value
        )
        self.target_url = str(target_url).strip()
        self.actor_id = actor_id
        self.actor_name = str(actor_name).strip()
        self.is_read = bool(is_read)
        self.read_at = read_at
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso

    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.now(timezone.utc).isoformat()

    def mark_as_unread(self):
        self.is_read = False
        self.read_at = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type,
            "target_url": self.target_url,
            "actor_id": self.actor_id,
            "actor_name": self.actor_name,
            "is_read": self.is_read,
            "read_at": self.read_at,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Notification":
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            title=data["title"],
            message=data["message"],
            notification_type=data.get(
                "notification_type", NotificationType.SYSTEM_ALERT.value
            ),
            target_url=data.get("target_url", ""),
            actor_id=data.get("actor_id"),
            actor_name=data.get("actor_name", ""),
            is_read=data.get("is_read", False),
            read_at=data.get("read_at"),
            created_at=data.get("created_at"),
        )

    def __repr__(self) -> str:
        return f"<Notification {self.id}: {self.title} (read={self.is_read})>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Notification):
            return False
        return self.id == other.id
