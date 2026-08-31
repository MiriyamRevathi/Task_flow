from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = 'SUPER_ADMIN'
    ORG_ADMIN = 'ORG_ADMIN'
    PROJECT_MANAGER = 'PROJECT_MANAGER'
    TEAM_LEAD = 'TEAM_LEAD'
    EMPLOYEE = 'EMPLOYEE'
    VIEWER = 'VIEWER'

    @classmethod
    def choices(cls):
        return [role.value for role in cls]

    @property
    def display_name(self):
        titles = {
            'SUPER_ADMIN': 'Super Administrator',
            'ORG_ADMIN': 'Organization Administrator',
            'PROJECT_MANAGER': 'Project Manager',
            'TEAM_LEAD': 'Team Lead',
            'EMPLOYEE': 'Employee / Team Member',
            'VIEWER': 'Read-Only Viewer'
        }
        return titles.get(self.value, self.value)

class ProjectStatus(str, Enum):
    PLANNING = 'PLANNING'
    ACTIVE = 'ACTIVE'
    ON_HOLD = 'ON_HOLD'
    COMPLETED = 'COMPLETED'
    ARCHIVED = 'ARCHIVED'

    @classmethod
    def choices(cls):
        return [s.value for s in cls]

class ProjectPriority(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

    @classmethod
    def choices(cls):
        return [p.value for p in cls]

class TaskStatus(str, Enum):
    BACKLOG = 'BACKLOG'
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    IN_REVIEW = 'IN_REVIEW'
    BLOCKED = 'BLOCKED'
    DONE = 'DONE'

    @classmethod
    def choices(cls):
        return [s.value for s in cls]

    @property
    def is_terminal(self):
        return self.value == 'DONE'

class TaskPriority(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

    @classmethod
    def choices(cls):
        return [p.value for p in cls]

class MilestoneStatus(str, Enum):
    UPCOMING = 'UPCOMING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    DELAYED = 'DELAYED'
    CANCELLED = 'CANCELLED'

    @classmethod
    def choices(cls):
        return [m.value for m in cls]

class NotificationType(str, Enum):
    TASK_ASSIGNED = 'TASK_ASSIGNED'
    TASK_COMPLETED = 'TASK_COMPLETED'
    TASK_OVERDUE = 'TASK_OVERDUE'
    MENTION = 'MENTION'
    PROJECT_UPDATE = 'PROJECT_UPDATE'
    MILESTONE_APPROACHING = 'MILESTONE_APPROACHING'
    COMMENT_ADDED = 'COMMENT_ADDED'
    STATUS_CHANGED = 'STATUS_CHANGED'
    SYSTEM_ALERT = 'SYSTEM_ALERT'

    @classmethod
    def choices(cls):
        return [n.value for n in cls]

class ActivityAction(str, Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    STATUS_CHANGE = 'STATUS_CHANGE'
    ASSIGN = 'ASSIGN'
    COMPLETE = 'COMPLETE'
    COMMENT = 'COMMENT'
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'
    ARCHIVE = 'ARCHIVE'
    RESTORE = 'RESTORE'

    @classmethod
    def choices(cls):
        return [a.value for a in cls]

class RiskLevel(str, Enum):
    LOW_RISK = 'LOW_RISK'
    MEDIUM_RISK = 'MEDIUM_RISK'
    HIGH_RISK = 'HIGH_RISK'

    @classmethod
    def choices(cls):
        return [r.value for r in cls]

class HealthCategory(str, Enum):
    HEALTHY = 'HEALTHY'
    AT_RISK = 'AT_RISK'
    CRITICAL = 'CRITICAL'
