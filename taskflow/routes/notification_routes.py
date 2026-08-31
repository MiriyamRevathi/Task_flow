"""
Notification Blueprint Routes.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, g
from taskflow.security.rbac_middleware import login_required

notification_bp = Blueprint("notification", __name__, url_prefix="/notifications")


@notification_bp.route("")
@login_required
def index():
    notifications = g.notification_service.get_user_notifications(g.current_user.id)
    return render_template("notifications/index.html", notifications=notifications)


@notification_bp.route("/read-all", methods=["POST"])
@login_required
def mark_read_all():
    g.notification_service.mark_all_read(g.current_user.id)
    flash("All notifications marked as read.", "success")
    return redirect(url_for("notification.index"))
