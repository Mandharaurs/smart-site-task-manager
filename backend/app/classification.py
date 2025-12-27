from app.nlp_utils import extract_entities

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


def classify_task(text: str):
    text_lower = text.lower()

    # ---------- Category ----------
    category = "general"
    for cat, words in CATEGORY_KEYWORDS.items():
        if any(word in text_lower for word in words):
            category = cat
            break

    # ---------- Priority ----------
    priority = "low"
    for pri, words in PRIORITY_KEYWORDS.items():
        if any(word in text_lower for word in words):
            priority = pri
            break

    # ---------- Entity Extraction (SINGLE SOURCE OF TRUTH) ----------
    entities = extract_entities(text)

    return {
        "category": category,
        "priority": priority,
        "extracted_entities": entities,
        "suggested_actions": SUGGESTED_ACTIONS.get(category, [])
    }
