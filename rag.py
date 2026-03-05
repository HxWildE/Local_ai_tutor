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

def load_vector_store():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        from index import build_index
        build_index()

    index = faiss.read_index(INDEX_PATH)
    
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
            
    return index,chunks 

# used the function here
index, chunks = load_vector_store()

def retrieve_context(question):

    if index is None:
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