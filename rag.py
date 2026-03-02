#hThe REtrival and prompt injector with context 
#This is some real rag pipeleine

import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "vector_store/index.faiss"
CHUNKS_PATH = "vector_store/chunks.pkl"

index = None
chunks = None

# Try loading index safely

if not os.path.exists(INDEX_PATH):
    print("No vector store found. Building index...")
    import index  # auto run builder
    
if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
        

def retrieve_context(question):

    if index is None or chunks is None:
        return None

    q_embedding = model.encode([question])
    q_embedding = q_embedding /np.linalg.norm(q_embedding,axis = 1, keepdims=True)
 
    D, I = index.search(q_embedding, k=3)
# D is already cosine similarity.
    cosine = D[0][0]
    threshold = 0.85

    if cosine < threshold:
        return None

    retrieved = "\n\n".join([chunks[i] for i in I[0]])
    return retrieved