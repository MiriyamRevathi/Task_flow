"""
Analytics Blueprint Routes.
"""

from flask import Blueprint, render_template, g
from taskflow.security.rbac_middleware import login_required

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("")
@login_required
def index():
    analytics = g.analytics_service.get_workspace_analytics(g.current_workspace_id)
    return render_template("analytics/index.html", analytics=analytics)
