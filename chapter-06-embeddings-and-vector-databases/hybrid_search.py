# hybrid_search.py
# Combines Chroma's semantic search with a basic keyword match pass,
# merging and deduplicating results.

from chroma_store import DocumentStore


def keyword_search(store: DocumentStore, query: str, top_k: int = 5) -> list[dict]:
    """
    A simple keyword fallback: pull a large batch of chunks via semantic
    search, then re-rank by literal keyword overlap. This isn't a full
    inverted-index search engine, but it catches exact-term matches that
    pure semantic search can sometimes rank too low.
    """
    query_words = set(query.lower().split())
    candidates = store.search(query, top_k=25)  # cast a wide net first

    def overlap_score(text: str) -> int:
        text_words = set(text.lower().split())
        return len(query_words & text_words)

    ranked = sorted(candidates, key=lambda c: overlap_score(c["text"]), reverse=True)
    return ranked[:top_k]


def hybrid_search(store: DocumentStore, query: str, top_k: int = 5) -> list[dict]:
    semantic_results = store.search(query, top_k=top_k)
    keyword_results = keyword_search(store, query, top_k=top_k)

    seen = set()
    merged = []

    # Interleave the two result sets, favoring semantic first, deduping by text.
    for pair in zip(semantic_results, keyword_results):
        for result in pair:
            key = result["text"][:80]
            if key not in seen:
                seen.add(key)
                merged.append(result)

    return merged[:top_k]


if __name__ == "__main__":
    store = DocumentStore(path="./chroma_db")
    query = "exact error code E-4021"  # example: a query with a precise term
    for result in hybrid_search(store, query):
        print(f"[{result['source']}] {result['text'][:150]}...")
