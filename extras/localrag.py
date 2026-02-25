
#hardcoded to refer for Embedding 

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from ollama import Client

# ----------------------------
# 1. Load embedding model
# ----------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# 2. Your syllabus content
# ----------------------------
documents = [
    "Perceptron updates weights using learning rate",
    "Backpropagation computes gradients using chain rule",
    "TCP uses three way handshake for connection setup",
    "Gradient descent minimizes loss function"
]

# ----------------------------
# 3. Convert text to embeddings
# ----------------------------
doc_embeddings = embed_model.encode(documents)

# ----------------------------
# 4. Create FAISS index
# ----------------------------
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(doc_embeddings))

print("Index built with", index.ntotal, "documents")

# ----------------------------
# 5. Ask a question
# ----------------------------
query = "How does perceptron learn?"

query_embedding = embed_model.encode([query])

# ----------------------------
# 6. Search top 2 similar chunks
# ----------------------------
k = 2
distances, indices = index.search(np.array(query_embedding), k)

print("Relevant chunks:")
retrieved_chunks = []

for idx in indices[0]:
    chunk = documents[idx]
    retrieved_chunks.append(chunk)
    print("-", chunk)

# ----------------------------
# 7. Build prompt
# ----------------------------
context = "\n".join(retrieved_chunks)

prompt = f"""
Answer only from the syllabus below.

Syllabus:
{context}

Question:
{query}
"""

# ----------------------------
# 8. Send to local LLM
# ----------------------------
client = Client()

response = client.chat(
    model="llama3",
    messages=[{"role": "user", "content": prompt}]
)

print("\nLLM Answer:\n")
print(response["message"]["content"])