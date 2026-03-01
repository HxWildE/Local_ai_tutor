#hThe REtrival and prompt injector with context 
#This is some real rag pipeleine
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_store/index.faiss")

with open("vector_store/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


def retrieve_context(question):
    q_embedding = model.encode([question])
    D, I = index.search(np.array(q_embedding), k=3)

    threshold = 1.2

    if D[0][0] > threshold:
        return None

    retrieved = "\n\n".join([chunks[i] for i in I[0]])
    return retrieved