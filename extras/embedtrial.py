from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Perceptron updates weights using learning rate",
    "Backpropagation computes gradients",
    "TCP uses three-way handshake"
]

embeddings = model.encode(sentences)

print(np.dot(embeddings[0], embeddings[1]))  # Similar ML topics
print(np.dot(embeddings[0], embeddings[2]))  # ML vs Networking

# //model embeddings 90mb package loaded and used once 

