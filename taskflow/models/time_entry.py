"""
Time Entry Domain Model.
Represents logged work hours, live timer records, task associations, and billable status.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional


class TimeEntry:
    def __init__(
        self,
        id: str,
        user_id: str,
        task_id: str,
        project_id: str,
        workspace_id: str,
        description: str = "",
        hours: float = 0.0,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        is_running: bool = False,
        is_billable: bool = True,
        hourly_rate: float = 0.0,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.task_id = task_id
        self.project_id = project_id
        self.workspace_id = workspace_id
        self.description = description
        self.hours = round(max(0.0, float(hours)), 2)
        self.start_time = start_time
        self.end_time = end_time
        self.is_running = is_running
        self.is_billable = is_billable
        self.hourly_rate = float(hourly_rate)
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "project_id": self.project_id,
            "workspace_id": self.workspace_id,
            "description": self.description,
            "hours": self.hours,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_running": self.is_running,
            "is_billable": self.is_billable,
            "hourly_rate": self.hourly_rate,
            "total_cost": round(self.hours * self.hourly_rate, 2),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimeEntry":
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            task_id=data["task_id"],
            project_id=data["project_id"],
            workspace_id=data["workspace_id"],
            description=data.get("description", ""),
            hours=data.get("hours", 0.0),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            is_running=data.get("is_running", False),
            is_billable=data.get("is_billable", True),
            hourly_rate=data.get("hourly_rate", 0.0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
