"""
TaskFlow Enterprise SaaS - Workspace Domain Model.
Represents an isolated collaborative environment containing projects, teams, milestones, and members.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Set


class Workspace:
    """Workspace domain entity representing team workspaces."""

    def __init__(
        self,
        id: str,
        organization_id: str,
        name: str,
        slug: str,
        description: str = "",
        owner_id: str = "",
        member_ids: Optional[List[str]] = None,
        is_archived: bool = False,
        color_theme: str = "#6366f1",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
    ):
        self.id = str(id).strip()
        self.organization_id = str(organization_id).strip()
        self.name = str(name).strip()
        self.slug = str(slug).lower().strip()
        self.description = str(description).strip()
        self.owner_id = str(owner_id).strip()
        self.member_ids = list(member_ids) if member_ids else []
        self.is_archived = bool(is_archived)
        self.color_theme = str(color_theme).strip()
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso
        self.settings = settings or {
            "default_project_visibility": "workspace",
            "allow_guest_access": False,
            "notify_on_new_project": True,
        }

    def add_member(self, user_id: str):
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_member(self, user_id: str):
        if user_id in self.member_ids and user_id != self.owner_id:
            self.member_ids.remove(user_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def archive(self):
        self.is_archived = True
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def restore(self):
        self.is_archived = False
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "owner_id": self.owner_id,
            "member_ids": self.member_ids,
            "is_archived": self.is_archived,
            "color_theme": self.color_theme,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workspace":
        return cls(
            id=data["id"],
            organization_id=data["organization_id"],
            name=data["name"],
            slug=data["slug"],
            description=data.get("description", ""),
            owner_id=data.get("owner_id", ""),
            member_ids=data.get("member_ids", []),
            is_archived=data.get("is_archived", False),
            color_theme=data.get("color_theme", "#6366f1"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            settings=data.get("settings"),
        )

    def __repr__(self) -> str:
        return f"<Workspace {self.id}: {self.name} ({self.slug})>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Workspace):
            return False
        return self.id == other.id
