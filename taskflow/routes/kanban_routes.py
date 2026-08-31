"""
Kanban Board Blueprint Routes.
"""

from flask import Blueprint, render_template, request, jsonify, g
from taskflow.security.rbac_middleware import login_required

kanban_bp = Blueprint("kanban", __name__, url_prefix="/kanban")


@kanban_bp.route("")
@login_required
def board():
    project_id = request.args.get("project_id")
    board_data = g.kanban_service.get_board_data(g.current_workspace_id, project_id)
    projects = g.project_repo.get_by_workspace(g.current_workspace_id)
    return render_template("kanban/board.html", board=board_data, projects=projects, selected_project_id=project_id)


@kanban_bp.route("/move", methods=["POST"])
@login_required
def move_card():
    data = request.get_json() or {}
    task_id = data.get("task_id")
    new_status = data.get("new_status")

    if not task_id or not new_status:
        return jsonify({"success": False, "error": "Missing task_id or new_status"}), 400

    task, msg = g.task_service.update_task_status(task_id, new_status)
    if task:
        # Trigger progress update for project
        g.project_service.update_progress(task.project_id)
        return jsonify({"success": True, "message": msg, "task": task.to_dict()})
    return jsonify({"success": False, "error": msg}), 400
