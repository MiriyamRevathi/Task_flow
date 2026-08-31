"""
TaskFlow Enterprise SaaS - Project Repository Data Access Layer.
Provides high-performance query methods for Project domain entities.
"""

from typing import Optional, List, Dict, Any, Set
from taskflow.models.project import Project
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine
from taskflow.models.enums import ProjectStatus, ProjectPriority, RiskLevel, HealthCategory


class ProjectRepository(BaseRepository[Project]):
    """Data access repository for Project entities."""

    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "projects", Project)

    def get_by_workspace(self, workspace_id: str, status: Optional[str] = None) -> List[Project]:
        if not workspace_id:
            return []
        projects = self.filter(lambda p: p.workspace_id == workspace_id)
        if status:
            projects = [p for p in projects if p.status == status]
        projects.sort(key=lambda p: p.updated_at or "", reverse=True)
        return projects

    def get_by_organization(self, org_id: str) -> List[Project]:
        if not org_id:
            return []
        return self.filter(lambda p: p.organization_id == org_id)

    def get_by_key(self, key: str) -> Optional[Project]:
        if not key:
            return None
        k_clean = key.upper().strip()
        return self.find_one(lambda p: p.key == k_clean)

    def get_by_owner(self, owner_id: str) -> List[Project]:
        return self.filter(lambda p: p.owner_id == owner_id and p.status != ProjectStatus.ARCHIVED.value)

    def get_by_team(self, team_id: str) -> List[Project]:
        return self.filter(lambda p: team_id in p.team_ids and p.status != ProjectStatus.ARCHIVED.value)

    def get_by_member(self, user_id: str) -> List[Project]:
        return self.filter(lambda p: user_id in p.member_ids and p.status != ProjectStatus.ARCHIVED.value)

    def get_active_projects(self, workspace_id: str) -> List[Project]:
        return self.filter(lambda p: p.workspace_id == workspace_id and p.status in (ProjectStatus.PLANNING.value, ProjectStatus.ACTIVE.value))

    def get_high_risk_projects(self, workspace_id: str) -> List[Project]:
        return self.filter(lambda p: p.workspace_id == workspace_id and p.risk_level == RiskLevel.HIGH_RISK.value)

    def get_overdue_projects(self, workspace_id: str) -> List[Project]:
        return [p for p in self.get_by_workspace(workspace_id) if p.is_overdue()]

    def search_projects(self, workspace_id: str, query_str: str) -> List[Project]:
        if not query_str:
            return self.get_by_workspace(workspace_id)
        q = query_str.lower().strip()
        return self.filter(
            lambda p: p.workspace_id == workspace_id
            and (q in p.name.lower() or q in p.key.lower() or q in p.description.lower() or any(q in t.lower() for t in p.tags))
        )

    def get_workspace_project_stats(self, workspace_id: str) -> Dict[str, Any]:
        projects = self.get_by_workspace(workspace_id)
        total = len(projects)
        planning = sum(1 for p in projects if p.status == ProjectStatus.PLANNING.value)
        active = sum(1 for p in projects if p.status == ProjectStatus.ACTIVE.value)
        on_hold = sum(1 for p in projects if p.status == ProjectStatus.ON_HOLD.value)
        completed = sum(1 for p in projects if p.status == ProjectStatus.COMPLETED.value)
        archived = sum(1 for p in projects if p.status == ProjectStatus.ARCHIVED.value)
        overdue = sum(1 for p in projects if p.is_overdue())

        total_budget = sum(p.budget for p in projects)
        total_spent = sum(p.spent_budget for p in projects)

        avg_progress = sum(p.progress_percentage for p in projects) / float(total) if total > 0 else 0.0

        return {
            "total_projects": total,
            "planning": planning,
            "active": active,
            "on_hold": on_hold,
            "completed": completed,
            "archived": archived,
            "overdue": overdue,
            "total_budget": round(total_budget, 2),
            "total_spent": round(total_spent, 2),
            "remaining_budget": round(max(0.0, total_budget - total_spent), 2),
            "average_progress": round(avg_progress, 1),
        }
