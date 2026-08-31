"""
User Domain Model.
Represents an authenticated user in the TaskFlow system with role-based access control,
organization assignment, profile attributes, and security metrics.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from taskflow.models.enums import UserRole


class User:
    """User entity representing platform accounts."""

    def __init__(
        self,
        id: str,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        role: str = UserRole.EMPLOYEE.value,
        organization_id: Optional[str] = None,
        workspace_ids: Optional[List[str]] = None,
        department: str = "General",
        job_title: str = "Team Member",
        avatar_url: str = "",
        phone: str = "",
        bio: str = "",
        is_active: bool = True,
        is_email_verified: bool = True,
        failed_login_attempts: int = 0,
        last_login_at: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
    ):
        self.id = id
        self.email = email.lower().strip()
        self.password_hash = password_hash
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.role = role if role in UserRole.choices() else UserRole.EMPLOYEE.value
        self.organization_id = organization_id
        self.workspace_ids = workspace_ids or []
        self.department = department
        self.job_title = job_title
        self.avatar_url = avatar_url or f"https://ui-avatars.com/api/?name={first_name}+{last_name}&background=6366f1&color=fff"
        self.phone = phone
        self.bio = bio
        self.is_active = is_active
        self.is_email_verified = is_email_verified
        self.failed_login_attempts = failed_login_attempts
        self.last_login_at = last_login_at
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso
        self.settings = settings or {
            "email_notifications": True,
            "theme": "light",
            "timezone": "UTC",
            "compact_view": False
        }

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def role_enum(self) -> UserRole:
        return UserRole(self.role)

    def is_super_admin(self) -> bool:
        return self.role == UserRole.SUPER_ADMIN.value

    def is_org_admin(self) -> bool:
        return self.role in (UserRole.SUPER_ADMIN.value, UserRole.ORG_ADMIN.value)

    def is_manager_or_above(self) -> bool:
        return self.role in (UserRole.SUPER_ADMIN.value, UserRole.ORG_ADMIN.value, UserRole.PROJECT_MANAGER.value)

    def is_lead_or_above(self) -> bool:
        return self.role in (
            UserRole.SUPER_ADMIN.value,
            UserRole.ORG_ADMIN.value,
            UserRole.PROJECT_MANAGER.value,
            UserRole.TEAM_LEAD.value,
        )

    def can_access_workspace(self, workspace_id: str) -> bool:
        if self.is_super_admin() or self.is_org_admin():
            return True
        return workspace_id in self.workspace_ids

    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "role": self.role,
            "role_display": UserRole(self.role).display_name,
            "organization_id": self.organization_id,
            "workspace_ids": self.workspace_ids,
            "department": self.department,
            "job_title": self.job_title,
            "avatar_url": self.avatar_url,
            "phone": self.phone,
            "bio": self.bio,
            "is_active": self.is_active,
            "is_email_verified": self.is_email_verified,
            "failed_login_attempts": self.failed_login_attempts,
            "last_login_at": self.last_login_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "settings": self.settings,
        }
        if include_sensitive:
            data["password_hash"] = self.password_hash
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(
            id=data["id"],
            email=data["email"],
            password_hash=data.get("password_hash", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            role=data.get("role", UserRole.EMPLOYEE.value),
            organization_id=data.get("organization_id"),
            workspace_ids=data.get("workspace_ids", []),
            department=data.get("department", "General"),
            job_title=data.get("job_title", "Team Member"),
            avatar_url=data.get("avatar_url", ""),
            phone=data.get("phone", ""),
            bio=data.get("bio", ""),
            is_active=data.get("is_active", True),
            is_email_verified=data.get("is_email_verified", True),
            failed_login_attempts=data.get("failed_login_attempts", 0),
            last_login_at=data.get("last_login_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            settings=data.get("settings"),
        )
