"""
Flask Auth Routes Blueprint.
Handles login, registration, logout, profile view, password update, and unauthorized access pages.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from taskflow.security.session_manager import SessionManager
from taskflow.security.rbac_middleware import login_required
from taskflow.models.enums import UserRole

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if SessionManager.is_authenticated():
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user, message = g.auth_service.authenticate(email, password)
        if user:
            workspaces = g.workspace_repo.get_user_workspaces(
                user.id, user.organization_id or "org-100", user.is_org_admin()
            )
            default_ws_id = workspaces[0].id if workspaces else "ws-prod-1"
            SessionManager.login_user(user.id, user.organization_id or "org-100", default_ws_id, user.role)
            flash(f"Welcome back, {user.first_name}!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.index"))
        else:
            flash(message, "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if SessionManager.is_authenticated():
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        role = request.form.get("role", UserRole.EMPLOYEE.value)

        user, message = g.auth_service.register_user(email, password, first_name, last_name, role)
        if user:
            flash("Account registered successfully! Please log in.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash(message, "danger")

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    SessionManager.logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile")
@login_required
def profile():
    user = g.current_user
    return render_template("auth/profile.html", user=user)


@auth_bp.route("/unauthorized")
def unauthorized():
    return render_template("errors/403.html"), 403
