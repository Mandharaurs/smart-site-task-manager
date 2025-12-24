import re

CATEGORY_KEYWORDS = {
    "scheduling": ["meeting", "schedule", "call", "appointment", "deadline"],
    "finance": ["payment", "invoice", "bill", "budget", "cost", "expense"],
    "technical": ["bug", "fix", "error", "install", "repair", "maintain"],
    "safety": ["safety", "hazard", "inspection", "compliance", "ppe"]
}

PRIORITY_KEYWORDS = {
    "high": ["urgent", "asap", "immediately", "today", "critical", "emergency"],
    "medium": ["soon", "this week", "important"]
}

SUGGESTED_ACTIONS = {
    "scheduling": ["Block calendar", "Send invite", "Prepare agenda", "Set reminder"],
    "finance": ["Check budget", "Get approval", "Generate invoice", "Update records"],
    "technical": ["Diagnose issue", "Check resources", "Assign technician", "Document fix"],
    "safety": ["Conduct inspection", "File report", "Notify supervisor", "Update checklist"],
    "general": ["Review task", "Plan next steps"]
}

DATE_KEYWORDS = [
    "today", "tomorrow",
    "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday"
]

def classify_task(text: str):
    text_lower = text.lower()

    # Category
    category = "general"
    for cat, words in CATEGORY_KEYWORDS.items():
        if any(word in text_lower for word in words):
            category = cat
            break

    # Priority
    priority = "low"
    for pri, words in PRIORITY_KEYWORDS.items():
        if any(word in text_lower for word in words):
            priority = pri
            break

    # People extraction
    people_pattern = r'(?:with|by|assign to)\s+([A-Za-z]+)'
    people = re.findall(people_pattern, text_lower)

    people = [p.strip() for match in people for p in match.split(",")]

    # Dates extraction
    dates = [word for word in DATE_KEYWORDS if word in text_lower]

    # Actions extraction (optional, can add more verbs)
    actions = re.findall(r'\b(schedule|call|review|approve|fix|check|update|conduct)\b', text_lower)

    entities = {
        "people": people,
        "datetime": dates,
        "actions": actions
    }

    return {
        "category": category,
        "priority": priority,
        "extracted_entities": entities,
        "suggested_actions": SUGGESTED_ACTIONS.get(category, [])
    }
