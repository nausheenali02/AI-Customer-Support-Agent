
from unittest.mock import patch

from app.nodes.intent_classifier import classify_intent


def test_classifier_returns_valid_intent():
    mock_result = type("MockResult", (), {"content": "order_tracking"})()

    with patch("app.nodes.intent_classifier.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_result

        result = classify_intent({
            "user_message": "Where is my order ORD1001?",
            "conversation_history": [],
            "order_id": None,
        })

    assert result["intent"] == "order_tracking"
    assert result["order_id"] is None


def test_invalid_classifier_response_defaults_to_faq():
    mock_result = type("MockResult", (), {"content": "something_unknown"})()

    with patch("app.nodes.intent_classifier.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_result

        result = classify_intent({
            "user_message": "Tell me something",
            "conversation_history": [],
            "order_id": None,
        })

    assert result["intent"] == "faq"
