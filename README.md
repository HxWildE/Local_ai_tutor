# 🧠 Local AI Tutor (Llama 3 - Ollama)

A fully local AI tutor built using Python and Ollama.

No internet required after model download.

---

## 🚀 Version 1 - Basic Chat Loop

- Connected Python app to Ollama local API
- Model: llama3:8b
- Simple request → response flow

### Architecture

User Input  
↓  
Python App  
↓  
Ollama Local Server  
↓  
Llama3 Model  
↓  
Response  

---

## 🚀 Version 2 - Tutor Personality + Memory

- Added system prompt
- Added conversation history
- Model now behaves like structured tutor
- Remembers previous conversation

### Prompt Structure

System Instructions  
+  
Conversation History  
+  
Current User Input  

---

## 🛠 How to Run

1. Install Ollama
2. Pull model:
   ```bash
   ollama pull llama3:8b