import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def generate_response(message: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": message,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()

    return data["response"]