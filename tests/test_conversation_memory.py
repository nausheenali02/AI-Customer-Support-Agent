
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from app.graph.workflow import support_graph


def test_conversation_history_persists_across_messages():
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    captured_prompts = []

    def mock_invoke(prompt):
        captured_prompts.append(prompt)
        return SimpleNamespace(content="human_support")

    with patch(
        "app.nodes.intent_classifier.llm"
    ) as mock_llm:
        mock_llm.invoke.side_effect = mock_invoke

        first_result = support_graph.invoke(
            {
                "user_message": "I want to speak to a human.",
                "intent": None,
                "response": None,
            },
            config=config,
        )

        second_result = support_graph.invoke(
            {
                "user_message": "Can you help me again?",
                "intent": None,
                "response": None,
            },
            config=config,
        )

    assert len(first_result["conversation_history"]) == 2
    assert len(second_result["conversation_history"]) == 4

    assert (
        "Customer: I want to speak to a human."
        in second_result["conversation_history"]
    )
    assert (
        "Customer: Can you help me again?"
        in second_result["conversation_history"]
    )

    # The classifier should receive the earlier conversation.
    assert "I want to speak to a human." in captured_prompts[1]
    assert "Assistant:" in captured_prompts[1]
