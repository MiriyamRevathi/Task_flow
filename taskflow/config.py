import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('TASKFLOW_SECRET_KEY', 'taskflow-enterprise-secret-key-production-2026-secure-hash')
    ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    PORT = int(os.environ.get('PORT', 5000))
    HOST = os.environ.get('HOST', '127.0.0.1')
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / 'data' / 'storage'
    ML_MODEL_DIR = DATA_DIR / 'ml_models'
    BACKUP_DIR = DATA_DIR / 'backups'
    EXPORT_DIR = DATA_DIR / 'exports'
    SESSION_COOKIE_NAME = 'taskflow_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400
    PASSWORD_SALT = 'taskflow_enterprise_salt_v1_2026'
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_TIME_SECONDS = 900
    DEFAULT_PAGE_SIZE = 15
    MAX_PAGE_SIZE = 100
    MAX_ATTACHMENT_SIZE_MB = 10
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'xlsx', 'zip', 'txt', 'csv', 'json'}
    RISK_OVERDUE_RATIO_HIGH = 0.25
    RISK_OVERDUE_RATIO_MEDIUM = 0.10
    RISK_BLOCKED_RATIO_HIGH = 0.15
    RISK_BLOCKED_RATIO_MEDIUM = 0.05
    HEALTH_SCORE_EXCELLENT = 85
    HEALTH_SCORE_GOOD = 70
    HEALTH_SCORE_FAIR = 50
    ACTIVITY_LOG_RETENTION_DAYS = 365
    MAX_NOTIFICATIONS_PER_USER = 200
    @classmethod
    def init_app(cls, app=None):
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.ML_MODEL_DIR, exist_ok=True)
        os.makedirs(cls.BACKUP_DIR, exist_ok=True)
        os.makedirs(cls.EXPORT_DIR, exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    DATA_DIR = Path(__file__).resolve().parent.parent / 'tests' / 'test_data'
    ML_MODEL_DIR = DATA_DIR / 'ml_models'
    BACKUP_DIR = DATA_DIR / 'backups'
    EXPORT_DIR = DATA_DIR / 'exports'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config_by_name = {'development': DevelopmentConfig, 'testing': TestingConfig, 'production': ProductionConfig, 'default': DevelopmentConfig}
