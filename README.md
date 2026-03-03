# 🧠 Local AI Tutor (RAG + Ollama)

A local AI Tutor built using:

- 🦙 Ollama (LLaMA 3 8B)
- 🔍 FAISS (Vector Search)
- 🧠 Sentence Transformers (Embeddings)
- 🐍 Python

This project demonstrates a complete Retrieval-Augmented Generation (RAG) pipeline running fully offline.

---

## 🚀 Features

- Local LLM inference via Ollama
- Document indexing using FAISS
- Cosine similarity based semantic retrieval
- Context injection into prompts
- Streaming output (ChatGPT-like effect)
- Fallback to pure LLM if no RAG available
- Persistent chat history logging

---

## 📂 Project Structure
local_ai_tuto/
│
├── app.py # Main chat loop
├── rag.py # Retrieval logic
├── index.py # Vector store builder
│
├── documents/
│ └── data.txt # Source knowledge file
│
├── vector_store/
│ ├── index.faiss # FAISS index
│ └── chunks.pkl # Stored text chunks
│
└── chat_history.txt # Saved conversations\


---

## 🔄 How It Works

### 1️⃣ Indexing Phase

- Documents are split into chunks
- Embeddings generated using `all-MiniLM-L6-v2`
- Embeddings are L2 normalized
- Stored in FAISS using Inner Product (IP)
- Since vectors are normalized:
  
  dot product = cosine similarity

---

### 2️⃣ Retrieval Phase

When user asks a question:

- Query embedding is generated
- Query is L2 normalized
- FAISS returns top-k matches
- Cosine similarity threshold is applied
- If relevant → context injected
- If not → fallback to normal LLM

---

### 3️⃣ Generation Phase

Prompt structure:

- System instruction
- Retrieved context (if available)
- Conversation history
- User query

LLM streams response in real time.

---

## 🧮 Cosine Similarity Logic

Because embeddings are normalized:
cosine(A, B) = A · B
FAISS uses:
IndexFlatIP(384)
Which directly returns cosine similarity scores.

---

---

## 🧠 Future Improvements

- Web interface (FastAPI / Flask)
- Auto re-index on document update
- Conversation memory windowing
- Token usage control
- Multi-document upload support
- UI formatting with Rich library

---

## 🎯 Learning Goals of This Project

- Understand RAG architecture
- Understand FAISS vector search
- Understand cosine similarity vs L2
- Build production-style local AI system
- Handle fallback logic gracefully

---

## ⚡ Author

Built as part of deep learning into:
- LLM systems
- Vector databases
- Retrieval architectures
- Production AI design

---

## 🏁 Status

✅ Local RAG working  
✅ Cosine threshold implemented  
✅ Streaming output enabled  
🚧 Improvements ongoing  