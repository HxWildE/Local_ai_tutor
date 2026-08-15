import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"


def generate_response(message: str, history: list) -> str:

    conversation = ""

    for item in history:
        conversation += f"{item['role']}: {item['content']}\n"

    prompt = f"""
You are a conversational AI tutor.

Conversation history:
{conversation}

User:
{message}

Assistant:
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