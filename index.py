import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

def build_index():
    os.makedirs("vector_store", exist_ok=True)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load syllabus
    with open("documents/data.txt", "r", encoding="utf-8") as f:
            text = f.read()

    chunks = text.split("\n\n")

    # Create embeddings
    embeddings = model.encode(chunks)
    embeddings = embeddings / np.linalg.norm(embeddings,axis = 1, keepdims=True)

    index = faiss.IndexFlatIP(384)
    # It stores Cosines actually (manualll ypassed 384 dimensions).
    index.add(embeddings)

    # Save index
    faiss.write_index(index, "vector_store/index.faiss")

    # Save chunks separately
    with open("vector_store/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

if __name__ == "__main__":
    build_index()
    
