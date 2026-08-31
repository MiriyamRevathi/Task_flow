"""
TaskFlow Enterprise SaaS - Milestone Domain Model.
Represents project target milestones, completion deadlines, progress tracking, and dependency goals.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from taskflow.models.enums import MilestoneStatus


class Milestone:
    """Milestone domain entity representing project milestone goals."""

    def __init__(
        self,
        id: str,
        project_id: str,
        workspace_id: str,
        title: str,
        description: str = "",
        due_date: Optional[str] = None,
        status: str = MilestoneStatus.UPCOMING.value,
        progress_percentage: float = 0.0,
        task_ids: Optional[List[str]] = None,
        owner_id: str = "",
        completed_at: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = str(id).strip()
        self.project_id = str(project_id).strip()
        self.workspace_id = str(workspace_id).strip()
        self.title = str(title).strip()
        self.description = str(description).strip()
        self.due_date = due_date
        self.status = status if status in MilestoneStatus.choices() else MilestoneStatus.UPCOMING.value
        self.progress_percentage = max(0.0, min(100.0, float(progress_percentage)))
        self.task_ids = list(task_ids) if task_ids else []
        self.owner_id = str(owner_id).strip()
        self.completed_at = completed_at
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    @property
    def is_completed(self) -> bool:
        return self.status == MilestoneStatus.COMPLETED.value

    def is_overdue(self) -> bool:
        if not self.due_date or self.is_completed:
            return False
        try:
            due = datetime.fromisoformat(self.due_date.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) > due
        except Exception:
            return False

    def update_progress(self, new_percentage: float):
        self.progress_percentage = max(0.0, min(100.0, float(new_percentage)))
        if self.progress_percentage >= 100.0 and self.status != MilestoneStatus.COMPLETED.value:
            self.status = MilestoneStatus.COMPLETED.value
            self.completed_at = datetime.now(timezone.utc).isoformat()
        elif self.progress_percentage < 100.0 and self.status == MilestoneStatus.COMPLETED.value:
            self.status = MilestoneStatus.IN_PROGRESS.value
            self.completed_at = None
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_task(self, task_id: str):
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_task(self, task_id: str):
        if task_id in self.task_ids:
            self.task_ids.remove(task_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "workspace_id": self.workspace_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "task_ids": self.task_ids,
            "owner_id": self.owner_id,
            "completed_at": self.completed_at,
            "is_overdue": self.is_overdue(),
            "is_completed": self.is_completed,
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
            due_date=data.get("due_date"),
            status=data.get("status", MilestoneStatus.UPCOMING.value),
            progress_percentage=data.get("progress_percentage", 0.0),
            task_ids=data.get("task_ids", []),
            owner_id=data.get("owner_id", ""),
            completed_at=data.get("completed_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"<Milestone {self.id}: {self.title} [{self.status}]>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Milestone):
            return False
        return self.id == other.id
