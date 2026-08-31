"""
REST API Blueprint Routes.
"""

from flask import Blueprint, jsonify, g
from taskflow.security.rbac_middleware import login_required

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/health")
def health_check():
    return jsonify({"status": "healthy", "service": "TaskFlow Enterprise SaaS", "version": "2.0.0"})


@api_bp.route("/projects")
@login_required
def api_projects():
    projects = g.project_service.get_workspace_projects(g.current_workspace_id)
    return jsonify([p.to_dict() for p in projects])


@api_bp.route("/docs")
def api_docs():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "TaskFlow Enterprise SaaS REST API",
            "version": "2.0.0",
            "description": "API documentation for projects, tasks, kanban, teams, calendar, time tracking, analytics, and scikit-learn ML risk prediction."
        },
        "paths": {
            "/api/v1/health": {"get": {"summary": "System Health Check"}},
            "/api/v1/projects": {"get": {"summary": "List Workspace Projects"}},
            "/api/v1/docs": {"get": {"summary": "OpenAPI Documentation"}}
        }
    })
