"""
In-Memory Full-Text Search Indexer.
"""

from typing import Dict, List, Any


class SearchIndexer:
    def __init__(self):
        self.index: Dict[str, List[Dict[str, Any]]] = {}

    def index_document(self, doc_type: str, doc_id: str, title: str, content: str):
        if doc_type not in self.index:
            self.index[doc_type] = []
        self.index[doc_type].append({"id": doc_id, "title": title, "content": content})
