"""
Notification Domain Model.
Represents user notifications for assignments, status changes, mentions, and system alerts.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from taskflow.models.enums import NotificationType


class Notification:
    def __init__(
        self,
        id: str,
        user_id: str,
        title: str,
        message: str,
        type: str = NotificationType.SYSTEM_ALERT.value,
        read: bool = False,
        link_url: str = "",
        project_id: Optional[str] = None,
        task_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.title = title.strip()
        self.message = message.strip()
        self.type = type if type in NotificationType.choices() else NotificationType.SYSTEM_ALERT.value
        self.read = read
        self.link_url = link_url
        self.project_id = project_id
        self.task_id = task_id
        self.actor_id = actor_id
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "read": self.read,
            "link_url": self.link_url,
            "project_id": self.project_id,
            "task_id": self.task_id,
            "actor_id": self.actor_id,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Notification":
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            title=data["title"],
            message=data["message"],
            type=data.get("type", NotificationType.SYSTEM_ALERT.value),
            read=data.get("read", False),
            link_url=data.get("link_url", ""),
            project_id=data.get("project_id"),
            task_id=data.get("task_id"),
            actor_id=data.get("actor_id"),
            created_at=data.get("created_at"),
        )
