#hThe REtrival and prompt injector with context 
#This is some real rag pipeleine

import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

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
    q_embedding = q_embedding / np.linalg.norm(q_embedding, axis=1, keepdims=True)

    D, I = index.search(q_embedding, k=7)

    retrieved_chunks = [chunks[i] for i in I[0] if i < len(chunks)]

    # reranking
    pairs = [(question, chunk) for chunk in retrieved_chunks]
    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(retrieved_chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    top_chunks = [chunk for chunk, _ in ranked[:3]]

    return "\n\n".join(top_chunks)
