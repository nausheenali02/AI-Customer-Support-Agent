from typing import TypedDict, Optional

class SupportState(TypedDict):
    user_message: str
    intent: Optional[str]
    response: Optional[str]
    order_id: Optional[str]
