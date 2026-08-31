"""
System Settings Domain Model.
Configures global application settings, organization defaults, and security policies.
"""

from typing import Dict, Any, Optional


class SystemSettings:
    def __init__(
        self,
        id: str = "global",
        app_name: str = "TaskFlow Enterprise",
        maintenance_mode: bool = False,
        allow_registration: bool = True,
        default_user_role: str = "EMPLOYEE",
        max_upload_size_mb: int = 10,
        session_timeout_minutes: int = 1440,
        theme_default: str = "light",
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.app_name = app_name
        self.maintenance_mode = maintenance_mode
        self.allow_registration = allow_registration
        self.default_user_role = default_user_role
        self.max_upload_size_mb = max_upload_size_mb
        self.session_timeout_minutes = session_timeout_minutes
        self.theme_default = theme_default
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "app_name": self.app_name,
            "maintenance_mode": self.maintenance_mode,
            "allow_registration": self.allow_registration,
            "default_user_role": self.default_user_role,
            "max_upload_size_mb": self.max_upload_size_mb,
            "session_timeout_minutes": self.session_timeout_minutes,
            "theme_default": self.theme_default,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SystemSettings":
        return cls(
            id=data.get("id", "global"),
            app_name=data.get("app_name", "TaskFlow Enterprise"),
            maintenance_mode=data.get("maintenance_mode", False),
            allow_registration=data.get("allow_registration", True),
            default_user_role=data.get("default_user_role", "EMPLOYEE"),
            max_upload_size_mb=data.get("max_upload_size_mb", 10),
            session_timeout_minutes=data.get("session_timeout_minutes", 1440),
            theme_default=data.get("theme_default", "light"),
            updated_at=data.get("updated_at"),
        )
