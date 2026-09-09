# vector_store.py
# A minimal, dependency-light vector store using NumPy for similarity search.
# In Chapter 6 we'll replace this with a proper vector database (Chroma),
# but building it by hand once is the best way to understand what that
# database is actually doing for you.

import numpy as np
import ollama

EMBED_MODEL = "nomic-embed-text"


def embed_text(text: str) -> np.ndarray:
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return np.array(response["embeddings"][0], dtype=np.float32)


class SimpleVectorStore:
    def __init__(self):
        self.chunks: list[str] = []
        self.vectors: list[np.ndarray] = []

    def add(self, chunk: str):
        vector = embed_text(chunk)
        self.chunks.append(chunk)
        self.vectors.append(vector)

    def add_many(self, chunks: list[str]):
        for chunk in chunks:
            self.add(chunk)

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        if not self.vectors:
            return []

        query_vector = embed_text(query)
        matrix = np.stack(self.vectors)

        # Cosine similarity between the query vector and every stored vector.
        query_norm = query_vector / np.linalg.norm(query_vector)
        matrix_norm = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
        similarities = matrix_norm @ query_norm

        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [(self.chunks[i], float(similarities[i])) for i in top_indices]
