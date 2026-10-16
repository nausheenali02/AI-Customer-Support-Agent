from app.state import SupportState

def route_by_intent(state: SupportState) -> str:
    intent = state.get("intent")

    if intent == "order_tracking":
        return "order_tracking"

    if intent == "refund":
        return "refund"

    if intent == "complaint":
        return "complaint"

    if intent == "human_support":
        return "human_support"

    return "faq"
