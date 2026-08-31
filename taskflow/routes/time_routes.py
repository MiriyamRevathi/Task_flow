"""
Time Tracking Blueprint Routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, g
from taskflow.security.rbac_middleware import login_required

time_bp = Blueprint("time", __name__, url_prefix="/time")


@time_bp.route("")
@login_required
def index():
    timesheet = g.time_service.get_user_timesheet(g.current_user.id)
    tasks = g.task_repo.get_by_workspace(g.current_workspace_id)
    return render_template("time/index.html", timesheet=timesheet, tasks=tasks)


@time_bp.route("/start", methods=["POST"])
@login_required
def start():
    task_id = request.form.get("task_id")
    desc = request.form.get("description", "")
    entry, msg = g.time_service.start_timer(g.current_user.id, task_id, desc)
    flash(msg, "success" if entry else "warning")
    return redirect(url_for("time.index"))


@time_bp.route("/stop", methods=["POST"])
@login_required
def stop():
    entry, msg = g.time_service.stop_timer(g.current_user.id)
    flash(msg, "success" if entry else "warning")
    return redirect(url_for("time.index"))
