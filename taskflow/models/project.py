"""
Project Domain Model.
Represents a project with lifecycle stages, deadlines, budget simulation, priorities, progress, and team assignments.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from taskflow.models.enums import ProjectStatus, ProjectPriority, RiskLevel, HealthCategory


class Project:
    def __init__(
        self,
        id: str,
        workspace_id: str,
        organization_id: str,
        name: str,
        key: str,
        description: str = "",
        owner_id: str = "",
        team_ids: Optional[List[str]] = None,
        member_ids: Optional[List[str]] = None,
        status: str = ProjectStatus.PLANNING.value,
        priority: str = ProjectPriority.MEDIUM.value,
        start_date: Optional[str] = None,
        due_date: Optional[str] = None,
        completed_at: Optional[str] = None,
        progress_percentage: float = 0.0,
        budget: float = 0.0,
        spent_budget: float = 0.0,
        tags: Optional[List[str]] = None,
        risk_level: str = RiskLevel.LOW_RISK.value,
        risk_score: float = 0.0,
        health_score: float = 100.0,
        health_category: str = HealthCategory.HEALTHY.value,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.workspace_id = workspace_id
        self.organization_id = organization_id
        self.name = name.strip()
        self.key = key.upper().strip()
        self.description = description
        self.owner_id = owner_id
        self.team_ids = team_ids or []
        self.member_ids = member_ids or []
        self.status = status if status in ProjectStatus.choices() else ProjectStatus.PLANNING.value
        self.priority = priority if priority in ProjectPriority.choices() else ProjectPriority.MEDIUM.value
        self.start_date = start_date
        self.due_date = due_date
        self.completed_at = completed_at
        self.progress_percentage = max(0.0, min(100.0, float(progress_percentage)))
        self.budget = float(budget)
        self.spent_budget = float(spent_budget)
        self.tags = tags or []
        self.risk_level = risk_level if risk_level in RiskLevel.choices() else RiskLevel.LOW_RISK.value
        self.risk_score = float(risk_score)
        self.health_score = max(0.0, min(100.0, float(health_score)))
        self.health_category = health_category
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def is_overdue(self) -> bool:
        if not self.due_date or self.status in (ProjectStatus.COMPLETED.value, ProjectStatus.ARCHIVED.value):
            return False
        try:
            due = datetime.fromisoformat(self.due_date.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) > due
        except Exception:
            return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "organization_id": self.organization_id,
            "name": self.name,
            "key": self.key,
            "description": self.description,
            "owner_id": self.owner_id,
            "team_ids": self.team_ids,
            "member_ids": self.member_ids,
            "status": self.status,
            "priority": self.priority,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "completed_at": self.completed_at,
            "progress_percentage": self.progress_percentage,
            "budget": self.budget,
            "spent_budget": self.spent_budget,
            "tags": self.tags,
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "health_score": self.health_score,
            "health_category": self.health_category,
            "is_overdue": self.is_overdue(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        return cls(
            id=data["id"],
            workspace_id=data["workspace_id"],
            organization_id=data.get("organization_id", ""),
            name=data["name"],
            key=data["key"],
            description=data.get("description", ""),
            owner_id=data.get("owner_id", ""),
            team_ids=data.get("team_ids", []),
            member_ids=data.get("member_ids", []),
            status=data.get("status", ProjectStatus.PLANNING.value),
            priority=data.get("priority", ProjectPriority.MEDIUM.value),
            start_date=data.get("start_date"),
            due_date=data.get("due_date"),
            completed_at=data.get("completed_at"),
            progress_percentage=data.get("progress_percentage", 0.0),
            budget=data.get("budget", 0.0),
            spent_budget=data.get("spent_budget", 0.0),
            tags=data.get("tags", []),
            risk_level=data.get("risk_level", RiskLevel.LOW_RISK.value),
            risk_score=data.get("risk_score", 0.0),
            health_score=data.get("health_score", 100.0),
            health_category=data.get("health_category", HealthCategory.HEALTHY.value),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
