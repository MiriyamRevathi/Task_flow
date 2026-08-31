"""
TaskFlow Enterprise SaaS - User Domain Model.
Represents an authenticated user in the TaskFlow system with role-based access control,
organization assignment, profile attributes, security metrics, and permission check helpers.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Set
import re
from taskflow.models.enums import UserRole


class User:
    """User domain entity representing authenticated enterprise accounts."""

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

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
        last_password_change_at: Optional[str] = None,
        locked_until: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        permissions: Optional[List[str]] = None,
    ):
        self.id = str(id).strip()
        self.email = str(email).lower().strip()
        self.password_hash = str(password_hash)
        self.first_name = str(first_name).strip()
        self.last_name = str(last_name).strip()
        self.role = role if role in UserRole.choices() else UserRole.EMPLOYEE.value
        self.organization_id = organization_id
        self.workspace_ids = list(workspace_ids) if workspace_ids else []
        self.department = str(department).strip()
        self.job_title = str(job_title).strip()
        self.avatar_url = avatar_url or f"https://ui-avatars.com/api/?name={self.first_name}+{self.last_name}&background=6366f1&color=fff"
        self.phone = str(phone).strip()
        self.bio = str(bio).strip()
        self.is_active = bool(is_active)
        self.is_email_verified = bool(is_email_verified)
        self.failed_login_attempts = int(failed_login_attempts)
        self.last_login_at = last_login_at
        self.last_password_change_at = last_password_change_at
        self.locked_until = locked_until
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso
        self.settings = settings or {
            "email_notifications": True,
            "theme": "light",
            "timezone": "UTC",
            "compact_view": False,
            "desktop_notifications": True,
            "weekly_summary": True,
        }
        self.permissions = list(permissions) if permissions else []

    @property
    def full_name(self) -> str:
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.email

    @property
    def role_enum(self) -> UserRole:
        return UserRole(self.role)

    @property
    def role_display(self) -> str:
        return self.role_enum.display_name

    def validate_email(self) -> bool:
        if not self.email:
            return False
        return bool(self.EMAIL_REGEX.match(self.email))

    def is_locked(self) -> bool:
        if not self.locked_until:
            return False
        try:
            lock_time = datetime.fromisoformat(self.locked_until.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) < lock_time
        except Exception:
            return False

    def record_failed_login(self, max_attempts: int = 5, lock_duration_minutes: int = 15) -> bool:
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            lock_until_dt = datetime.now(timezone.utc) + timedelta(minutes=lock_duration_minutes)
            self.locked_until = lock_until_dt.isoformat()
            return True
        return False

    def reset_failed_logins(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login_at = datetime.now(timezone.utc).isoformat()

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
        if not self.is_active or self.is_locked():
            return False
        if self.is_super_admin() or self.is_org_admin():
            return True
        return workspace_id in self.workspace_ids

    def has_permission(self, permission_name: str) -> bool:
        if self.is_super_admin():
            return True
        return permission_name in self.permissions

    def add_workspace(self, workspace_id: str):
        if workspace_id not in self.workspace_ids:
            self.workspace_ids.append(workspace_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_workspace(self, workspace_id: str):
        if workspace_id in self.workspace_ids:
            self.workspace_ids.remove(workspace_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def update_profile(self, first_name: str, last_name: str, phone: str = "", bio: str = "", department: str = "", job_title: str = ""):
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        if phone:
            self.phone = phone.strip()
        if bio:
            self.bio = bio.strip()
        if department:
            self.department = department.strip()
        if job_title:
            self.job_title = job_title.strip()
        self.avatar_url = f"https://ui-avatars.com/api/?name={self.first_name}+{self.last_name}&background=6366f1&color=fff"
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self, include_sensitive: bool = True) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "role": self.role,
            "role_display": self.role_display,
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
            "last_password_change_at": self.last_password_change_at,
            "locked_until": self.locked_until,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "settings": self.settings,
            "permissions": self.permissions,
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
            last_password_change_at=data.get("last_password_change_at"),
            locked_until=data.get("locked_until"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            settings=data.get("settings"),
            permissions=data.get("permissions"),
        )
