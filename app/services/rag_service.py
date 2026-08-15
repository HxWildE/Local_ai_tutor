import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder


INDEX_PATH = "vector_store/index.faiss"
CHUNKS_PATH = "vector_store/chunks.pkl"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

RETRIEVAL_K = 7
FINAL_K = 3


class RAGService:

    def __init__(self):
        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )

        self.reranker = CrossEncoder(
            RERANKER_MODEL_NAME
        )

        self.index = None
        self.chunks = None

        self._load_vector_store()

    def _load_vector_store(self):

        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(
                f"FAISS index not found: {INDEX_PATH}"
            )

        if not os.path.exists(CHUNKS_PATH):
            raise FileNotFoundError(
                f"Chunks file not found: {CHUNKS_PATH}"
            )

        self.index = faiss.read_index(INDEX_PATH)

        with open(CHUNKS_PATH, "rb") as f:
            self.chunks = pickle.load(f)

    def retrieve_context(self, question: str) -> str:

        query_embedding = self.embedding_model.encode([question])

        
        query_embedding = (
            query_embedding
            / np.linalg.norm(
                query_embedding,
                axis=1,
                keepdims=True
            )
        )

        distances, indices = self.index.search(
            query_embedding,
            RETRIEVAL_K
        )

        retrieved_chunks = [
            self.chunks[i]
            for i in indices[0]
            if 0 <= i < len(self.chunks)
        ]

        if not retrieved_chunks:
            return ""

        pairs = [
            (question, chunk)
            for chunk in retrieved_chunks
        ]

        scores = self.reranker.predict(pairs)

        ranked = sorted(
            zip(retrieved_chunks, scores),
            key=lambda item: item[1],
            reverse=True
        )

        top_chunks = [
            chunk
            for chunk, _ in ranked[:FINAL_K]
        ]

        return "\n\n".join(top_chunks)


rag_service = RAGService()