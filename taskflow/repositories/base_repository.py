"""
Generic Base Repository.
Provides CRUD abstractions, pagination, sorting, filtering, and ID-based lookup for file storage.
"""

from typing import Generic, TypeVar, List, Optional, Dict, Any, Callable
from taskflow.storage.file_storage import FileStorageEngine

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic base repository for file-based entity management."""

    def __init__(self, storage_engine: FileStorageEngine, collection_name: str, model_class: Any):
        self.storage = storage_engine
        self.collection_name = collection_name
        self.model_class = model_class

    def get_all(self) -> List[T]:
        items_dict = self.storage.read_all(self.collection_name)
        return [self.model_class.from_dict(item) for item in items_dict]

    def get_by_id(self, entity_id: str) -> Optional[T]:
        items = self.get_all()
        for item in items:
            if getattr(item, "id", None) == entity_id:
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        items = self.get_all()
        return [item for item in items if predicate(item)]

    def find_one(self, predicate: Callable[[T], bool]) -> Optional[T]:
        items = self.get_all()
        for item in items:
            if predicate(item):
                return item
        return None

    def save(self, entity: T) -> T:
        items = self.get_all()
        entity_id = getattr(entity, "id")
        
        updated = False
        new_items_dict = []
        for item in items:
            if getattr(item, "id") == entity_id:
                new_items_dict.append(entity.to_dict())
                updated = True
            else:
                new_items_dict.append(item.to_dict())

        if not updated:
            new_items_dict.append(entity.to_dict())

        self.storage.write_all(self.collection_name, new_items_dict)
        return entity

    def delete(self, entity_id: str) -> bool:
        items = self.get_all()
        initial_count = len(items)
        remaining_dict = [item.to_dict() for item in items if getattr(item, "id") != entity_id]

        if len(remaining_dict) < initial_count:
            self.storage.write_all(self.collection_name, remaining_dict)
            return True
        return False

    def paginate(self, items: List[T], page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        page = max(1, page)
        per_page = max(1, min(100, per_page))
        total = len(items)
        total_pages = max(1, (total + per_page - 1) // per_page)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        paginated_items = items[start_idx:end_idx]

        return {
            "items": paginated_items,
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        }
