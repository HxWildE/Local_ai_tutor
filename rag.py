#hThe REtrival and prompt injector with context 
#This is some real rag pipeleine

import faiss
import pickle
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_store/index.faiss")

# ✅ Load SAME chunks used during indexing
with open("vector_store/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


def query_rag(question):
    q_embedding = model.encode([question])
    D, I = index.search(np.array(q_embedding), k=3)

    retrieved = "\n\n".join([chunks[i] for i in I[0]])

    prompt = f"""
Answer only from the context below.

Context:
{retrieved}

Question:
{question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


print(query_rag("Your question here"))