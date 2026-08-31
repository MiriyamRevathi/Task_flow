"""
TaskFlow Enterprise Project Management SaaS.
Main application factory & entry point.
"""

from flask import Flask, g
from taskflow.config import config_by_name, Config
from taskflow.storage.file_storage import FileStorageEngine
from taskflow.storage.seeder import DataSeeder
from taskflow.storage.migrator import StorageMigrator

# Repositories
from taskflow.repositories.user_repository import UserRepository
from taskflow.repositories.organization_repository import OrganizationRepository
from taskflow.repositories.workspace_repository import WorkspaceRepository
from taskflow.repositories.project_repository import ProjectRepository
from taskflow.repositories.task_repository import TaskRepository
from taskflow.repositories.milestone_repository import MilestoneRepository
from taskflow.repositories.team_repository import TeamRepository
from taskflow.repositories.calendar_repository import CalendarRepository
from taskflow.repositories.time_repository import TimeRepository
from taskflow.repositories.notification_repository import NotificationRepository
from taskflow.repositories.activity_repository import ActivityRepository

# Services
from taskflow.services.auth_service import AuthService
from taskflow.services.workspace_service import WorkspaceService
from taskflow.services.project_service import ProjectService
from taskflow.services.task_service import TaskService
from taskflow.services.kanban_service import KanbanService
from taskflow.services.milestone_service import MilestoneService
from taskflow.services.team_service import TeamService
from taskflow.services.calendar_service import CalendarService
from taskflow.services.time_tracking_service import TimeTrackingService
from taskflow.services.notification_service import NotificationService
from taskflow.services.audit_service import AuditService
from taskflow.services.analytics_service import AnalyticsService
from taskflow.services.ml_service import MLService
from taskflow.services.reporting_service import ReportingService
from taskflow.services.admin_service import AdminService
from taskflow.services.export_service import ExportService
from taskflow.services.search_service import SearchService

# Routes
from taskflow.routes.auth_routes import auth_bp
from taskflow.routes.dashboard_routes import dashboard_bp
from taskflow.routes.workspace_routes import workspace_bp
from taskflow.routes.project_routes import project_bp
from taskflow.routes.task_routes import task_bp
from taskflow.routes.kanban_routes import kanban_bp
from taskflow.routes.milestone_routes import milestone_bp
from taskflow.routes.team_routes import team_bp
from taskflow.routes.calendar_routes import calendar_bp
from taskflow.routes.time_routes import time_bp
from taskflow.routes.notification_routes import notification_bp
from taskflow.routes.activity_routes import activity_bp
from taskflow.routes.analytics_routes import analytics_bp
from taskflow.routes.ml_routes import ml_bp
from taskflow.routes.report_routes import report_bp
from taskflow.routes.admin_routes import admin_bp
from taskflow.routes.search_routes import search_bp
from taskflow.routes.api_routes import api_bp

from taskflow.security.session_manager import SessionManager


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    Config.init_app(app)

    # Storage & Seed
    storage_engine = FileStorageEngine(app.config["DATA_DIR"])
    migrator = StorageMigrator(storage_engine)
    migrator.check_and_migrate()
    seeder = DataSeeder(storage_engine)
    seeder.seed_all()

    # Instantiate Repositories
    user_repo = UserRepository(storage_engine)
    org_repo = OrganizationRepository(storage_engine)
    ws_repo = WorkspaceRepository(storage_engine)
    proj_repo = ProjectRepository(storage_engine)
    task_repo = TaskRepository(storage_engine)
    ms_repo = MilestoneRepository(storage_engine)
    team_repo = TeamRepository(storage_engine)
    cal_repo = CalendarRepository(storage_engine)
    time_repo = TimeRepository(storage_engine)
    notif_repo = NotificationRepository(storage_engine)
    act_repo = ActivityRepository(storage_engine)

    # Instantiate Services
    auth_service = AuthService(user_repo, org_repo, ws_repo)
    ws_service = WorkspaceService(ws_repo, user_repo)
    proj_service = ProjectService(proj_repo, task_repo)
    task_service = TaskService(task_repo, proj_repo)
    kanban_service = KanbanService(task_repo, user_repo)
    ms_service = MilestoneService(ms_repo)
    team_service = TeamService(team_repo, task_repo, user_repo)
    cal_service = CalendarService(cal_repo, task_repo, ms_repo)
    time_service = TimeTrackingService(time_repo, task_repo)
    notif_service = NotificationService(notif_repo)
    audit_service = AuditService(act_repo)
    analytics_service = AnalyticsService(proj_repo, task_repo)
    ml_service = MLService(proj_repo, task_repo)
    reporting_service = ReportingService(proj_repo, task_repo, user_repo, time_repo)
    admin_service = AdminService(user_repo, org_repo, ws_repo)
    export_service = ExportService()
    search_service = SearchService(proj_repo, task_repo, team_repo, ms_repo)

    @app.before_request
    def inject_context():
        g.storage_engine = storage_engine
        g.user_repo = user_repo
        g.workspace_repo = ws_repo
        g.project_repo = proj_repo
        g.task_repo = task_repo
        g.milestone_repo = ms_repo

        g.auth_service = auth_service
        g.workspace_service = ws_service
        g.project_service = proj_service
        g.task_service = task_service
        g.kanban_service = kanban_service
        g.milestone_service = ms_service
        g.team_service = team_service
        g.calendar_service = cal_service
        g.time_service = time_service
        g.notification_service = notif_service
        g.audit_service = audit_service
        g.analytics_service = analytics_service
        g.ml_service = ml_service
        g.reporting_service = reporting_service
        g.admin_service = admin_service
        g.export_service = export_service
        g.search_service = search_service

        current_user_id = SessionManager.get_current_user_id()
        g.current_user = user_repo.get_by_id(current_user_id) if current_user_id else None
        
        ws_id = SessionManager.get_current_workspace_id() or "ws-prod-1"
        g.current_workspace_id = ws_id
        g.current_workspace = ws_repo.get_by_id(ws_id)

    @app.context_processor
    def inject_template_globals():
        current_user_id = SessionManager.get_current_user_id()
        user = user_repo.get_by_id(current_user_id) if current_user_id else None
        workspaces = ws_repo.get_user_workspaces(user.id, user.organization_id or "org-100", user.is_org_admin()) if user else []
        ws_id = SessionManager.get_current_workspace_id() or "ws-prod-1"
        current_ws = ws_repo.get_by_id(ws_id)

        return {
            "current_user": user,
            "current_workspace": current_ws,
            "user_workspaces": workspaces,
        }

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(workspace_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(kanban_bp)
    app.register_blueprint(milestone_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(time_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))

    return app


app = create_app("development")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
