from pydantic import BaseModel
from typing import Literal


class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    mode: Literal["tutor", "quiz", "interview"]
    use_rag: bool = False


class ChatResponse(BaseModel):
    response: str