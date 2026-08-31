# TaskFlow — Enterprise Project Management SaaS

TaskFlow is a production-grade Enterprise Project Management SaaS platform built with Python (Flask, Jinja2, scikit-learn, pandas, numpy), HTML5/CSS3, vanilla JavaScript, and an atomic JSON file storage engine.

## Features
- **Local Persistence**: Atomic file locking and transaction support. Zero external database required.
- **Role-Based Access Control**: 6 role tiers (Super Admin, Org Admin, Project Manager, Team Lead, Employee, Viewer).
- **Interactive Drag-and-Drop Kanban Board**: Vanilla JS status updates.
- **Machine Learning Risk Engine**: Local scikit-learn RandomForest & GradientBoosting model predicting project risk levels (LOW, MEDIUM, HIGH).
- **Live Work Time Tracking**: Live start/stop timer widget and timesheets.
- **Project Calendar**: Interactive month grid overlaying task deadlines and milestones.
- **Activity & Audit Logging**: Immutable history of all user actions.
- **Executive Reporting & Export**: CSV and JSON report downloads.

## Demo Accounts
| Role | Email | Password |
|---|---|---|
| Super Admin | admin@taskflow.local | admin123 |
| Project Manager | manager@taskflow.local | manager123 |
| Team Lead | lead@taskflow.local | lead123 |
| Employee | employee@taskflow.local | employee123 |
| Viewer | viewer@taskflow.local | viewer123 |

## Local Installation
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
App runs at: http://127.0.0.1:5000

## Lockfile Installation
```bash
pip install -r requirements.lock
```

## Running via Docker
```bash
docker build -t taskflow-saas .
docker run -p 5000:5000 taskflow-saas
```

## Running Tests
```bash
pytest
```
