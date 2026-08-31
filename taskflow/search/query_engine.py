"""
Search Query Engine.
"""

from typing import List, Dict, Any


def match_query(query: str, text: str) -> bool:
    if not query or not text:
        return False
    return query.lower() in text.lower()
