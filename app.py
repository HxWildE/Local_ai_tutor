import requests
import json
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b"

#its an AI server based architecture

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

        new_input = build_prompt(user_input)
        print("Tutor : ",end="")
        
        reply = ask_llm(new_input)

        conversational_history.append(("User",user_input))
        conversational_history.append(("Tutor",reply))

        save_to_file(user_input,reply)

if __name__ == "__main__":
    chat_loop()

    