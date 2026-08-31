"""
Activity Audit Log Domain Model.
Represents immutable application audit entries tracking who did what, when, and on which object.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from taskflow.models.enums import ActivityAction


class Activity:
    def __init__(
        self,
        id: str,
        actor_id: str,
        actor_name: str,
        action: str,
        target_type: str,  # PROJECT, TASK, MILESTONE, TEAM, USER, WORKSPACE
        target_id: str,
        target_name: str,
        description: str = "",
        workspace_id: str = "",
        project_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.actor_id = actor_id
        self.actor_name = actor_name
        self.action = action if action in ActivityAction.choices() else ActivityAction.UPDATE.value
        self.target_type = target_type
        self.target_id = target_id
        self.target_name = target_name
        self.description = description or f"{actor_name} performed {action} on {target_type.lower()} {target_name}"
        self.workspace_id = workspace_id
        self.project_id = project_id
        self.details = details or {}
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "actor_id": self.actor_id,
            "actor_name": self.actor_name,
            "action": self.action,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "target_name": self.target_name,
            "description": self.description,
            "workspace_id": self.workspace_id,
            "project_id": self.project_id,
            "details": self.details,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Activity":
        return cls(
            id=data["id"],
            actor_id=data["actor_id"],
            actor_name=data.get("actor_name", "User"),
            action=data.get("action", ActivityAction.UPDATE.value),
            target_type=data.get("target_type", "OBJECT"),
            target_id=data.get("target_id", ""),
            target_name=data.get("target_name", ""),
            description=data.get("description", ""),
            workspace_id=data.get("workspace_id", ""),
            project_id=data.get("project_id"),
            details=data.get("details", {}),
            created_at=data.get("created_at"),
        )
