import sqlite3
from unittest.mock import patch

from app.tools import order_tool
from app.tools.order_tool import create_complaint_ticket


def test_complaint_ticket_is_created_successfully():
    connection = sqlite3.connect(":memory:")
    connection.execute("""
        CREATE TABLE complaint_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            customer_message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL
        )
    """)

    with patch.object(order_tool.sqlite3, "connect", return_value=connection):
        result = create_complaint_ticket(
            customer_message="I received a damaged product.",
            order_id="ORD1001",
        )

    assert "ticket_id" in result
    assert result["order_id"] == "ORD1001"
    assert result["status"] == "Open"
    assert "registered successfully" in result["message"]

    connection.close()

def test_empty_complaint_returns_error():
    result = create_complaint_ticket(
        customer_message="   ",
        order_id="ORD1001",
    )

    assert result["error"] == "Please describe your complaint."
