"""
Audit Log Service.
"""

from typing import List, Optional
from taskflow.repositories.activity_repository import ActivityRepository
from taskflow.models.activity import Activity
from taskflow.utils.id_generator import generate_id


class AuditService:
    def __init__(self, activity_repo: ActivityRepository):
        self.activity_repo = activity_repo

    def log_activity(
        self,
        actor_id: str,
        actor_name: str,
        action: str,
        target_type: str,
        target_id: str,
        target_name: str,
        workspace_id: str,
        description: str = "",
        project_id: Optional[str] = None,
    ):
        act = Activity(
            id=generate_id("act"),
            actor_id=actor_id,
            actor_name=actor_name,
            action=action,
            target_type=target_type,
            target_id=target_id,
            target_name=target_name,
            description=description,
            workspace_id=workspace_id,
            project_id=project_id,
        )
        self.activity_repo.save(act)
        return act

    def get_workspace_activities(self, workspace_id: str, limit: int = 50) -> List[Activity]:
        return self.activity_repo.get_by_workspace(workspace_id, limit)
