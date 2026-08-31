"""
Authentication Service.
Handles user registration, authentication validation, profile updates, and password changes.
"""

from typing import Optional, Dict, Any, Tuple
from taskflow.repositories.user_repository import UserRepository
from taskflow.repositories.organization_repository import OrganizationRepository
from taskflow.repositories.workspace_repository import WorkspaceRepository
from taskflow.security.password_hasher import PasswordHasher
from taskflow.models.user import User
from taskflow.utils.id_generator import generate_id


class AuthService:
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
        user = self.user_repo.get_by_email(email)
        if not user:
            return None, "Invalid email or password."

        if not user.is_active:
            return None, "Your account has been deactivated. Please contact an administrator."

        if not PasswordHasher.verify_password(password, user.password_hash):
            user.failed_login_attempts += 1
            self.user_repo.save(user)
            return None, "Invalid email or password."

        user.failed_login_attempts = 0
        self.user_repo.save(user)
        return user, "Authentication successful."

    def register_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: str = "EMPLOYEE",
        org_id: Optional[str] = None,
    ) -> Tuple[Optional[User], str]:
        if self.user_repo.get_by_email(email):
            return None, "An account with this email address already exists."

        if not PasswordHasher.validate_password_complexity(password):
            return None, "Password must be at least 6 characters long."

        if not org_id:
            orgs = self.org_repo.get_all()
            org_id = orgs[0].id if orgs else "org-100"

        workspaces = self.workspace_repo.get_by_organization(org_id)
        ws_ids = [w.id for w in workspaces]

        user_id = generate_id("usr")
        hashed_pwd = PasswordHasher.hash_password(password)

        new_user = User(
            id=user_id,
            email=email,
            password_hash=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            role=role,
            organization_id=org_id,
            workspace_ids=ws_ids,
        )
        self.user_repo.save(new_user)
        return new_user, "Account created successfully."
