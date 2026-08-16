import requests
from app.services.mode_service import get_mode_instruction

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"

def generate_response(
    message: str,
    history: list,
    context: str,
    mode: str
) -> str:
    
    conversation = ""

    for item in history:
        conversation += (
            f"{item['role']}: {item['content']}\n"
        )

    if not conversation:
        conversation = "No previous conversation."

    if not context:
        context = "No relevant documents were retrieved."
    
    mode_instruction = get_mode_instruction(mode)
        
    prompt = f"""
You are Local AI Tutor.

Your current operating mode is STRICTLY defined below:

{mode_instruction}

IMPORTANT:
- Follow the mode instructions above before any other behavior.
- Do not switch modes.
- If Quiz Mode is active, ask questions instead of explaining.
- If Interview Mode is active, behave like an interviewer instead of giving answers.
notepad app\services\ollama_service.py

================ RETRIEVED CONTEXT ================

{context}

================ CONVERSATION HISTORY ================

{conversation}

================ CURRENT USER QUESTION ================

{message}

================ ASSISTANT ANSWER ================
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()
    data = response.json()

    return data["response"]