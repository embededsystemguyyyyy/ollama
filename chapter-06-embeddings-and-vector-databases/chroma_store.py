# chroma_store.py
# A reusable wrapper around ChromaDB for local, persistent semantic search,
# using Ollama for embeddings instead of Chroma's default embedding function.

import chromadb
import ollama

EMBED_MODEL = "nomic-embed-text"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts using Ollama's embedding model."""
    response = ollama.embed(model=EMBED_MODEL, input=texts)
    return response["embeddings"]


class DocumentStore:
    def __init__(self, path: str = "./chroma_db", collection_name: str = "documents"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[str], source: str):
        """Add chunks from a single source document, with metadata attached."""
        if not chunks:
            return

        embeddings = embed_texts(chunks)
        ids = [f"{source}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    def search(self, query: str, top_k: int = 3, source_filter: str | None = None) -> list[dict]:
        query_embedding = embed_texts([query])[0]

        where_clause = {"source": source_filter} if source_filter else None

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause,
        )

        matches = []
        for doc, meta, distance in zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        ):
            matches.append({"text": doc, "source": meta["source"], "distance": distance})
        return matches

    def count(self) -> int:
        return self.collection.count()
