"""
TaskFlow Demo Data Seeder.
Populates storage with enterprise seed data including organizations, workspaces, users, projects, tasks,
kanban items, milestones, time entries, notifications, and activity logs.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List
from werkzeug.security import generate_password_hash
from taskflow.storage.file_storage import FileStorageEngine
from taskflow.models.enums import UserRole, ProjectStatus, ProjectPriority, TaskStatus, TaskPriority, MilestoneStatus, RiskLevel


class DataSeeder:
    """Enterprise seed data generator."""

    def __init__(self, storage_engine: FileStorageEngine):
        self.engine = storage_engine

    def seed_all(self, force: bool = False):
        existing_users = self.engine.read_all("users")
        if existing_users and not force:
            print("Data already seeded. Skipping.")
            return

        print("Seeding initial TaskFlow enterprise data...")
        now = datetime.now(timezone.utc)
        
        # 1. Organization
        org_id = "org-100"
        orgs = [{
            "id": org_id,
            "name": "Acme Enterprise Corp",
            "slug": "acme-corp",
            "owner_id": "usr-admin-1",
            "domain": "taskflow.local",
            "logo_url": "https://ui-avatars.com/api/?name=Acme+Corp&background=4f46e5&color=fff",
            "description": "Global enterprise software & innovations solutions.",
            "plan_tier": "ENTERPRISE",
            "max_workspaces": 20,
            "max_members": 500,
            "is_active": True,
            "created_at": (now - timedelta(days=120)).isoformat(),
            "updated_at": now.isoformat(),
            "settings": {"enforce_sso": False, "time_tracking_enabled": True, "ml_insights_enabled": True}
        }]
        self.engine.write_all("organizations", orgs)

        # 2. Workspaces
        ws_id1 = "ws-prod-1"
        ws_id2 = "ws-mkt-2"
        workspaces = [
            {
                "id": ws_id1,
                "organization_id": org_id,
                "name": "Engineering & Product",
                "slug": "engineering-product",
                "description": "Primary workspace for software development, cloud operations, and security teams.",
                "owner_id": "usr-admin-1",
                "member_ids": ["usr-admin-1", "usr-mgr-1", "usr-emp-1", "usr-viewer-1", "usr-lead-1"],
                "is_default": True,
                "is_archived": False,
                "color_theme": "#6366f1",
                "created_at": (now - timedelta(days=120)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": ws_id2,
                "organization_id": org_id,
                "name": "Marketing & Growth",
                "slug": "marketing-growth",
                "description": "Brand campaigns, growth hacking, customer success, and market analytics.",
                "owner_id": "usr-admin-1",
                "member_ids": ["usr-admin-1", "usr-mgr-1", "usr-emp-1"],
                "is_default": False,
                "is_archived": False,
                "color_theme": "#10b981",
                "created_at": (now - timedelta(days=90)).isoformat(),
                "updated_at": now.isoformat(),
            }
        ]
        self.engine.write_all("workspaces", workspaces)

        # 3. Users with Demo Credentials
        users = [
            {
                "id": "usr-admin-1",
                "email": "admin@taskflow.local",
                "password_hash": generate_password_hash("admin123"),
                "first_name": "Alexander",
                "last_name": "Wright",
                "role": UserRole.SUPER_ADMIN.value,
                "organization_id": org_id,
                "workspace_ids": [ws_id1, ws_id2],
                "department": "Executive",
                "job_title": "Chief Technology Officer",
                "avatar_url": "https://ui-avatars.com/api/?name=Alexander+Wright&background=4f46e5&color=fff",
                "phone": "+1-555-0101",
                "bio": "CTO overseeing enterprise engineering architecture.",
                "is_active": True,
                "is_email_verified": True,
                "failed_login_attempts": 0,
                "created_at": (now - timedelta(days=120)).isoformat(),
                "updated_at": now.isoformat(),
                "settings": {"theme": "light", "timezone": "UTC"}
            },
            {
                "id": "usr-mgr-1",
                "email": "manager@taskflow.local",
                "password_hash": generate_password_hash("manager123"),
                "first_name": "Sarah",
                "last_name": "Jenkins",
                "role": UserRole.PROJECT_MANAGER.value,
                "organization_id": org_id,
                "workspace_ids": [ws_id1, ws_id2],
                "department": "Engineering",
                "job_title": "Senior Project Manager",
                "avatar_url": "https://ui-avatars.com/api/?name=Sarah+Jenkins&background=059669&color=fff",
                "phone": "+1-555-0102",
                "bio": "Leading cloud migration and platform modernization.",
                "is_active": True,
                "is_email_verified": True,
                "failed_login_attempts": 0,
                "created_at": (now - timedelta(days=110)).isoformat(),
                "updated_at": now.isoformat(),
                "settings": {"theme": "light", "timezone": "UTC"}
            },
            {
                "id": "usr-lead-1",
                "email": "lead@taskflow.local",
                "password_hash": generate_password_hash("lead123"),
                "first_name": "Marcus",
                "last_name": "Vance",
                "role": UserRole.TEAM_LEAD.value,
                "organization_id": org_id,
                "workspace_ids": [ws_id1],
                "department": "Engineering",
                "job_title": "Tech Lead - Backend Architecture",
                "avatar_url": "https://ui-avatars.com/api/?name=Marcus+Vance&background=d97706&color=fff",
                "phone": "+1-555-0103",
                "bio": "Backend lead specialized in microservices and distributed systems.",
                "is_active": True,
                "is_email_verified": True,
                "failed_login_attempts": 0,
                "created_at": (now - timedelta(days=100)).isoformat(),
                "updated_at": now.isoformat(),
                "settings": {"theme": "light", "timezone": "UTC"}
            },
            {
                "id": "usr-emp-1",
                "email": "employee@taskflow.local",
                "password_hash": generate_password_hash("employee123"),
                "first_name": "Michael",
                "last_name": "Chen",
                "role": UserRole.EMPLOYEE.value,
                "organization_id": org_id,
                "workspace_ids": [ws_id1, ws_id2],
                "department": "Engineering",
                "job_title": "Senior Full-Stack Engineer",
                "avatar_url": "https://ui-avatars.com/api/?name=Michael+Chen&background=2563eb&color=fff",
                "phone": "+1-555-0104",
                "bio": "Full-stack developer building user experiences.",
                "is_active": True,
                "is_email_verified": True,
                "failed_login_attempts": 0,
                "created_at": (now - timedelta(days=90)).isoformat(),
                "updated_at": now.isoformat(),
                "settings": {"theme": "light", "timezone": "UTC"}
            },
            {
                "id": "usr-viewer-1",
                "email": "viewer@taskflow.local",
                "password_hash": generate_password_hash("viewer123"),
                "first_name": "Emily",
                "last_name": "Watson",
                "role": UserRole.VIEWER.value,
                "organization_id": org_id,
                "workspace_ids": [ws_id1],
                "department": "Quality Assurance",
                "job_title": "Stakeholder Auditor",
                "avatar_url": "https://ui-avatars.com/api/?name=Emily+Watson&background=7c3aed&color=fff",
                "phone": "+1-555-0105",
                "bio": "Internal compliance and progress reviewer.",
                "is_active": True,
                "is_email_verified": True,
                "failed_login_attempts": 0,
                "created_at": (now - timedelta(days=80)).isoformat(),
                "updated_at": now.isoformat(),
                "settings": {"theme": "light", "timezone": "UTC"}
            }
        ]
        self.engine.write_all("users", users)

        # 4. Teams
        team_id1 = "team-eng-1"
        team_id2 = "team-devops-2"
        teams = [
            {
                "id": team_id1,
                "organization_id": org_id,
                "workspace_id": ws_id1,
                "name": "Core Platform Engineering",
                "department": "Engineering",
                "lead_id": "usr-lead-1",
                "member_ids": ["usr-lead-1", "usr-emp-1", "usr-mgr-1"],
                "description": "Responsible for API architecture, core services, and application security.",
                "created_at": (now - timedelta(days=110)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": team_id2,
                "organization_id": org_id,
                "workspace_id": ws_id1,
                "name": "Cloud Infrastructure & DevOps",
                "department": "DevOps",
                "lead_id": "usr-admin-1",
                "member_ids": ["usr-admin-1", "usr-emp-1"],
                "description": "Kubernetes clusters, CI/CD deployment pipelines, and reliability engineering.",
                "created_at": (now - timedelta(days=100)).isoformat(),
                "updated_at": now.isoformat(),
            }
        ]
        self.engine.write_all("teams", teams)

        # 5. Projects
        proj1_id = "proj-101"
        proj2_id = "proj-102"
        proj3_id = "proj-103"
        projects = [
            {
                "id": proj1_id,
                "workspace_id": ws_id1,
                "organization_id": org_id,
                "name": "TaskFlow 2.0 Enterprise SaaS Platform",
                "key": "TASK",
                "description": "Next-generation enterprise project management SaaS with AI risk analytics and live collaboration.",
                "owner_id": "usr-mgr-1",
                "team_ids": [team_id1, team_id2],
                "member_ids": ["usr-admin-1", "usr-mgr-1", "usr-lead-1", "usr-emp-1", "usr-viewer-1"],
                "status": ProjectStatus.ACTIVE.value,
                "priority": ProjectPriority.HIGH.value,
                "start_date": (now - timedelta(days=45)).strftime("%Y-%m-%d"),
                "due_date": (now + timedelta(days=45)).strftime("%Y-%m-%d"),
                "progress_percentage": 68.5,
                "budget": 150000.0,
                "spent_budget": 95000.0,
                "tags": ["saas", "python", "flask", "ml", "enterprise"],
                "risk_level": RiskLevel.LOW_RISK.value,
                "risk_score": 18.4,
                "health_score": 88.5,
                "health_category": "HEALTHY",
                "created_at": (now - timedelta(days=45)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": proj2_id,
                "workspace_id": ws_id1,
                "organization_id": org_id,
                "name": "Cloud Infrastructure Migration & Security Audit",
                "key": "CLOUD",
                "description": "Migrate core microservices to high-availability local storage containers and zero-trust security.",
                "owner_id": "usr-admin-1",
                "team_ids": [team_id2],
                "member_ids": ["usr-admin-1", "usr-emp-1"],
                "status": ProjectStatus.ACTIVE.value,
                "priority": ProjectPriority.CRITICAL.value,
                "start_date": (now - timedelta(days=30)).strftime("%Y-%m-%d"),
                "due_date": (now + timedelta(days=15)).strftime("%Y-%m-%d"),
                "progress_percentage": 42.0,
                "budget": 85000.0,
                "spent_budget": 55000.0,
                "tags": ["cloud", "devops", "security", "docker"],
                "risk_level": RiskLevel.MEDIUM_RISK.value,
                "risk_score": 48.0,
                "health_score": 68.0,
                "health_category": "AT_RISK",
                "created_at": (now - timedelta(days=30)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": proj3_id,
                "workspace_id": ws_id2,
                "organization_id": org_id,
                "name": "Q3 Enterprise Product Marketing & Growth Launch",
                "key": "MKTG",
                "description": "Omnichannel global marketing launch campaign, developer webinars, and enterprise collateral.",
                "owner_id": "usr-mgr-1",
                "team_ids": [],
                "member_ids": ["usr-mgr-1", "usr-emp-1"],
                "status": ProjectStatus.PLANNING.value,
                "priority": ProjectPriority.MEDIUM.value,
                "start_date": now.strftime("%Y-%m-%d"),
                "due_date": (now + timedelta(days=60)).strftime("%Y-%m-%d"),
                "progress_percentage": 10.0,
                "budget": 50000.0,
                "spent_budget": 4500.0,
                "tags": ["growth", "marketing", "webinar"],
                "risk_level": RiskLevel.LOW_RISK.value,
                "risk_score": 12.0,
                "health_score": 92.0,
                "health_category": "HEALTHY",
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }
        ]
        self.engine.write_all("projects", projects)

        # 6. Milestones
        ms1_id = "ms-201"
        ms2_id = "ms-202"
        milestones = [
            {
                "id": ms1_id,
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "title": "Phase 1: Core Engine & Authentication",
                "description": "Complete local JSON storage engine, role-based access security, and session management.",
                "status": MilestoneStatus.COMPLETED.value,
                "start_date": (now - timedelta(days=45)).strftime("%Y-%m-%d"),
                "due_date": (now - timedelta(days=15)).strftime("%Y-%m-%d"),
                "completed_at": (now - timedelta(days=14)).isoformat(),
                "completion_percentage": 100.0,
                "task_ids": ["task-1", "task-2"],
                "created_at": (now - timedelta(days=45)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": ms2_id,
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "title": "Phase 2: Interactive Kanban Board & Analytics Engine",
                "description": "Interactive drag-and-drop Kanban project board, time tracking timer, and scikit-learn ML risk insights.",
                "status": MilestoneStatus.IN_PROGRESS.value,
                "start_date": (now - timedelta(days=14)).strftime("%Y-%m-%d"),
                "due_date": (now + timedelta(days=20)).strftime("%Y-%m-%d"),
                "completed_at": None,
                "completion_percentage": 65.0,
                "task_ids": ["task-3", "task-4", "task-5", "task-6"],
                "created_at": (now - timedelta(days=14)).isoformat(),
                "updated_at": now.isoformat(),
            }
        ]
        self.engine.write_all("milestones", milestones)

        # 7. Tasks
        tasks = [
            {
                "id": "task-1",
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "title": "Build atomic JSON file storage persistence engine",
                "description": "Implement thread-safe file reading, atomic writing via temp file move, and memory caching.",
                "assignee_id": "usr-lead-1",
                "creator_id": "usr-admin-1",
                "team_id": team_id1,
                "milestone_id": ms1_id,
                "status": TaskStatus.DONE.value,
                "priority": TaskPriority.HIGH.value,
                "start_date": (now - timedelta(days=40)).strftime("%Y-%m-%d"),
                "due_date": (now - timedelta(days=30)).strftime("%Y-%m-%d"),
                "completed_at": (now - timedelta(days=29)).isoformat(),
                "estimated_hours": 16.0,
                "actual_hours": 14.5,
                "tags": ["backend", "storage", "json"],
                "checklist": [{"title": "File locks", "completed": True}, {"title": "Atomic rename", "completed": True}],
                "dependencies": [],
                "attachments": [],
                "comments": [{"id": "c1", "author_id": "usr-admin-1", "author_name": "Alexander Wright", "content": "Atomic storage tested successfully.", "created_at": (now - timedelta(days=29)).isoformat()}],
                "order_index": 1,
                "created_at": (now - timedelta(days=40)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": "task-2",
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "title": "Implement RBAC session authentication & user password hashing",
                "description": "Secure Werkzeug password hashing, session cookies, and 6 role permission decorators.",
                "assignee_id": "usr-emp-1",
                "creator_id": "usr-mgr-1",
                "team_id": team_id1,
                "milestone_id": ms1_id,
                "status": TaskStatus.DONE.value,
                "priority": TaskPriority.CRITICAL.value,
                "start_date": (now - timedelta(days=28)).strftime("%Y-%m-%d"),
                "due_date": (now - timedelta(days=16)).strftime("%Y-%m-%d"),
                "completed_at": (now - timedelta(days=15)).isoformat(),
                "estimated_hours": 24.0,
                "actual_hours": 22.0,
                "tags": ["security", "auth", "rbac"],
                "checklist": [{"title": "Password Hashing", "completed": True}, {"title": "Session protection", "completed": True}],
                "dependencies": ["task-1"],
                "attachments": [],
                "comments": [],
                "order_index": 2,
                "created_at": (now - timedelta(days=28)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": "task-3",
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "title": "Develop vanilla JS Drag-and-Drop interactive Kanban board UI",
                "description": "Create smooth column card drag/drop status updates, filter controls, and modal card editor.",
                "assignee_id": "usr-emp-1",
                "creator_id": "usr-mgr-1",
                "team_id": team_id1,
                "milestone_id": ms2_id,
                "status": TaskStatus.IN_PROGRESS.value,
                "priority": TaskPriority.HIGH.value,
                "start_date": (now - timedelta(days=12)).strftime("%Y-%m-%d"),
                "due_date": (now + timedelta(days=5)).strftime("%Y-%m-%d"),
                "completed_at": None,
                "estimated_hours": 32.0,
                "actual_hours": 20.0,
                "tags": ["kanban", "js", "frontend", "ui"],
                "checklist": [{"title": "HTML5 Drag-Drop", "completed": True}, {"title": "Card Modal Editor", "completed": True}, {"title": "Priority Badges", "completed": False}],
                "dependencies": ["task-2"],
                "attachments": [],
                "comments": [{"id": "c2", "author_id": "usr-mgr-1", "author_name": "Sarah Jenkins", "content": "Drag & drop animation feels very responsive!", "created_at": (now - timedelta(days=2)).isoformat()}],
                "order_index": 1,
                "created_at": (now - timedelta(days=12)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": "task-4",
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "title": "Train scikit-learn RandomForest project risk prediction model",
                "description": "Extract project features (overdue ratio, completion velocity, team workload) and train classifier.",
                "assignee_id": "usr-lead-1",
                "creator_id": "usr-admin-1",
                "team_id": team_id1,
                "milestone_id": ms2_id,
                "status": TaskStatus.IN_REVIEW.value,
                "priority": TaskPriority.HIGH.value,
                "start_date": (now - timedelta(days=10)).strftime("%Y-%m-%d"),
                "due_date": (now + timedelta(days=8)).strftime("%Y-%m-%d"),
                "completed_at": None,
                "estimated_hours": 20.0,
                "actual_hours": 18.0,
                "tags": ["ml", "scikit-learn", "risk-engine"],
                "checklist": [{"title": "Feature Extractor", "completed": True}, {"title": "Model Training Script", "completed": True}, {"title": "Model Registry", "completed": True}],
                "dependencies": ["task-1"],
                "attachments": [],
                "comments": [],
                "order_index": 2,
                "created_at": (now - timedelta(days=10)).isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": "task-5",
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "title": "Build live work time tracking timer and timesheet summary views",
                "description": "Include live start/stop/pause timer widget and manual timesheet entry with billable rate calculations.",
                "assignee_id": "usr-emp-1",
                "creator_id": "usr-mgr-1",
                "team_id": team_id1,
                "milestone_id": ms2_id,
                "status": TaskStatus.TODO.value,
                "priority": TaskPriority.MEDIUM.value,
                "start_date": now.strftime("%Y-%m-%d"),
                "due_date": (now + timedelta(days=12)).strftime("%Y-%m-%d"),
                "completed_at": None,
                "estimated_hours": 16.0,
                "actual_hours": 0.0,
                "tags": ["time-tracking", "timer", "timesheet"],
                "checklist": [{"title": "Live JS Timer Widget", "completed": False}, {"title": "Timesheet Table", "completed": False}],
                "dependencies": [],
                "attachments": [],
                "comments": [],
                "order_index": 3,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            },
            {
                "id": "task-6",
                "project_id": proj2_id,
                "workspace_id": ws_id1,
                "title": "Configure zero-trust Docker container network policies",
                "description": "Strict ingress/egress rules and security isolation for enterprise local deployments.",
                "assignee_id": "usr-admin-1",
                "creator_id": "usr-admin-1",
                "team_id": team_id2,
                "milestone_id": None,
                "status": TaskStatus.BLOCKED.value,
                "priority": TaskPriority.CRITICAL.value,
                "start_date": (now - timedelta(days=15)).strftime("%Y-%m-%d"),
                "due_date": (now - timedelta(days=2)).strftime("%Y-%m-%d"),
                "completed_at": None,
                "estimated_hours": 24.0,
                "actual_hours": 12.0,
                "tags": ["docker", "security", "devops"],
                "checklist": [{"title": "Network policy yaml", "completed": False}],
                "dependencies": [],
                "attachments": [],
                "comments": [{"id": "c3", "author_id": "usr-admin-1", "author_name": "Alexander Wright", "content": "Waiting for firewall port allocation.", "created_at": (now - timedelta(days=1)).isoformat()}],
                "order_index": 1,
                "created_at": (now - timedelta(days=15)).isoformat(),
                "updated_at": now.isoformat(),
            }
        ]
        self.engine.write_all("tasks", tasks)

        # 8. Time Entries
        time_entries = [
            {
                "id": "time-1",
                "user_id": "usr-lead-1",
                "task_id": "task-1",
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "description": "Storage lock implementation and testing.",
                "hours": 8.0,
                "start_time": (now - timedelta(days=35)).isoformat(),
                "end_time": (now - timedelta(days=35)).isoformat(),
                "is_running": False,
                "is_billable": True,
                "hourly_rate": 95.0,
                "created_at": (now - timedelta(days=35)).isoformat(),
                "updated_at": (now - timedelta(days=35)).isoformat(),
            },
            {
                "id": "time-2",
                "user_id": "usr-emp-1",
                "task_id": "task-3",
                "project_id": proj1_id,
                "workspace_id": ws_id1,
                "description": "Kanban drag and drop event listeners.",
                "hours": 6.5,
                "start_time": (now - timedelta(days=5)).isoformat(),
                "end_time": (now - timedelta(days=5)).isoformat(),
                "is_running": False,
                "is_billable": True,
                "hourly_rate": 85.0,
                "created_at": (now - timedelta(days=5)).isoformat(),
                "updated_at": (now - timedelta(days=5)).isoformat(),
            }
        ]
        self.engine.write_all("time_entries", time_entries)

        # 9. Notifications
        notifications = [
            {
                "id": "notif-1",
                "user_id": "usr-emp-1",
                "title": "New Task Assigned",
                "message": "Sarah Jenkins assigned you to 'Develop vanilla JS Drag-and-Drop interactive Kanban board UI'.",
                "type": "TASK_ASSIGNED",
                "read": False,
                "link_url": "/tasks/task-3",
                "project_id": proj1_id,
                "task_id": "task-3",
                "actor_id": "usr-mgr-1",
                "created_at": (now - timedelta(days=12)).isoformat(),
            },
            {
                "id": "notif-2",
                "user_id": "usr-admin-1",
                "title": "Task Blocked Alert",
                "message": "Task 'Configure zero-trust Docker container network policies' was marked BLOCKED.",
                "type": "SYSTEM_ALERT",
                "read": True,
                "link_url": "/tasks/task-6",
                "project_id": proj2_id,
                "task_id": "task-6",
                "actor_id": "usr-admin-1",
                "created_at": (now - timedelta(days=1)).isoformat(),
            }
        ]
        self.engine.write_all("notifications", notifications)

        # 10. Activities
        activities = [
            {
                "id": "act-1",
                "actor_id": "usr-admin-1",
                "actor_name": "Alexander Wright",
                "action": "CREATE",
                "target_type": "PROJECT",
                "target_id": proj1_id,
                "target_name": "TaskFlow 2.0 Enterprise SaaS Platform",
                "description": "Alexander Wright created project TaskFlow 2.0 Enterprise SaaS Platform",
                "workspace_id": ws_id1,
                "project_id": proj1_id,
                "details": {},
                "created_at": (now - timedelta(days=45)).isoformat(),
            },
            {
                "id": "act-2",
                "actor_id": "usr-emp-1",
                "actor_name": "Michael Chen",
                "action": "STATUS_CHANGE",
                "target_type": "TASK",
                "target_id": "task-3",
                "target_name": "Develop vanilla JS Drag-and-Drop interactive Kanban board UI",
                "description": "Michael Chen moved task Develop vanilla JS Drag-and-Drop interactive Kanban board UI to IN_PROGRESS",
                "workspace_id": ws_id1,
                "project_id": proj1_id,
                "details": {"old_status": "TODO", "new_status": "IN_PROGRESS"},
                "created_at": (now - timedelta(days=12)).isoformat(),
            }
        ]
        self.engine.write_all("activities", activities)
        
        # 11. Settings
        settings = [{
            "id": "global",
            "app_name": "TaskFlow Enterprise",
            "maintenance_mode": False,
            "allow_registration": True,
            "default_user_role": "EMPLOYEE",
            "max_upload_size_mb": 10,
            "session_timeout_minutes": 1440,
            "theme_default": "light",
            "updated_at": now.isoformat()
        }]
        self.engine.write_all("settings", settings)

        print("Seeding complete! Demo data populated successfully.")
