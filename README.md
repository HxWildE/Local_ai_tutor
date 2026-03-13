# 🧠 Local AI Tutor (RAG + Ollama)

A fully local **AI Tutor** built using **Retrieval Augmented Generation (RAG)**.

This project demonstrates how modern AI systems combine **vector search and language models** to produce context-aware answers instead of hallucinating.

The system retrieves relevant documents using **semantic similarity** and feeds them to an **LLM running locally via Ollama**.

---

# 🚀 Features

✔ Fully Local AI Tutor  
✔ Retrieval Augmented Generation (RAG) pipeline  
✔ FAISS Vector Search for fast document retrieval  
✔ Sentence Transformers for semantic embeddings  
✔ Context-aware answers using retrieved knowledge  
✔ Streaming CLI interaction  
✔ Lightweight and runs entirely on local machine  

---

# 🧠 How It Works

The system follows a standard **RAG architecture**:

User Query
│
▼
Sentence Transformer (Embeddings)
│
▼
FAISS Vector Search
│
▼
Top-K Relevant Documents Retrieved
│
▼
Context Injected into Prompt
│
▼
LLM (LLaMA3 via Ollama)
│
▼
Final Response Generated


Instead of relying only on the model's internal knowledge, the LLM receives **relevant external context** before generating a response.

This significantly improves **accuracy and factual grounding**.

---

# ⚙️ Tech Stack

- **Ollama** – running LLaMA3 locally  
- **FAISS** – vector similarity search  
- **Sentence Transformers** – text embeddings  
- **Python** – core implementation  

---

# 📂 Project Structure


local-ai-tutor/

data/ # source documents
embeddings/ # FAISS index files
embed.py # document embedding pipeline
rag.py # retrieval logic
chat.py # CLI chat interface
requirements.txt
README.md


---

# ▶️ Running the Project

Clone the repository:

git clone https://github.com/HxWildE/Local_ai_tutor
cd local-ai-tutor

Install dependencies:
pip install -r requirements.txt

Generate embeddings:
python embed.py

Start the AI tutor:
python chat.py


---

# 📊 Key Concepts Demonstrated

This project demonstrates several important ideas used in modern AI systems:

### Semantic Embeddings
Sentence Transformers convert text into dense vectors that capture meaning.

### Vector Search
FAISS enables efficient similarity search across large collections of embeddings.

### Retrieval Augmented Generation (RAG)
Relevant documents are retrieved and injected into the LLM prompt to improve answer quality.

---

# 🎥 Demo Video

python chat.py
Ask a question:
What is retrieval augmented generation?

[retrieving context...]

AI Tutor:
Retrieval Augmented Generation (RAG) is a technique that combines...

---

# 📚 Learning Outcome

This project was built to understand how **real-world AI systems combine retrieval and generation** to build more reliable assistants.

It provides a simple implementation of the **RAG pipeline running completely locally**.

---

# 🔮 Future Improvements

- Document reranking
- Streaming token output
- Web interface
- Multi-document knowledge bases

---