import re

from app.state import SupportState
from app.tools.order_tool import create_complaint_ticket


def handle_complaint(state: SupportState) -> dict:
    message = state["user_message"]

    order_id = state.get("order_id")

    if not order_id:
        match = re.search(r"\bORD\d+\b", message, re.IGNORECASE)
        order_id = match.group(0).upper() if match else None

    ticket = create_complaint_ticket(message, order_id)

    if "error" in ticket:
        return {"response": ticket["error"]}

    return {
        "order_id": order_id,
        "response": (
            f"Your complaint has been registered successfully. "
            f"Your ticket ID is #{ticket['ticket_id']}, "
            f"and its current status is {ticket['status']}."
        ),
    }
