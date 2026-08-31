"""
Unique ID Generator.
Generates prefixed readable unique IDs for entity records.
"""

import uuid
import time


def generate_id(prefix: str = "id") -> str:
    short_uuid = uuid.uuid4().hex[:8]
    return f"{prefix}-{short_uuid}"


def generate_timestamped_id(prefix: str = "rec") -> str:
    ts = int(time.time())
    short_uuid = uuid.uuid4().hex[:4]
    return f"{prefix}-{ts}-{short_uuid}"
