"""
TaskFlow Enterprise SaaS - Time Entry Domain Model.
Represents logged work duration, live timer sessions, billable hours, hourly rates, and timesheet approvals.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional


class TimeEntry:
    """TimeEntry domain entity representing logged work hours."""

    def __init__(
        self,
        id: str,
        task_id: str,
        project_id: str,
        workspace_id: str,
        user_id: str,
        hours: float,
        description: str = "",
        date_logged: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        is_billable: bool = True,
        hourly_rate: float = 0.0,
        is_approved: bool = False,
        approved_by: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = str(id).strip()
        self.task_id = str(task_id).strip()
        self.project_id = str(project_id).strip()
        self.workspace_id = str(workspace_id).strip()
        self.user_id = str(user_id).strip()
        self.hours = round(max(0.0, float(hours)), 2)
        self.description = str(description).strip()
        now_iso = datetime.now(timezone.utc).isoformat()
        self.date_logged = date_logged or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.start_time = start_time
        self.end_time = end_time
        self.is_billable = bool(is_billable)
        self.hourly_rate = max(0.0, float(hourly_rate))
        self.is_approved = bool(is_approved)
        self.approved_by = approved_by
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    @property
    def total_cost(self) -> float:
        if not self.is_billable:
            return 0.0
        return round(self.hours * self.hourly_rate, 2)

    def approve(self, approver_user_id: str):
        self.is_approved = True
        self.approved_by = approver_user_id
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "project_id": self.project_id,
            "workspace_id": self.workspace_id,
            "user_id": self.user_id,
            "hours": self.hours,
            "description": self.description,
            "date_logged": self.date_logged,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_billable": self.is_billable,
            "hourly_rate": self.hourly_rate,
            "total_cost": self.total_cost,
            "is_approved": self.is_approved,
            "approved_by": self.approved_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimeEntry":
        return cls(
            id=data["id"],
            task_id=data["task_id"],
            project_id=data["project_id"],
            workspace_id=data["workspace_id"],
            user_id=data["user_id"],
            hours=data.get("hours", 0.0),
            description=data.get("description", ""),
            date_logged=data.get("date_logged"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            is_billable=data.get("is_billable", True),
            hourly_rate=data.get("hourly_rate", 0.0),
            is_approved=data.get("is_approved", False),
            approved_by=data.get("approved_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"<TimeEntry {self.id}: {self.hours} hrs by {self.user_id}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TimeEntry):
            return False
        return self.id == other.id
