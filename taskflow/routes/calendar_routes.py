"""
Calendar Blueprint Routes.
"""

from flask import Blueprint, render_template, jsonify, g
from taskflow.security.rbac_middleware import login_required

calendar_bp = Blueprint("calendar", __name__, url_prefix="/calendar")


@calendar_bp.route("")
@login_required
def index():
    events = g.calendar_service.get_workspace_events(g.current_workspace_id)
    return render_template("calendar/index.html", events=events)


@calendar_bp.route("/events")
@login_required
def get_events_json():
    events = g.calendar_service.get_workspace_events(g.current_workspace_id)
    return jsonify(events)
