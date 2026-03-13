import requests
import json
import time
from rag import retrieve_context
from index import browse_and_add

# fix the documents 
# rag issue

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b"

#its an AI server based architecture

SYSTEM_PROMPT = """
YOU ARE A CONVERSATIONAL AI TUTOR.
SO LISTEN CLOSELY AND BE ATTENTIVE.
ANSWER WELL AND PRECISE.
Explain concepts clearly.
Use examples.
Keep explanations structured.
If the student seems confused, simplify further."""

conversational_history = []
   
def ask_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt ,
        "stream": True
        #for Streaming Output like GPT Style
    }
    response = requests.post(OLLAMA_URL, json=payload,stream=True)

    full_response =""
    for line in response.iter_lines():
    
        if line:
            decoded = json.loads(line.decode("utf-8"))
            token = decoded.get("response","")
            for char in token:
                print(char, end="", flush=True)
                if char in ".!?":
                    time.sleep(0.2)
                else:
                    time.sleep(0.02)
                
            full_response += token

    return full_response

def save_to_file(user_input,full_reply):
    #saves Converstional History to a File
    with open("chat_history.txt","a",encoding="utf-8") as f:
        f.write(f" User :{user_input} \n")
        f.write(f" Ai :{full_reply} \n\n ")
        

def chat_loop():
    print("Local AI Tutor (type 'exit' to quit)\n")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Bye 👋")
            break

        
        if user_input.strip() == "/upload":
            print("Opening File Browser ")
            browse_and_add()
            continue # Browse and Upload feature 

        # context = retrieve_context(user_input,7)hey

        context = retrieve_context(user_input)

        
        if context is None:
            prompt = f"""
            {SYSTEM_PROMPT}

            Conversation so far:
            {conversational_history}

            User:
            {user_input}

            Tutor:
            """
        else:
            prompt = f"""
            {SYSTEM_PROMPT}

            Use the context below to answer.

            Context:
            {context}

            Conversation unti now:
            {conversational_history}

            User:
            {user_input}

            Tutor:
            """

        print("Tutor : ", end="")
        reply = ask_llm(prompt)
        print("\n \n")
        conversational_history.append(("User",user_input))
        conversational_history.append(("Tutor",reply))

        save_to_file(user_input,reply)

if __name__ == "__main__":
    chat_loop()


# (name == main ?) ->It means:  “Run this code only if this file is being executed directly.”
    # Not when the file is imported into another file.
    