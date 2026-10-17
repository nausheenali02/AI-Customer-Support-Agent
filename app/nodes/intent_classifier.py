from app.state import SupportState
from app.llm import llm


def classify_intent(state: SupportState) -> dict:
    prompt = f"""
You are an intent classifier for a customer support assistant.

Classify the customer's message into exactly ONE of these intents:

1. faq
   General questions about store policies, delivery rules, refund
   policies, return rules, and how customer support works.

2. order_tracking
   Questions about the status, location, or delivery progress of
   a specific order.

3. refund
   The customer explicitly requests a refund or asks to get their
   money back for an order.

4. complaint
   The customer reports a problem, such as a damaged or incorrect item.

5. human_support
   The customer explicitly asks to speak to a human support agent.

IMPORTANT RULES:
- Asking about the refund policy is faq, NOT refund.
- Asking how many days are allowed for a refund is faq.
- Actually requesting a refund for an order is refund.
- Asking where a specific order is should be order_tracking.
- Reporting a damaged or incorrect item should be complaint.
- Asking to speak to a human should be human_support.

EXAMPLES:
"What is the refund policy?" -> faq
"How many days do I have to return an item?" -> faq
"What is the estimated delivery time?" -> faq
"I want a refund for ORD1003" -> refund
"Can I get my money back for ORD1003?" -> refund
"Where is my order ORD1001?" -> order_tracking
"My order ORD1003 arrived damaged" -> complaint
"I received the wrong product" -> complaint
"I want to speak to a human" -> human_support

Return ONLY the intent name.
Do not include explanations, punctuation, or extra text.

Conversation history:
{chr(10).join(state.get('conversation_history', []))}

Current customer message: {state['user_message']}

Intent:
"""

    result = llm.invoke(prompt)
    content = result.content

    # Handle responses returned as a list of content blocks.
    if isinstance(content, list):
        content = " ".join(
            item["text"] if isinstance(item, dict) and "text" in item
            else str(item)
            for item in content
        )

    intent = content.strip().lower()

    # Keep only supported intent values.
    valid_intents = {
        "faq",
        "order_tracking",
        "refund",
        "complaint",
        "human_support",
    }

    if intent not in valid_intents:
        intent = "faq"

    return {
    "intent": intent,
    "order_id": state.get("order_id"),
   }
