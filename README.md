# 🧠 Local AI Tutor (RAG + Ollama)

A **fully local Retrieval-Augmented Generation (RAG) AI Tutor** built using modern LLM infrastructure.
The system retrieves relevant knowledge from a vector database and injects it into prompts before generating responses with a local LLM.

Runs **100% offline** with no external APIs.

---

# ⚙️ Tech Stack

* 🦙 Ollama — Local LLM inference
* 🤖 LLaMA 3 (8B) — Core language model
* 🔍 FAISS — Vector similarity search
* 🧠 Sentence Transformers — Text embeddings
* 🐍 Python — System implementation

---

# 🚀 Features

### 📚 Local Knowledge Retrieval

Documents are embedded and stored inside a FAISS vector database for semantic search.

### 🔎 Cosine Similarity Search

Embeddings are **L2 normalized** and searched using **Inner Product**, making:

```
dot_product == cosine_similarity
```

### 🧠 Context-Aware Responses

Relevant retrieved context is injected into the prompt before generation.

### ⚡ Real-Time Streaming

Responses stream token-by-token from the LLM for a **ChatGPT-like experience**.

### 🧯 Intelligent Fallback

If retrieved context is not relevant (below similarity threshold), the system automatically falls back to **pure LLM generation**.

### 💾 Conversation Logging

All conversations are saved locally for inspection and debugging.

---

# 📂 Project Structure

```
local_ai_tutor/
│
├── app.py              # Main interactive chat loop
├── rag.py              # Retrieval pipeline
├── index.py            # Vector database builder
│
├── documents/
│   └── data.txt        # Knowledge source
│
├── vector_store/
│   ├── index.faiss     # FAISS vector index
│   └── chunks.pkl      # Stored text chunks
│
└── chat_history.txt    # Conversation logs
```

---

# 🔄 System Architecture

The system works in **three main stages**.

---

# 1️⃣ Indexing Phase

Documents are converted into searchable vectors.

Process:

1. Split documents into smaller **semantic chunks**
2. Generate embeddings using:

```
all-MiniLM-L6-v2
```

3. Apply **L2 normalization**

```
v = v / ||v||
```

4. Store vectors inside FAISS using:

```
IndexFlatIP
```

Because vectors are normalized:

```
A · B = cosine similarity
```

This allows extremely **fast semantic retrieval**.

---

# 2️⃣ Retrieval Phase

When a user asks a question:

1. Generate query embedding
2. Normalize query vector
3. Search FAISS for **top-k most similar chunks**
4. Apply similarity threshold
5. If relevant → return context
6. If not → fallback to normal LLM

This prevents **hallucinations from irrelevant context**.

---

# 3️⃣ Generation Phase

The final prompt contains:

```
System Prompt
+
Retrieved Context (if available)
+
Conversation History
+
User Query
```

The LLM then generates the answer **while streaming tokens live**.

---

# 🧮 Cosine Similarity Optimization

Instead of computing cosine similarity directly:

```
cos(A,B) = (A · B) / (||A|| ||B||)
```

We normalize vectors beforehand:

```
A = A / ||A||
B = B / ||B||
```

Which simplifies to:

```
cos(A,B) = A · B
```

This allows FAISS to perform **very fast similarity search** using only dot products.

---

# ⚡ Performance Characteristics

| Component             | Role                            |
| --------------------- | ------------------------------- |
| FAISS                 | Fast vector similarity search   |
| Sentence Transformers | Lightweight embeddings          |
| Ollama                | Local LLM inference             |
| Streaming API         | Token-level response generation |

The pipeline is optimized for **low-latency local inference**.

---

# 🧠 Learning Goals of This Project

This project was built to deeply understand:

* Retrieval-Augmented Generation (RAG)
* Vector search systems
* Embedding models
* Cosine similarity vs L2 distance
* Prompt engineering with context injection
* Local LLM deployment
* AI system architecture

---

# 🧠 Future Improvements

Planned upgrades:

### 🌐 Interface

* Web UI using **FastAPI / Flask**
* Chat interface

### 📚 Retrieval Improvements

* Multi-document ingestion
* Automatic re-indexing
* Metadata filtering

### 🧠 Advanced RAG

* Cross-encoder reranking
* Hybrid search (BM25 + vector)
* Multi-query retrieval

### ⚡ Performance

* True token streaming from Ollama API
* Chunk caching
* Query batching

---

# 🏁 Current Status

| Feature                       | Status |
| ----------------------------- | ------ |
| Local LLM inference           | ✅      |
| FAISS vector database         | ✅      |
| Cosine similarity search      | ✅      |
| Context injection             | ✅      |
| Token streaming               | ✅      |
| Similarity threshold fallback | ✅      |
| Conversation logging          | ✅      |
| Reranking pipeline            | 🚧     |

---

# ⚡ Author

Built as part of deep exploration into:

* Local LLM systems
* Vector databases
* Retrieval architectures
* Production AI pipelines

---
