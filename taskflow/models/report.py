"""
Report Domain Model.
Represents generated executive, project, team, and time tracking reports with export parameters.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional


class Report:
    def __init__(
        self,
        id: str,
        title: str,
        report_type: str,  # EXECUTIVE, PROJECT, TEAM, TIME, RISK, PRODUCTIVITY
        creator_id: str,
        workspace_id: str,
        parameters: Optional[Dict[str, Any]] = None,
        summary: Optional[Dict[str, Any]] = None,
        file_path: str = "",
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.title = title.strip()
        self.report_type = report_type
        self.creator_id = creator_id
        self.workspace_id = workspace_id
        self.parameters = parameters or {}
        self.summary = summary or {}
        self.file_path = file_path
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "report_type": self.report_type,
            "creator_id": self.creator_id,
            "workspace_id": self.workspace_id,
            "parameters": self.parameters,
            "summary": self.summary,
            "file_path": self.file_path,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Report":
        return cls(
            id=data["id"],
            title=data["title"],
            report_type=data.get("report_type", "EXECUTIVE"),
            creator_id=data.get("creator_id", ""),
            workspace_id=data.get("workspace_id", ""),
            parameters=data.get("parameters", {}),
            summary=data.get("summary", {}),
            file_path=data.get("file_path", ""),
            created_at=data.get("created_at"),
        )
