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

def retrieve_context(question, k=5):

    if index is None:
        return None

    q_embedding = model.encode([question])
    q_embedding = q_embedding / np.linalg.norm(q_embedding, axis=1, keepdims=True)

    D, I = index.search(q_embedding, k=k)
    print("Similarity scores:", D)
    # print("Similarity scores:", D)

    threshold = 0.40
    #experimented score

    retrieved_chunks = []

    for score, idx in zip(D[0], I[0]):
        if score >= threshold:
            retrieved_chunks.append(chunks[idx])
            #return all chunks that are above a threshold
            
    if not retrieved_chunks:
        return None

    return "\n\n".join(retrieved_chunks)

