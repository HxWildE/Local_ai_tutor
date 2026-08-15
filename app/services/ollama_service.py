import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"


def generate_response(
    message: str,
    history: list,
    context: str
) -> str:

    conversation = ""

    for item in history:
        conversation += f"{item['role']}: {item['content']}\n"

    prompt = f"""
You are a conversational AI tutor.

Use the retrieved context below when it is relevant to the user's question.
If the context does not contain the answer, answer using your general knowledge.
Do not invent information from the context.

Retrieved context:
{context}

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