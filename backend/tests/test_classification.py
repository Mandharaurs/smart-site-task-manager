import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_high_priority_scheduling():
    res = client.post(
        "/classify",
        json={"text": "urgent meeting with manager today"}
    )
    data = res.json()["analysis"]
    assert data["priority"] == "high"
    assert data["category"] == "scheduling"
    assert "manager" in data["extracted_entities"]["people"]


def test_finance_medium_priority():
    res = client.post(
        "/classify",
        json={"text": "important invoice payment this week"}
    )
    data = res.json()["analysis"]
    assert data["category"] == "finance"
    assert data["priority"] == "medium"


def test_general_low_priority():
    res = client.post(
        "/classify",
        json={"text": "read documentation"}
    )
    data = res.json()["analysis"]
    assert data["priority"] == "low"
