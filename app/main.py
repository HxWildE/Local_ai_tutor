from fastapi import FastAPI

from app.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import generate_response
from app.services.memory_service import get_history, add_message
from app.services.rag_service import rag_service

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Local AI Tutor API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    history = get_history(request.conversation_id)
    if request.use_rag:
        context = rag_service.retrieve_context(
        request.message
    )
    else:
        context = ""

    response = generate_response(
        request.message,
        history,
        context,
        request.mode
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