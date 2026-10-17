from app.graph.router import route_by_intent

def test_order_tracking_route():
    assert route_by_intent({"intent": "order_tracking"}) == "order_tracking"


def test_refund_route():
    assert route_by_intent({"intent": "refund"}) == "refund"


def test_complaint_route():
    assert route_by_intent({"intent": "complaint"}) == "complaint"


def test_human_support_route():
    assert route_by_intent({"intent": "human_support"}) == "human_support"


def test_faq_route():
    assert route_by_intent({"intent": "faq"}) == "faq"


def test_unknown_intent_defaults_to_faq():
    assert route_by_intent({"intent": "unknown"}) == "faq"


def test_missing_intent_defaults_to_faq():
    assert route_by_intent({}) == "faq"
