import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b"

def ask_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]

def chat_loop():
    print("Local AI Tutor (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bye 👋")
            break

        reply = ask_llm(user_input)
        print("\nTutor:", reply, "\n")

if __name__ == "__main__":
    chat_loop()

    