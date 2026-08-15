from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.ollama_client import OllamaClient


app = FastAPI(
    title="Local AI Tutor",
    version="2.0.0",
    description="Local AI tutoring backend powered by Ollama",
)

ollama = OllamaClient(
    base_url=OLLAMA_BASE_URL,
    model=OLLAMA_MODEL,
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model": OLLAMA_MODEL,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = ollama.generate(request.message)
        return ChatResponse(response=response)

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"LLM service error: {str(e)}",
        )