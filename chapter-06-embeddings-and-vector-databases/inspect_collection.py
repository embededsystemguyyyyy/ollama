# inspect_collection.py
# A quick look at what's actually inside the Chroma collection.

from chroma_store import DocumentStore

store = DocumentStore(path="./chroma_db")
print(f"Total chunks: {store.count()}")

# Peek at a handful of raw entries, including their metadata.
sample = store.collection.get(limit=3, include=["documents", "metadatas"])
for doc, meta in zip(sample["documents"], sample["metadatas"]):
    print(f"\nSource: {meta['source']} (chunk {meta['chunk_index']})")
    print(f"Text: {doc[:150]}...")
