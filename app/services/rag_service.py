import os
import pickle
from typing import List, Optional, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from pypdf import PdfReader

INDEX_PATH = "vector_store/index.faiss"
CHUNKS_PATH = "vector_store/chunks.pkl"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

RETRIEVAL_K = 7
FINAL_K = 2

class RAGService:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.reranker = CrossEncoder(RERANKER_MODEL_NAME)
        self.index: Optional[faiss.IndexFlatIP] = None
        self.chunks: List[str] = []
        self._load_or_initialize_vector_store()

    def _load_or_initialize_vector_store(self):
        os.makedirs("vector_store", exist_ok=True)
        if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(CHUNKS_PATH, "rb") as f:
                self.chunks = pickle.load(f)
        else:
            # Initialize empty FAISS Index with 384 dimensions (all-MiniLM-L6-v2 output dimension)
            self.index = faiss.IndexFlatIP(384)
            self.chunks = []
            self._save_vector_store()

    def _save_vector_store(self):
        os.makedirs("vector_store", exist_ok=True)
        faiss.write_index(self.index, INDEX_PATH)
        with open(CHUNKS_PATH, "wb") as f:
            pickle.dump(self.chunks, f)

    def retrieve_context(self, question: str) -> str:
        if self.index is None or self.index.ntotal == 0 or not self.chunks:
            return ""

        query_embedding = self.embedding_model.encode([question])
        query_embedding = (
            query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        )

        k = min(RETRIEVAL_K, self.index.ntotal)
        distances, indices = self.index.search(query_embedding, k)

        retrieved_chunks = [
            self.chunks[i]
            for i in indices[0]
            if 0 <= i < len(self.chunks)
        ]

        if not retrieved_chunks:
            return ""

        pairs = [(question, chunk) for chunk in retrieved_chunks]
        scores = self.reranker.predict(pairs)

        ranked = sorted(
            zip(retrieved_chunks, scores),
            key=lambda item: item[1],
            reverse=True
        )

        top_chunks = [chunk for chunk, _ in ranked[:FINAL_K]]
        return "\n\n".join(top_chunks)

    def extract_text_from_file(self, filename: str, content_bytes: bytes) -> str:
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            import io
            reader = PdfReader(io.BytesIO(content_bytes))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        else: # .txt, .md, code files
            return content_bytes.decode("utf-8", errors="ignore")

    def add_document(self, filename: str, content_bytes: bytes) -> Tuple[int, int]:
        """
        Extracts text, splits into chunks, computes normalized embeddings,
        updates FAISS vector index, and saves state to disk.
        Returns (num_chunks_added, total_chunks_in_store).
        """
        text = self.extract_text_from_file(filename, content_bytes)
        if not text or not text.strip():
            raise ValueError(f"No extractable text content found in {filename}")

        # Simple semantic paragraph chunking
        raw_chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        if not raw_chunks:
            raw_chunks = [text.strip()]

        embeddings = self.embedding_model.encode(raw_chunks)
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

        # Add to FAISS index
        self.index.add(embeddings)
        self.chunks.extend(raw_chunks)

        # Persist updated vector store
        self._save_vector_store()

        return len(raw_chunks), len(self.chunks)

rag_service = RAGService()