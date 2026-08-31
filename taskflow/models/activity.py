"""
TaskFlow Enterprise SaaS - Activity Audit Trail Domain Model.
Represents an immutable activity audit record tracking actor, action, target resource, diff changes, and client metadata.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from taskflow.models.enums import ActivityAction


class Activity:
    """Activity domain entity representing immutable audit trail logs."""

    def __init__(
        self,
        id: str,
        workspace_id: str,
        actor_id: str,
        actor_name: str,
        action: str,
        target_type: str,
        target_id: str,
        target_name: str,
        details: str = "",
        changes: Optional[Dict[str, Any]] = None,
        ip_address: str = "127.0.0.1",
        user_agent: str = "",
        created_at: Optional[str] = None,
    ):
        self.id = str(id).strip()
        self.workspace_id = str(workspace_id).strip()
        self.actor_id = str(actor_id).strip()
        self.actor_name = str(actor_name).strip()
        self.action = action if action in ActivityAction.choices() else ActivityAction.UPDATE.value
        self.target_type = str(target_type).upper().strip()
        self.target_id = str(target_id).strip()
        self.target_name = str(target_name).strip()
        self.details = str(details).strip()
        self.changes = changes or {}
        self.ip_address = str(ip_address).strip()
        self.user_agent = str(user_agent).strip()
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "actor_id": self.actor_id,
            "actor_name": self.actor_name,
            "action": self.action,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "target_name": self.target_name,
            "details": self.details,
            "changes": self.changes,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Activity":
        return cls(
            id=data["id"],
            workspace_id=data["workspace_id"],
            actor_id=data["actor_id"],
            actor_name=data.get("actor_name", ""),
            action=data.get("action", ActivityAction.UPDATE.value),
            target_type=data.get("target_type", "TASK"),
            target_id=data.get("target_id", ""),
            target_name=data.get("target_name", ""),
            details=data.get("details", ""),
            changes=data.get("changes"),
            ip_address=data.get("ip_address", "127.0.0.1"),
            user_agent=data.get("user_agent", ""),
            created_at=data.get("created_at"),
        )

    def __repr__(self) -> str:
        return f"<Activity {self.id}: {self.actor_name} {self.action} {self.target_type} '{self.target_name}'>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Activity):
            return False
        return self.id == other.id
