from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from app.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import generate_response, generate_response_stream
from app.services.memory_service import get_history, add_message
from app.services.rag_service import rag_service
from app.services.tool_service import detect_tool, execute_tool

app = FastAPI(
    title="Local AI Tutor API",
    description="Local AI Tutor featuring LLM inference, RAG, tool layer simulation, and streaming.",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import threading
import requests
from app.services.ollama_service import MODEL_NAME, OLLAMA_URL

@app.get("/api/warmup")
def warmup():
    def ping_ollama():
        try:
            # Just send a tiny prompt to ensure model is loaded in VRAM
            requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": "hi", "stream": False}, timeout=10)
        except:
            pass
    threading.Thread(target=ping_ollama).start()
    return {"status": "warming up"}

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "Local AI Tutor API",
        "rag_chunks": len(rag_service.chunks) if rag_service.chunks else 0
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    history = get_history(request.conversation_id)

    if request.use_rag:
        tool_name, tool_input = detect_tool(request.message)
        if tool_name:
            tool_execution = execute_tool(tool_name, tool_input)
            tool_result = tool_execution.get("result", {})
            if tool_name == "retrieval":
                context = tool_result.get("context", "") if isinstance(tool_result, dict) else str(tool_result)
            elif tool_name == "summarizer":
                context = f"Summarizer Tool Output: {tool_result.get('summary', '')}" if isinstance(tool_result, dict) else str(tool_result)
            else: # calculator
                context = f"Calculator Tool Output: {tool_result}"
        else:
            context = rag_service.retrieve_context(request.message)
    else:
        context = ""

    response = generate_response(
        request.message,
        history,
        context,
        request.mode
    )

    add_message(request.conversation_id, "user", request.message)
    add_message(request.conversation_id, "assistant", response)

    return ChatResponse(response=response)

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    history = get_history(request.conversation_id)

    if request.use_rag:
        tool_name, tool_input = detect_tool(request.message)
        if tool_name:
            tool_execution = execute_tool(tool_name, tool_input)
            tool_result = tool_execution.get("result", {})
            if tool_name == "retrieval":
                context = tool_result.get("context", "") if isinstance(tool_result, dict) else str(tool_result)
            elif tool_name == "summarizer":
                context = f"Summarizer Tool Output: {tool_result.get('summary', '')}" if isinstance(tool_result, dict) else str(tool_result)
            else: # calculator
                context = f"Calculator Tool Result: {tool_result}"
        else:
            context = rag_service.retrieve_context(request.message)
    else:
        context = ""

    # Record user message
    add_message(request.conversation_id, "user", request.message)

    def stream_generator():
        accumulated_text = ""
        for token in generate_response_stream(request.message, history, context, request.mode):
            accumulated_text += token
            yield token
        # Record complete assistant response once finished streaming
        add_message(request.conversation_id, "assistant", accumulated_text)

    return StreamingResponse(stream_generator(), media_type="text/plain")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        chunks_added, total_chunks = rag_service.add_document(file.filename, content)
        return {
            "status": "success",
            "message": f"Successfully indexed '{file.filename}'.",
            "chunks_added": chunks_added,
            "total_chunks": total_chunks
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Mount static web interface
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
