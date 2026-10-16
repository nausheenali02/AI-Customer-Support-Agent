from app.state import SupportState
from app.rag.faq_chain import answer_faq


def handle_faq(state: SupportState) -> dict:
    question = state["user_message"]
    response = answer_faq(question)

    return {"response": response}
