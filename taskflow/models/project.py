"""
TaskFlow Enterprise SaaS - Project Domain Model.
Represents a project with lifecycle stages, deadlines, budget simulation, priorities, progress, and team assignments.
Includes full business state machine validations, status calculations, risk evaluations, and serialization helpers.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Set
from taskflow.models.enums import ProjectStatus, ProjectPriority, RiskLevel, HealthCategory


class Project:
    """Project domain entity representing enterprise projects."""

    VALID_TRANSITIONS = {
        ProjectStatus.PLANNING.value: [ProjectStatus.ACTIVE.value, ProjectStatus.ON_HOLD.value, ProjectStatus.ARCHIVED.value],
        ProjectStatus.ACTIVE.value: [ProjectStatus.ON_HOLD.value, ProjectStatus.COMPLETED.value, ProjectStatus.ARCHIVED.value],
        ProjectStatus.ON_HOLD.value: [ProjectStatus.ACTIVE.value, ProjectStatus.ARCHIVED.value],
        ProjectStatus.COMPLETED.value: [ProjectStatus.ACTIVE.value, ProjectStatus.ARCHIVED.value],
        ProjectStatus.ARCHIVED.value: [ProjectStatus.PLANNING.value, ProjectStatus.ACTIVE.value],
    }

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
        settings: Optional[Dict[str, Any]] = None,
    ):
        self.id = str(id).strip()
        self.workspace_id = str(workspace_id).strip()
        self.organization_id = str(organization_id).strip()
        self.name = str(name).strip()
        self.key = str(key).upper().strip()
        self.description = str(description).strip()
        self.owner_id = str(owner_id).strip()
        self.team_ids = list(team_ids) if team_ids else []
        self.member_ids = list(member_ids) if member_ids else []
        self.status = status if status in ProjectStatus.choices() else ProjectStatus.PLANNING.value
        self.priority = priority if priority in ProjectPriority.choices() else ProjectPriority.MEDIUM.value
        self.start_date = start_date
        self.due_date = due_date
        self.completed_at = completed_at
        self.progress_percentage = max(0.0, min(100.0, float(progress_percentage)))
        self.budget = max(0.0, float(budget))
        self.spent_budget = max(0.0, float(spent_budget))
        self.tags = list(tags) if tags else []
        self.risk_level = risk_level if risk_level in RiskLevel.choices() else RiskLevel.LOW_RISK.value
        self.risk_score = max(0.0, min(100.0, float(risk_score)))
        self.health_score = max(0.0, min(100.0, float(health_score)))
        self.health_category = health_category if health_category in HealthCategory.choices() else HealthCategory.HEALTHY.value
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso
        self.settings = settings or {
            "allow_member_invites": True,
            "notify_on_status_change": True,
            "auto_calculate_progress": True,
            "require_code_review": True,
        }

    @property
    def status_enum(self) -> ProjectStatus:
        return ProjectStatus(self.status)

    @property
    def priority_enum(self) -> ProjectPriority:
        return ProjectPriority(self.priority)

    @property
    def risk_level_enum(self) -> RiskLevel:
        return RiskLevel(self.risk_level)

    @property
    def remaining_budget(self) -> float:
        return round(max(0.0, self.budget - self.spent_budget), 2)

    @property
    def budget_utilization_percentage(self) -> float:
        if self.budget <= 0:
            return 0.0
        return round(min(100.0, (self.spent_budget / self.budget) * 100.0), 1)

    def can_transition_to(self, target_status: str) -> bool:
        if target_status not in ProjectStatus.choices():
            return False
        allowed = self.VALID_TRANSITIONS.get(self.status, [])
        return target_status in allowed or target_status == self.status

    def transition_to(self, target_status: str) -> bool:
        if not self.can_transition_to(target_status):
            return False
        self.status = target_status
        if target_status == ProjectStatus.COMPLETED.value:
            self.completed_at = datetime.now(timezone.utc).isoformat()
            self.progress_percentage = 100.0
        elif target_status == ProjectStatus.ACTIVE.value and self.completed_at:
            self.completed_at = None
        self.updated_at = datetime.now(timezone.utc).isoformat()
        return True

    def is_overdue(self) -> bool:
        if not self.due_date or self.status in (ProjectStatus.COMPLETED.value, ProjectStatus.ARCHIVED.value):
            return False
        try:
            due = datetime.fromisoformat(self.due_date.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) > due
        except Exception:
            return False

    def days_until_due(self) -> int:
        if not self.due_date:
            return 0
        try:
            due = datetime.fromisoformat(self.due_date.replace("Z", "+00:00"))
            delta = due - datetime.now(timezone.utc)
            return delta.days
        except Exception:
            return 0

    def add_team(self, team_id: str):
        if team_id not in self.team_ids:
            self.team_ids.append(team_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_team(self, team_id: str):
        if team_id in self.team_ids:
            self.team_ids.remove(team_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_member(self, user_id: str):
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_member(self, user_id: str):
        if user_id in self.member_ids:
            self.member_ids.remove(user_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_tag(self, tag: str):
        clean_tag = tag.strip().lower()
        if clean_tag and clean_tag not in self.tags:
            self.tags.append(clean_tag)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_tag(self, tag: str):
        clean_tag = tag.strip().lower()
        if clean_tag in self.tags:
            self.tags.remove(clean_tag)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def update_budget_spend(self, amount: float):
        self.spent_budget = round(max(0.0, self.spent_budget + float(amount)), 2)
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def update_health(self, score: float, category: str, risk_level: str, risk_score: float):
        self.health_score = max(0.0, min(100.0, float(score)))
        self.health_category = category if category in HealthCategory.choices() else HealthCategory.HEALTHY.value
        self.risk_level = risk_level if risk_level in RiskLevel.choices() else RiskLevel.LOW_RISK.value
        self.risk_score = max(0.0, min(100.0, float(risk_score)))
        self.updated_at = datetime.now(timezone.utc).isoformat()

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
            "remaining_budget": self.remaining_budget,
            "budget_utilization": self.budget_utilization_percentage,
            "tags": self.tags,
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "health_score": self.health_score,
            "health_category": self.health_category,
            "is_overdue": self.is_overdue(),
            "days_until_due": self.days_until_due(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "settings": self.settings,
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
            settings=data.get("settings"),
        )

    def __repr__(self) -> str:
        return f"<Project {self.key}: {self.name} ({self.status})>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Project):
            return False
        return self.id == other.id
