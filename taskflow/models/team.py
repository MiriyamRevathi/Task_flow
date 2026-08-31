"""
Team Domain Model.
Represents a group of users within an organization and workspace assigned to projects and tasks.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class Team:
    def __init__(
        self,
        id: str,
        organization_id: str,
        workspace_id: str,
        name: str,
        department: str = "Engineering",
        lead_id: str = "",
        member_ids: Optional[List[str]] = None,
        description: str = "",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.organization_id = organization_id
        self.workspace_id = workspace_id
        self.name = name.strip()
        self.department = department
        self.lead_id = lead_id
        self.member_ids = member_ids or []
        self.description = description
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "workspace_id": self.workspace_id,
            "name": self.name,
            "department": self.department,
            "lead_id": self.lead_id,
            "member_ids": self.member_ids,
            "member_count": len(self.member_ids),
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Team":
        return cls(
            id=data["id"],
            organization_id=data["organization_id"],
            workspace_id=data["workspace_id"],
            name=data["name"],
            department=data.get("department", "Engineering"),
            lead_id=data.get("lead_id", ""),
            member_ids=data.get("member_ids", []),
            description=data.get("description", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
