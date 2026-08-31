"""
TaskFlow Enterprise SaaS - Calendar Event Domain Model.
Represents scheduled project calendar events, meetings, deadlines, and milestone reviews with recurring schedule options.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List


class CalendarEvent:
    """CalendarEvent domain entity representing scheduled calendar items."""

    def __init__(
        self,
        id: str,
        workspace_id: str,
        title: str,
        start_time: str,
        end_time: str,
        description: str = "",
        location: str = "",
        project_id: Optional[str] = None,
        task_id: Optional[str] = None,
        creator_id: str = "",
        attendee_ids: Optional[List[str]] = None,
        is_all_day: bool = False,
        event_type: str = "MEETING",
        recurring_pattern: str = "NONE",
        color_code: str = "#6366f1",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = str(id).strip()
        self.workspace_id = str(workspace_id).strip()
        self.title = str(title).strip()
        self.start_time = start_time
        self.end_time = end_time
        self.description = str(description).strip()
        self.location = str(location).strip()
        self.project_id = project_id
        self.task_id = task_id
        self.creator_id = str(creator_id).strip()
        self.attendee_ids = list(attendee_ids) if attendee_ids else []
        self.is_all_day = bool(is_all_day)
        self.event_type = event_type.upper().strip()
        self.recurring_pattern = recurring_pattern.upper().strip()
        self.color_code = str(color_code).strip()
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def add_attendee(self, user_id: str):
        if user_id not in self.attendee_ids:
            self.attendee_ids.append(user_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_attendee(self, user_id: str):
        if user_id in self.attendee_ids:
            self.attendee_ids.remove(user_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description,
            "location": self.location,
            "project_id": self.project_id,
            "task_id": self.task_id,
            "creator_id": self.creator_id,
            "attendee_ids": self.attendee_ids,
            "is_all_day": self.is_all_day,
            "event_type": self.event_type,
            "recurring_pattern": self.recurring_pattern,
            "color_code": self.color_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalendarEvent":
        return cls(
            id=data["id"],
            workspace_id=data["workspace_id"],
            title=data["title"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            description=data.get("description", ""),
            location=data.get("location", ""),
            project_id=data.get("project_id"),
            task_id=data.get("task_id"),
            creator_id=data.get("creator_id", ""),
            attendee_ids=data.get("attendee_ids", []),
            is_all_day=data.get("is_all_day", False),
            event_type=data.get("event_type", "MEETING"),
            recurring_pattern=data.get("recurring_pattern", "NONE"),
            color_code=data.get("color_code", "#6366f1"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"<CalendarEvent {self.id}: {self.title} ({self.start_time})>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CalendarEvent):
            return False
        return self.id == other.id
