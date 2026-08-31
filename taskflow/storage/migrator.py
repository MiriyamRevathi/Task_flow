"""
Storage Schema Migrator.
Manages schema version upgrades, data integrity checks, foreign key constraint validation, and dataset cleanup.
"""

from typing import Dict, Any, List
from taskflow.storage.file_storage import FileStorageEngine


class StorageMigrator:
    """Handles dataset schema updates and referential integrity verification."""

    CURRENT_VERSION = "2.0.0"

    def __init__(self, storage_engine: FileStorageEngine):
        self.engine = storage_engine

    def check_and_migrate(self):
        settings_data = self.engine.read_all("settings")
        if not settings_data:
            return

        current = settings_data[0].get("schema_version", "1.0.0")
        if current != self.CURRENT_VERSION:
            print(f"Migrating storage schema from {current} to {self.CURRENT_VERSION}...")
            self.run_integrity_check()
            settings_data[0]["schema_version"] = self.CURRENT_VERSION
            self.engine.write_all("settings", settings_data)

    def run_integrity_check(self) -> Dict[str, Any]:
        """Validate foreign keys and relationship integrity across entities."""
        users = {u["id"] for u in self.engine.read_all("users")}
        workspaces = {w["id"] for w in self.engine.read_all("workspaces")}
        projects = {p["id"] for p in self.engine.read_all("projects")}

        orphaned_tasks = 0
        tasks = self.engine.read_all("tasks")
        for task in tasks:
            if task.get("project_id") not in projects or task.get("workspace_id") not in workspaces:
                orphaned_tasks += 1

        return {
            "valid": orphaned_tasks == 0,
            "user_count": len(users),
            "workspace_count": len(workspaces),
            "project_count": len(projects),
            "task_count": len(tasks),
            "orphaned_tasks": orphaned_tasks,
        }
