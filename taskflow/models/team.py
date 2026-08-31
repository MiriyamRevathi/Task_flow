"""
TaskFlow Enterprise SaaS - Team Domain Model.
Represents a collaborative team grouping within a workspace with assigned members, leads, and department metrics.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class Team:
    """Team domain entity representing user teams."""

    def __init__(
        self,
        id: str,
        workspace_id: str,
        organization_id: str,
        name: str,
        description: str = "",
        lead_id: str = "",
        member_ids: Optional[List[str]] = None,
        department: str = "Engineering",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = str(id).strip()
        self.workspace_id = str(workspace_id).strip()
        self.organization_id = str(organization_id).strip()
        self.name = str(name).strip()
        self.description = str(description).strip()
        self.lead_id = str(lead_id).strip()
        self.member_ids = list(member_ids) if member_ids else []
        self.department = str(department).strip()
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def add_member(self, user_id: str):
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_member(self, user_id: str):
        if user_id in self.member_ids and user_id != self.lead_id:
            self.member_ids.remove(user_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def set_lead(self, user_id: str):
        self.lead_id = user_id
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "organization_id": self.organization_id,
            "name": self.name,
            "description": self.description,
            "lead_id": self.lead_id,
            "member_ids": self.member_ids,
            "department": self.department,
            "member_count": len(self.member_ids),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Team":
        return cls(
            id=data["id"],
            workspace_id=data["workspace_id"],
            organization_id=data.get("organization_id", ""),
            name=data["name"],
            description=data.get("description", ""),
            lead_id=data.get("lead_id", ""),
            member_ids=data.get("member_ids", []),
            department=data.get("department", "Engineering"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"<Team {self.id}: {self.name} ({len(self.member_ids)} members)>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Team):
            return False
        return self.id == other.id
