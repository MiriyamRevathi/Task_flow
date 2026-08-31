"""
Milestone Domain Model.
Represents project phase delivery goals with completion percentages and target deadlines.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from taskflow.models.enums import MilestoneStatus


class Milestone:
    def __init__(
        self,
        id: str,
        project_id: str,
        workspace_id: str,
        title: str,
        description: str = "",
        status: str = MilestoneStatus.UPCOMING.value,
        start_date: Optional[str] = None,
        due_date: Optional[str] = None,
        completed_at: Optional[str] = None,
        completion_percentage: float = 0.0,
        task_ids: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.project_id = project_id
        self.workspace_id = workspace_id
        self.title = title.strip()
        self.description = description
        self.status = status if status in MilestoneStatus.choices() else MilestoneStatus.UPCOMING.value
        self.start_date = start_date
        self.due_date = due_date
        self.completed_at = completed_at
        self.completion_percentage = max(0.0, min(100.0, float(completion_percentage)))
        self.task_ids = task_ids or []
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def is_overdue(self) -> bool:
        if not self.due_date or self.status == MilestoneStatus.COMPLETED.value:
            return False
        try:
            due = datetime.fromisoformat(self.due_date.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) > due
        except Exception:
            return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "workspace_id": self.workspace_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "completed_at": self.completed_at,
            "completion_percentage": self.completion_percentage,
            "task_ids": self.task_ids,
            "is_overdue": self.is_overdue(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Milestone":
        return cls(
            id=data["id"],
            project_id=data["project_id"],
            workspace_id=data["workspace_id"],
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", MilestoneStatus.UPCOMING.value),
            start_date=data.get("start_date"),
            due_date=data.get("due_date"),
            completed_at=data.get("completed_at"),
            completion_percentage=data.get("completion_percentage", 0.0),
            task_ids=data.get("task_ids", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
