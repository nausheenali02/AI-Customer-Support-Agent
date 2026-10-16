from langgraph.graph import StateGraph, START, END
from app.nodes.refund_handler import handle_refund
from app.nodes.order_tracker import track_order
from app.state import SupportState
from app.nodes.complaint_handler import handle_complaint
from app.nodes.intent_classifier import classify_intent
from app.graph.router import route_by_intent
from app.nodes.faq_handler import handle_faq


def placeholder_node(state: SupportState) -> dict:
    return {
        "response": f"Request routed to: {state['intent']}"
    }


builder = StateGraph(SupportState)

builder.add_node("classify_intent", classify_intent)

for route in [
    "faq",
    "order_tracking",
    "refund",
    "complaint",
    "human_support",
]:
    if route == "faq":
        builder.add_node(route, handle_faq)
    elif route == "order_tracking":
        builder.add_node(route, track_order)
    elif route == "refund":
        builder.add_node(route, handle_refund)
    elif route == "complaint":
        builder.add_node(route, handle_complaint)
    elif route == "human_support":
        builder.add_node(
          route,
          lambda state: {
            "response": (
                "I'll escalate your request to a human support agent. "
                "Please wait while our support team reviews your concern."
            )
         },
        )
    else:
        builder.add_node(route, placeholder_node)
    


builder.add_edge(START, "classify_intent")

builder.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    {
        "faq": "faq",
        "order_tracking": "order_tracking",
        "refund": "refund",
        "complaint": "complaint",
        "human_support": "human_support",
    },
)

for route in [
    "faq",
    "order_tracking",
    "refund",
    "complaint",
    "human_support",
]:
    builder.add_edge(route, END)

support_graph = builder.compile()
