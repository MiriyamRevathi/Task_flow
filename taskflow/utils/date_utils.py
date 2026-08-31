"""
Date & Time Utility Module.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def format_date_display(iso_str: Optional[str], fmt: str = "%b %d, %Y") -> str:
    if not iso_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime(fmt)
    except Exception:
        return iso_str


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            return None


def days_until(date_str: Optional[str]) -> int:
    dt = parse_date(date_str)
    if not dt:
        return 0
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = dt - now
    return delta.days
