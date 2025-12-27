import re
from datetime import datetime

ACTION_VERBS = [
    "schedule", "call", "meet", "fix", "install", "repair",
    "pay", "review", "submit", "prepare", "inspect"
]

DATE_PATTERNS = [
    r"\btoday\b",
    r"\btomorrow\b",
    r"\bnext week\b",
    r"\bthis week\b",
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",   # 12/25/2025
]

PERSON_PATTERNS = [
    r"with ([A-Z][a-z]+)",
    r"by ([A-Z][a-z]+)",
    r"assign to ([A-Z][a-z]+)"
]

LOCATION_PATTERNS = [
    r"\bat ([A-Za-z\s]+)",
    r"\bin ([A-Za-z\s]+ office)",
]


def extract_entities(text: str):
    text_lower = text.lower()

    # ---------- Actions ----------
    actions = [v for v in ACTION_VERBS if v in text_lower]

    # ---------- Dates ----------
    dates = []
    for pattern in DATE_PATTERNS:
        dates.extend(re.findall(pattern, text_lower))

    # ---------- People ----------
    people = []
    person_patterns = [
        r"with\s+([a-zA-Z]+)",
        r"by\s+([a-zA-Z]+)",
        r"assign(?:ed)?\s+to\s+([a-zA-Z]+)"
    ]

    for pattern in person_patterns:
        people.extend(re.findall(pattern, text_lower))

    # ---------- Locations ----------
    locations = []
    location_patterns = [
        r"\bat\s+([a-zA-Z]+)",
        r"\bin\s+([a-zA-Z]+\s+office)"
    ]

    for pattern in location_patterns:
        locations.extend(re.findall(pattern, text_lower))

    return {
        "people": list(set(people)),
        "dates": list(set(dates)),
        "locations": list(set(locations)),
        "actions": list(set(actions)),
    }
