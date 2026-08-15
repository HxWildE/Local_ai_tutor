from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import generate_response

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Local AI Tutor API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = generate_response(request.message)

    return ChatResponse(response=response)