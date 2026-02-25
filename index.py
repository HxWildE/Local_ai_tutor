import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load syllabus
with open("documents/data.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = text.split("\n\n")

# Create embeddings
embeddings = model.encode(chunks)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index
faiss.write_index(index, "vector_store/index.faiss")

# Save chunks separately
with open("vector_store/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Index + chunks saved.")