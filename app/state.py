import operator
from typing import Annotated, TypedDict, Optional

class SupportState(TypedDict):
    user_message: str
    intent: Optional[str]
    response: Optional[str]
    order_id: Optional[str]
    conversation_history: Annotated[list[str], operator.add]
