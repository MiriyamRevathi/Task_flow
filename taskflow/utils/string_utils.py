"""
String Formatting & Slugification Utilities.
"""

import re
import unicodedata


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def truncate(text: str, max_len: int = 100, suffix: str = "...") -> str:
    if not text or len(text) <= max_len:
        return text or ""
    return text[: max_len - len(suffix)].strip() + suffix


def generate_project_key(name: str) -> str:
    words = re.findall(r"\w+", name.upper())
    if not words:
        return "PROJ"
    if len(words) == 1:
        return words[0][:4]
    return "".join(w[0] for w in words[:4])
