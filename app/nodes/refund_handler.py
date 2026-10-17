
import re
from datetime import date, datetime

from app.state import SupportState
from app.tools.order_tool import get_order


def handle_refund(state: SupportState) -> dict:
    message = state["user_message"]

    # Prefer the order ID mentioned in the current message.
    match = re.search(r"\bORD\d+\b", message, re.IGNORECASE)

    if match:
        order_id = match.group(0).upper()
    else:
        # Use the remembered order ID for follow-up messages.
        order_id = state.get("order_id")

    if not order_id:
        return {
            "response": "Please provide your order ID, such as ORD1001."
        }

    order = get_order(order_id)

    if "error" in order:
        return {"response": order["error"]}

    if order["status"].lower() != "delivered":
        return {
            "order_id": order_id,
            "response": (
                f"Your order is currently {order['status']}. "
                "Please contact support to check available cancellation options."
            ),
        }

    delivery_date = datetime.strptime(
        order["estimated_delivery"], "%Y-%m-%d"
    ).date()

    days_since_delivery = (date.today() - delivery_date).days

    if 0 <= days_since_delivery <= 7:
        return {
            "order_id": order_id,
            "response": (
                f"Your order {order_id} was delivered "
                f"{days_since_delivery} days ago and is eligible "
                "to request a refund. I'll guide you through the next steps."
            ),
        }

    return {
        "order_id": order_id,
        "response": (
            "This order is outside the 7-day refund window. "
            "Please contact human support if you believe an exception applies."
        ),
    }
