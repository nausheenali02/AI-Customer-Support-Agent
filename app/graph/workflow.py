
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import SupportState
from app.nodes.intent_classifier import classify_intent
from app.nodes.faq_handler import handle_faq
from app.nodes.order_tracker import track_order
from app.nodes.refund_handler import handle_refund
from app.nodes.complaint_handler import handle_complaint
from app.graph.router import route_by_intent


def handle_human_support(state: SupportState) -> dict:
    return {
        "response": (
            "I'll escalate your request to a human support agent. "
            "Please wait while our support team reviews your concern."
        )
    }


def save_conversation(state: SupportState) -> dict:
    return {
        "conversation_history": [
            f"Customer: {state['user_message']}",
            f"Assistant: {state.get('response', '')}",
        ]
    }


handlers = {
    "faq": handle_faq,
    "order_tracking": track_order,
    "refund": handle_refund,
    "complaint": handle_complaint,
    "human_support": handle_human_support,
}

builder = StateGraph(SupportState)

builder.add_node("classify_intent", classify_intent)
builder.add_node("save_conversation", save_conversation)

for route, handler in handlers.items():
    builder.add_node(route, handler)

builder.add_edge(START, "classify_intent")

builder.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    {route: route for route in handlers},
)

for route in handlers:
    builder.add_edge(route, "save_conversation")

builder.add_edge("save_conversation", END)

memory = MemorySaver()
support_graph = builder.compile(checkpointer=memory)
