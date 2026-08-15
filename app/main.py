from fastapi import FastAPI

from app.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import generate_response
from app.services.memory_service import get_history, add_message

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Local AI Tutor API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    history = get_history(request.conversation_id)

    response = generate_response(
        request.message,
        history
    )

    add_message(
        request.conversation_id,
        "user",
        request.message
    )

    add_message(
        request.conversation_id,
        "assistant",
        response
    )

    return ChatResponse(response=response)