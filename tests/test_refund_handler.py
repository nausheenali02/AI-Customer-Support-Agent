
from app.nodes.refund_handler import handle_refund


def test_missing_order_id_asks_user_for_order_id():
    result = handle_refund({
        "user_message": "Can I get a refund?",
        "order_id": None,
    })

    assert "Please provide your order ID" in result["response"]

from datetime import date, timedelta
from unittest.mock import patch


def test_delivered_order_within_7_days_is_eligible():
    delivery_date = date.today() - timedelta(days=3)

    with patch(
        "app.nodes.refund_handler.get_order",
        return_value={
            "order_id": "ORD1003",
            "item": "Keyboard",
            "status": "Delivered",
            "estimated_delivery": delivery_date.isoformat(),
        },
    ):
        result = handle_refund({
            "user_message": "Can I get a refund for ORD1003?",
            "order_id": None,
        })

    assert "eligible to request a refund" in result["response"]


def test_delivered_order_outside_7_days_is_not_eligible():
    delivery_date = date.today() - timedelta(days=10)

    with patch(
        "app.nodes.refund_handler.get_order",
        return_value={
            "order_id": "ORD1003",
            "item": "Keyboard",
            "status": "Delivered",
            "estimated_delivery": delivery_date.isoformat(),
        },
    ):
        result = handle_refund({
            "user_message": "Can I get a refund for ORD1003?",
            "order_id": None,
        })

    assert "outside the 7-day refund window" in result["response"]
