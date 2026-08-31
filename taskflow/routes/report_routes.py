"""
Report Blueprint Routes.
"""

from flask import Blueprint, render_template, Response, request, g
from taskflow.security.rbac_middleware import login_required

report_bp = Blueprint("report", __name__, url_prefix="/reports")


@report_bp.route("")
@login_required
def index():
    exec_report = g.reporting_service.generate_executive_report(g.current_workspace_id)
    return render_template("reports/index.html", report=exec_report)


@report_bp.route("/export/csv")
@login_required
def export_csv():
    exec_report = g.reporting_service.generate_executive_report(g.current_workspace_id)
    csv_data = g.export_service.export_to_csv(exec_report["projects_summary"])
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=projects_report.csv"}
    )
