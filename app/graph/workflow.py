from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from app.nodes.refund_handler import handle_refund
from app.nodes.order_tracker import track_order
from app.state import SupportState
from app.nodes.complaint_handler import handle_complaint
from app.nodes.intent_classifier import classify_intent
from app.graph.router import route_by_intent
from app.nodes.faq_handler import handle_faq


def save_conversation(state: SupportState) -> dict:
    message = f"Customer: {state['user_message']}"
    response = f"Assistant: {state.get('response', '')}"

    return {
        "conversation_history": [message, response]
    }


builder = StateGraph(SupportState)

builder.add_node("classify_intent", classify_intent)
builder.add_node("save_conversation", save_conversation)

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

    builder.add_edge(route, "save_conversation")

builder.add_edge("save_conversation", END)


memory = MemorySaver()
support_graph = builder.compile(checkpointer=memory)