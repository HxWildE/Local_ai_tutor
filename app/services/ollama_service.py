import json
from typing import Generator
import requests
from app.services.mode_service import get_mode_instruction

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"

def _build_prompt(message: str, history: list, context: str, mode: str) -> str:
    conversation = ""
    for item in history:
        conversation += f"{item['role']}: {item['content']}\n"

    if not conversation:
        conversation = "No previous conversation."

    if not context:
        context = "No relevant documents were retrieved."

    mode_instruction = get_mode_instruction(mode)

    return f"""
You are Local AI Tutor.

Your current operating mode is STRICTLY defined below:

{mode_instruction}

IMPORTANT:
- Follow the mode instructions above before any other behavior.
- Do not switch modes.
- If Quiz Mode is active, ask questions instead of explaining.
- If Interview Mode is active, behave like an interviewer instead of giving answers.

================ RETRIEVED CONTEXT ================

{context}

================ CONVERSATION HISTORY ================

{conversation}

================ CURRENT USER QUESTION ================

{message}

================ ASSISTANT ANSWER ================
"""

def generate_response(
    message: str,
    history: list,
    context: str,
    mode: str
) -> str:
    prompt = _build_prompt(message, history, context, mode)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        return data["response"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with local LLM (Ollama): {str(e)}"

def generate_response_stream(
    message: str,
    history: list,
    context: str,
    mode: str
) -> Generator[str, None, None]:
    """
    Streams generated tokens line-by-line from Ollama endpoint.
    """
    prompt = _build_prompt(message, history, context, mode)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True
    }

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    data = json.loads(decoded)
                    token = data.get("response", "")
                    if token:
                        yield token
                    if data.get("done", False):
                        break
    except requests.exceptions.RequestException as e:
        yield f" Error connecting to Ollama service: {str(e)}"