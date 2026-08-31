"""
Calendar Event Domain Model.
Represents scheduled events, meetings, task deadlines, and milestone dates on the project calendar.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class CalendarEvent:
    def __init__(
        self,
        id: str,
        workspace_id: str,
        title: str,
        description: str = "",
        event_type: str = "DEADLINE",  # DEADLINE, MILESTONE, MEETING, EVENT
        start_time: str = "",
        end_time: str = "",
        all_day: bool = True,
        project_id: Optional[str] = None,
        task_id: Optional[str] = None,
        milestone_id: Optional[str] = None,
        creator_id: str = "",
        participant_ids: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.workspace_id = workspace_id
        self.title = title.strip()
        self.description = description
        self.event_type = event_type
        self.start_time = start_time
        self.end_time = end_time or start_time
        self.all_day = all_day
        self.project_id = project_id
        self.task_id = task_id
        self.milestone_id = milestone_id
        self.creator_id = creator_id
        self.participant_ids = participant_ids or []
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "title": self.title,
            "description": self.description,
            "event_type": self.event_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "all_day": self.all_day,
            "project_id": self.project_id,
            "task_id": self.task_id,
            "milestone_id": self.milestone_id,
            "creator_id": self.creator_id,
            "participant_ids": self.participant_ids,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalendarEvent":
        return cls(
            id=data["id"],
            workspace_id=data["workspace_id"],
            title=data["title"],
            description=data.get("description", ""),
            event_type=data.get("event_type", "DEADLINE"),
            start_time=data.get("start_time", ""),
            end_time=data.get("end_time", ""),
            all_day=data.get("all_day", True),
            project_id=data.get("project_id"),
            task_id=data.get("task_id"),
            milestone_id=data.get("milestone_id"),
            creator_id=data.get("creator_id", ""),
            participant_ids=data.get("participant_ids", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
