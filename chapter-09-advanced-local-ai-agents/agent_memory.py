# agent_memory.py
# Persistent, cross-session memory for agents, built on Chapter 6's
# DocumentStore. Lets an agent recall past research instead of starting
# from zero every run.

from chroma_store import DocumentStore
from datetime import datetime


class AgentMemory:
    def __init__(self, path: str = "./agent_memory_db"):
        self.store = DocumentStore(path=path, collection_name="agent_memory")

    def remember(self, content: str, topic: str):
        timestamped = f"[{datetime.now().date()}] {content}"
        self.store.add_chunks([timestamped], source=topic)

    def recall(self, query: str, top_k: int = 3) -> list[str]:
        results = self.store.search(query, top_k=top_k)
        return [r["text"] for r in results]
