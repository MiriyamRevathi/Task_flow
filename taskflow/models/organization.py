"""
Organization Domain Model.
Represents an enterprise tenant containing workspaces, teams, users, and organization settings.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class Organization:
    def __init__(
        self,
        id: str,
        name: str,
        slug: str,
        owner_id: str,
        domain: str = "",
        logo_url: str = "",
        description: str = "",
        plan_tier: str = "ENTERPRISE",
        max_workspaces: int = 20,
        max_members: int = 500,
        is_active: bool = True,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
    ):
        self.id = id
        self.name = name.strip()
        self.slug = slug.lower().strip()
        self.owner_id = owner_id
        self.domain = domain.lower().strip()
        self.logo_url = logo_url
        self.description = description
        self.plan_tier = plan_tier
        self.max_workspaces = max_workspaces
        self.max_members = max_members
        self.is_active = is_active
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso
        self.settings = settings or {
            "enforce_sso": False,
            "allow_public_projects": False,
            "default_timezone": "UTC",
            "time_tracking_enabled": True,
            "ml_insights_enabled": True
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "owner_id": self.owner_id,
            "domain": self.domain,
            "logo_url": self.logo_url,
            "description": self.description,
            "plan_tier": self.plan_tier,
            "max_workspaces": self.max_workspaces,
            "max_members": self.max_members,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Organization":
        return cls(
            id=data["id"],
            name=data["name"],
            slug=data["slug"],
            owner_id=data["owner_id"],
            domain=data.get("domain", ""),
            logo_url=data.get("logo_url", ""),
            description=data.get("description", ""),
            plan_tier=data.get("plan_tier", "ENTERPRISE"),
            max_workspaces=data.get("max_workspaces", 20),
            max_members=data.get("max_members", 500),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            settings=data.get("settings"),
        )
