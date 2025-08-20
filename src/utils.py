import re
from datetime import datetime
from typing import Optional

LEVELS = [
    "Corporate","School","College/University","Club/Academy",
    "District","State","Zonal/Regional","National","International"
]

def parse_date(s: str) -> str:
    """Parse many human date formats to ISO YYYY-MM-DD. Return original if fail."""
    if not s:
        return s
    for fmt in ("%Y-%m-%d","%d-%m-%Y","%d/%m/%Y","%b %d, %Y","%B %d, %Y","%Y/%m/%d"):
        try:
            return datetime.strptime(s.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return s

def infer_level(text: str) -> Optional[str]:
    text_low = (text or "").lower()
    for lvl in LEVELS:
        if lvl.lower().split('/')[0] in text_low:
            return lvl
    # naive fallbacks
    if "world" in text_low or "international" in text_low:
        return "International"
    if "state" in text_low:
        return "State"
    if "district" in text_low:
        return "District"
    return None
