"""
Pagination Utility Helpers.
"""

from typing import List, Dict, Any, TypeVar

T = TypeVar("T")


def paginate_list(items: List[T], page: int = 1, per_page: int = 15) -> Dict[str, Any]:
    page = max(1, page)
    per_page = max(1, min(100, per_page))
    total = len(items)
    total_pages = max(1, (total + per_page - 1) // per_page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    return {
        "items": items[start_idx:end_idx],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
