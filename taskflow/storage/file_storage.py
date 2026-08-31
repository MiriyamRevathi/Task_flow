"""
Atomic JSON File Storage Engine.
Provides thread-safe atomic read and write access to local JSON files with locking, schema validation,
caching, backup creation, and corruption recovery helpers.
"""

import os
import json
import shutil
import threading
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path
from taskflow.config import Config


class FileStorageEngine:
    """Thread-safe, atomic file persistence engine."""

    _lock = threading.RLock()
    _memory_cache: Dict[str, List[Dict[str, Any]]] = {}

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = Path(data_dir) if data_dir else Config.DATA_DIR
        os.makedirs(self.data_dir, exist_ok=True)

    def _get_filepath(self, collection_name: str) -> Path:
        filename = f"{collection_name}.json" if not collection_name.endswith(".json") else collection_name
        return self.data_dir / filename

    def read_all(self, collection_name: str, use_cache: bool = False) -> List[Dict[str, Any]]:
        with self._lock:
            if use_cache and collection_name in self._memory_cache:
                return [dict(item) for item in self._memory_cache[collection_name]]

            filepath = self._get_filepath(collection_name)
            if not filepath.exists():
                self.write_all(collection_name, [])
                return []

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:
                        return []
                    data = json.loads(content)
                    if isinstance(data, list):
                        self._memory_cache[collection_name] = data
                        return [dict(item) for item in data]
                    return []
            except (json.JSONDecodeError, IOError) as e:
                # Attempt recovery from backup if corrupt
                recovered = self._recover_from_backup(collection_name)
                if recovered is not None:
                    return recovered
                print(f"File Storage Error reading {collection_name}: {e}")
                return []

    def write_all(self, collection_name: str, items: List[Dict[str, Any]]) -> bool:
        with self._lock:
            filepath = self._get_filepath(collection_name)
            temp_filepath = filepath.with_suffix(".tmp")
            
            try:
                # Always format nicely with indent=2
                json_str = json.dumps(items, indent=2, ensure_ascii=False)
                
                with open(temp_filepath, "w", encoding="utf-8") as f:
                    f.write(json_str)
                    f.flush()
                    os.fsync(f.fileno())

                # Atomic replace on file systems
                shutil.move(str(temp_filepath), str(filepath))
                
                # Update memory cache
                self._memory_cache[collection_name] = items
                return True
            except Exception as e:
                print(f"Error writing to {collection_name}: {e}")
                if temp_filepath.exists():
                    try:
                        os.remove(temp_filepath)
                    except OSError:
                        pass
                return False

    def create_backup(self, collection_name: str) -> Optional[str]:
        with self._lock:
            filepath = self._get_filepath(collection_name)
            if not filepath.exists():
                return None
            
            backup_dir = Config.BACKUP_DIR
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filepath = backup_dir / f"{collection_name}_{timestamp}.json"
            
            try:
                shutil.copy2(filepath, backup_filepath)
                return str(backup_filepath)
            except Exception as e:
                print(f"Backup creation error for {collection_name}: {e}")
                return None

    def _recover_from_backup(self, collection_name: str) -> Optional[List[Dict[str, Any]]]:
        backup_dir = Config.BACKUP_DIR
        if not backup_dir.exists():
            return None
            
        pattern = f"{collection_name}_*.json"
        backups = sorted(backup_dir.glob(pattern), reverse=True)
        if not backups:
            return None

        latest_backup = backups[0]
        try:
            with open(latest_backup, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                if isinstance(data, list):
                    # Restore file
                    self.write_all(collection_name, data)
                    print(f"Successfully recovered {collection_name} from backup {latest_backup.name}")
                    return data
        except Exception:
            pass
        return None

    def clear_cache(self, collection_name: Optional[str] = None):
        with self._lock:
            if collection_name:
                self._memory_cache.pop(collection_name, None)
            else:
                self._memory_cache.clear()
