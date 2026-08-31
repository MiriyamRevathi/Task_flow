"""
Data Export Service (CSV, JSON, HTML).
"""

import json
import csv
import io
from typing import List, Dict, Any


class ExportService:
    @staticmethod
    def export_to_csv(data: List[Dict[str, Any]]) -> str:
        if not data:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(data[0].keys()))
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return output.getvalue()

    @staticmethod
    def export_to_json(data: List[Dict[str, Any]]) -> str:
        return json.dumps(data, indent=2)
