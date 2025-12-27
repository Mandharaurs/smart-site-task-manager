from app.classification import classify_task


def test_high_priority_scheduling_unit():
    result = classify_task("urgent meeting with manager today")

    assert result["priority"] == "high"
    assert result["category"] == "scheduling"
    assert "manager" in result["extracted_entities"]["people"]


def test_finance_medium_priority_unit():
    result = classify_task("important invoice payment this week")

    assert result["category"] == "finance"
    assert result["priority"] == "medium"


def test_general_low_priority_unit():
    result = classify_task("read documentation")

    assert result["category"] == "general"
    assert result["priority"] == "low"
