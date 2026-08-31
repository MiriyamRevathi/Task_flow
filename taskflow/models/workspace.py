"""
Workspace Domain Model.
Represents an isolated environment inside an organization where projects, tasks, and teams are managed.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class Workspace:
    def __init__(
        self,
        id: str,
        organization_id: str,
        name: str,
        slug: str,
        description: str = "",
        owner_id: str = "",
        member_ids: Optional[List[str]] = None,
        is_default: bool = False,
        is_archived: bool = False,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        color_theme: str = "#6366f1",
    ):
        self.id = id
        self.organization_id = organization_id
        self.name = name.strip()
        self.slug = slug.lower().strip()
        self.description = description
        self.owner_id = owner_id
        self.member_ids = member_ids or []
        self.is_default = is_default
        self.is_archived = is_archived
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso
        self.color_theme = color_theme

    def add_member(self, user_id: str):
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)

    def remove_member(self, user_id: str):
        if user_id in self.member_ids:
            self.member_ids.remove(user_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "owner_id": self.owner_id,
            "member_ids": self.member_ids,
            "is_default": self.is_default,
            "is_archived": self.is_archived,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "color_theme": self.color_theme,
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
            is_default=data.get("is_default", False),
            is_archived=data.get("is_archived", False),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            color_theme=data.get("color_theme", "#6366f1"),
        )
