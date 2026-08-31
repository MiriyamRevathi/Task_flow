"""
Storage Transaction Manager.
Provides context-managed transaction support for executing batch updates across multiple storage collections atomically.
"""

from typing import Dict, List, Any
from taskflow.storage.file_storage import FileStorageEngine


class StorageTransaction:
    """Transaction wrapper supporting rollbacks on multi-collection updates."""

    def __init__(self, storage_engine: FileStorageEngine):
        self.engine = storage_engine
        self._snapshots: Dict[str, List[Dict[str, Any]]] = {}
        self._staged: Dict[str, List[Dict[str, Any]]] = {}
        self._active = False

    def __enter__(self):
        self._snapshots.clear()
        self._staged.clear()
        self._active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        self._active = False

    def stage_write(self, collection_name: str, items: List[Dict[str, Any]]):
        if not self._active:
            raise RuntimeError("Transaction is not active")
            
        if collection_name not in self._snapshots:
            self._snapshots[collection_name] = self.engine.read_all(collection_name)
            
        self._staged[collection_name] = items

    def commit(self) -> bool:
        if not self._active:
            raise RuntimeError("Transaction is not active")
            
        written_collections = []
        try:
            for col_name, items in self._staged.items():
                if not self.engine.write_all(col_name, items):
                    raise IOError(f"Failed writing staged data for {col_name}")
                written_collections.append(col_name)
            return True
        except Exception as e:
            print(f"Transaction commit failed: {e}. Rolling back...")
            # Revert already written collections
            for col_name in written_collections:
                if col_name in self._snapshots:
                    self.engine.write_all(col_name, self._snapshots[col_name])
            return False

    def rollback(self):
        for col_name, original_items in self._snapshots.items():
            self.engine.write_all(col_name, original_items)
        self._staged.clear()
