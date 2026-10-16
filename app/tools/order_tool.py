import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path(__file__).resolve().parents[2] / "data" / "orders.db"


def init_order_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaint_tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT,
                customer_message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                created_at TEXT NOT NULL
            )
        """)

        conn.executemany("""
            INSERT OR IGNORE INTO orders
            (order_id, customer_name, item, status, estimated_delivery)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("ORD1001", "Aisha", "Wireless Headphones", "Shipped", "2026-10-18"),
            ("ORD1002", "Rahul", "Laptop Stand", "Processing", "2026-10-20"),
            ("ORD1003", "Sara", "Keyboard", "Delivered", "2026-10-14"),
        ])


def get_order(order_id: str) -> dict:
    if not order_id or not order_id.strip():
        return {"error": "Please provide your order ID."}

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            "SELECT * FROM orders WHERE order_id = ?",
            (order_id.strip().upper(),),
        ).fetchone()

    if row is None:
        return {"error": "Order not found. Please check your order ID."}

    return dict(row)


def create_complaint_ticket(customer_message: str, order_id: str = None) -> dict:
    if not customer_message or not customer_message.strip():
        return {"error": "Please describe your complaint."}

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO complaint_tickets
            (order_id, customer_message, created_at)
            VALUES (?, ?, ?)
            """,
            (
                order_id.strip().upper() if order_id else None,
                customer_message.strip(),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        ticket_id = cursor.lastrowid

    return {
        "ticket_id": ticket_id,
        "order_id": order_id.strip().upper() if order_id else None,
        "status": "Open",
        "message": "Your complaint has been registered successfully.",
    }


if __name__ == "__main__":
    init_order_db()
    print("Order database initialized successfully.")
