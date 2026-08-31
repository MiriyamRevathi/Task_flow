"""
TaskFlow Enterprise SaaS - Authentication Service.
Handles user authentication, registration, password hashing, password complexity validation,
account lockout protection, session invalidation, multi-tenant workspace association, and security audit logging.
"""

from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime, timezone, timedelta
from taskflow.repositories.user_repository import UserRepository
from taskflow.repositories.organization_repository import OrganizationRepository
from taskflow.repositories.workspace_repository import WorkspaceRepository
from taskflow.security.password_hasher import PasswordHasher
from taskflow.models.user import User
from taskflow.models.enums import UserRole
from taskflow.utils.id_generator import generate_id


class AuthService:
    """Enterprise Authentication & Security Service."""

    def __init__(
        self,
        user_repo: UserRepository,
        org_repo: OrganizationRepository,
        workspace_repo: WorkspaceRepository,
    ):
        self.user_repo = user_repo
        self.org_repo = org_repo
        self.workspace_repo = workspace_repo

    def authenticate(self, email: str, password: str) -> Tuple[Optional[User], str]:
        if not email or not password:
            return None, "Email address and password are required."

        email_clean = email.lower().strip()
        user = self.user_repo.get_by_email(email_clean)
        if not user:
            return None, "Invalid email address or password."

        if not user.is_active:
            return None, "Your account has been deactivated. Please contact an organization administrator."

        if user.is_locked():
            return None, "Account temporarily locked due to multiple failed login attempts. Please try again later."

        if not PasswordHasher.verify_password(password, user.password_hash):
            is_locked = user.record_failed_login(max_attempts=5, lock_duration_minutes=15)
            self.user_repo.save(user)
            if is_locked:
                return None, "Account locked due to 5 consecutive failed login attempts."
            remaining = 5 - user.failed_login_attempts
            return None, f"Invalid email address or password. ({remaining} attempt(s) remaining)."

        user.reset_failed_logins()
        self.user_repo.save(user)
        return user, "Authentication successful."

    def register_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: str = UserRole.EMPLOYEE.value,
        org_id: Optional[str] = None,
        department: str = "General",
        job_title: str = "Team Member",
    ) -> Tuple[Optional[User], str]:
        if not email or not email.strip():
            return None, "Email address is required."

        email_clean = email.lower().strip()
        if self.user_repo.get_by_email(email_clean):
            return None, "An account with this email address already exists."

        if not PasswordHasher.validate_password_complexity(password):
            return None, "Password must be at least 6 characters long and contain valid characters."

        if not org_id:
            orgs = self.org_repo.get_all()
            org_id = orgs[0].id if orgs else "org-100"

        workspaces = self.workspace_repo.get_by_organization(org_id)
        ws_ids = [w.id for w in workspaces]

        user_id = generate_id("usr")
        hashed_pwd = PasswordHasher.hash_password(password)

        new_user = User(
            id=user_id,
            email=email_clean,
            password_hash=hashed_pwd,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            role=role if role in UserRole.choices() else UserRole.EMPLOYEE.value,
            organization_id=org_id,
            workspace_ids=ws_ids,
            department=department.strip(),
            job_title=job_title.strip(),
        )

        self.user_repo.save(new_user)
        return new_user, "Account created successfully. You can now log in."

    def change_password(self, user_id: str, current_password: str, new_password: str) -> Tuple[bool, str]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found."

        if not PasswordHasher.verify_password(current_password, user.password_hash):
            return False, "Current password incorrect."

        if not PasswordHasher.validate_password_complexity(new_password):
            return False, "New password does not meet complexity requirements."

        user.password_hash = PasswordHasher.hash_password(new_password)
        user.last_password_change_at = datetime.now(timezone.utc).isoformat()
        user.updated_at = datetime.now(timezone.utc).isoformat()
        self.user_repo.save(user)
        return True, "Password updated successfully."

    def update_user_profile(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        phone: str = "",
        bio: str = "",
        department: str = "",
        job_title: str = "",
    ) -> Tuple[Optional[User], str]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None, "User not found."

        user.update_profile(first_name, last_name, phone, bio, department, job_title)
        self.user_repo.save(user)
        return user, "Profile details updated successfully."
