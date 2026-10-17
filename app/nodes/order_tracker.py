
import re

from app.state import SupportState
from app.tools.order_tool import get_order


def track_order(state: SupportState) -> dict:
    message = state["user_message"]

    # Prefer an order ID mentioned in the current message.
    match = re.search(r"\bORD\d+\b", message, re.IGNORECASE)

    if match:
        order_id = match.group(0).upper()
    else:
        # Reuse the remembered ID for follow-up questions.
        order_id = state.get("order_id")

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

    # Answer delivery-date follow-up questions directly.
    delivery_questions = [
        "when will it arrive",
        "when will it be delivered",
        "delivery date",
        "when can i expect it",
    ]

    if any(word in message.lower() for word in delivery_questions):
        response = (
            f"Your order {order_id} is expected to arrive on "
            f"{order['estimated_delivery']}."
        )
    else:
        response = (
            f"Your order {order['order_id']} for {order['item']} "
            f"is currently {order['status']}. "
            f"Estimated delivery: {order['estimated_delivery']}."
        )

    return {
        "order_id": order_id,
        "response": response,
    }
