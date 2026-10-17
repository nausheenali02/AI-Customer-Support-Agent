
from app.nodes.order_tracker import track_order


def test_valid_order_returns_correct_details():
    result = track_order({
        "user_message": "Where is my order ORD1002?",
        "order_id": None,
    })

    assert result["order_id"] == "ORD1002"
    assert "Laptop Stand" in result["response"]
    assert "Processing" in result["response"]

def test_invalid_order_returns_error():
    result = track_order({
        "user_message": "Where is my order ORD9999?",
        "order_id": None,
    })

    assert result["order_id"] == "ORD9999"
    assert "Order not found" in result["response"]


def test_delivery_followup_returns_expected_date():
    result = track_order({
        "user_message": "When will it arrive?",
        "order_id": "ORD1002",
    })

    assert "2026-10-20" in result["response"]
