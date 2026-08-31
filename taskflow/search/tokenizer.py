"""
Search Tokenizer.
"""

import re


def tokenize(text: str) -> List[str]:
    if not text:
        return []
    return re.findall(r"\w+", text.lower())
