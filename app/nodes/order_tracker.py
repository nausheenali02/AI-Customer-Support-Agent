import re

from app.state import SupportState
from app.tools.order_tool import get_order


def track_order(state: SupportState) -> dict:
    message = state["user_message"]

    # Use an order ID already present in the state, if available.
    order_id = state.get("order_id")

    # Otherwise, extract an ID like ORD1001 from the message.
    if not order_id:
        match = re.search(r"\bORD\d+\b", message, re.IGNORECASE)
        order_id = match.group(0).upper() if match else None

    if not order_id:
        return {
            "order_id": None,
            "response": "Please provide your order ID, such as ORD1001.",
        }

    order = get_order(order_id)

    if "error" in order:
        return {
            "order_id": order_id,
            "response": order["error"],
        }

    return {
        "order_id": order_id,
        "response": (
            f"Your order {order['order_id']} for {order['item']} "
            f"is currently {order['status']}. "
            f"Estimated delivery: {order['estimated_delivery']}."
        ),
    }

