"""
TaskFlow Enterprise SaaS - Organization Domain Model.
Represents a multi-tenant enterprise organization with plan quotas, branding settings, SSO config, and subscription metrics.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Set


class Organization:
    """Organization domain entity representing tenant accounts."""

    def __init__(
        self,
        id: str,
        name: str,
        slug: str,
        domain: str = "",
        owner_id: str = "",
        subscription_plan: str = "ENTERPRISE",
        max_workspaces: int = 50,
        max_users: int = 500,
        logo_url: str = "",
        billing_email: str = "",
        is_active: bool = True,
        sso_enabled: bool = False,
        sso_provider: str = "",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
    ):
        self.id = str(id).strip()
        self.name = str(name).strip()
        self.slug = str(slug).lower().strip()
        self.domain = str(domain).lower().strip()
        self.owner_id = str(owner_id).strip()
        self.subscription_plan = str(subscription_plan).upper().strip()
        self.max_workspaces = int(max_workspaces)
        self.max_users = int(max_users)
        self.logo_url = logo_url or f"https://ui-avatars.com/api/?name={self.name}&background=4f46e5&color=fff"
        self.billing_email = str(billing_email).lower().strip()
        self.is_active = bool(is_active)
        self.sso_enabled = bool(sso_enabled)
        self.sso_provider = str(sso_provider).strip()
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso
        self.settings = settings or {
            "enforce_2fa": False,
            "allowed_domains": [],
            "custom_theme": "indigo",
            "data_retention_days": 365,
        }

    def update_plan(self, new_plan: str, max_workspaces: int, max_users: int):
        self.subscription_plan = new_plan.upper().strip()
        self.max_workspaces = max_workspaces
        self.max_users = max_users
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def enable_sso(self, provider: str):
        self.sso_enabled = True
        self.sso_provider = provider.strip()
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def disable_sso(self):
        self.sso_enabled = False
        self.sso_provider = ""
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict() -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "domain": self.domain,
            "owner_id": self.owner_id,
            "subscription_plan": self.subscription_plan,
            "max_workspaces": self.max_workspaces,
            "max_users": self.max_users,
            "logo_url": self.logo_url,
            "billing_email": self.billing_email,
            "is_active": self.is_active,
            "sso_enabled": self.sso_enabled,
            "sso_provider": self.sso_provider,
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
            domain=data.get("domain", ""),
            owner_id=data.get("owner_id", ""),
            subscription_plan=data.get("subscription_plan", "ENTERPRISE"),
            max_workspaces=data.get("max_workspaces", 50),
            max_users=data.get("max_users", 500),
            logo_url=data.get("logo_url", ""),
            billing_email=data.get("billing_email", ""),
            is_active=data.get("is_active", True),
            sso_enabled=data.get("sso_enabled", False),
            sso_provider=data.get("sso_provider", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            settings=data.get("settings"),
        )

    def __repr__(self) -> str:
        return f"<Organization {self.id}: {self.name} ({self.subscription_plan})>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Organization):
            return False
        return self.id == other.id
