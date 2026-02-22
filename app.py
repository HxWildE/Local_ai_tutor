import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b"

SYSTEM_PROMPT = """
YOU ARE A CONCERSATIONAL AI TUTOR.
SO LISTEN CLOSELY AND BE ATTENTIVE.
ANSWER WELL AND PRECISE.
Explain concepts clearly.
Use examples.
Keep explanations structured.
If the student seems confused, simplify further."""

conversational_history = []

def build_prompt(user_input):

    history_text = "" 
    for role,message in conversational_history:
        history_text = f"{role} : {message}"

    new_prompt = f""" 

SYSTEM_PROMPT 

Conversation SO far: {history_text}

User : {user_input}

Tutor: 

"""
    
    return new_prompt
   


def ask_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt ,
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

        new_input = build_prompt(user_input)
        reply = ask_llm(new_input)

        conversational_history.append(("User",user_input))
        conversational_history.append(("Tutor",reply))
        print("\nTutor:", reply, "\n")

if __name__ == "__main__":
    chat_loop()

    