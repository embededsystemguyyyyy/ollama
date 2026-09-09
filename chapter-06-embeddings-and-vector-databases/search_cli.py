# search_cli.py
# A simple interactive semantic search interface over the knowledge base.

from chroma_store import DocumentStore


def main():
    store = DocumentStore(path="./chroma_db")
    print(f"Knowledge base loaded: {store.count()} chunks. Type 'exit' to quit.\n")

    while True:
        query = input("Search: ").strip()
        if query.lower() == "exit":
            break
        if not query:
            continue

        results = store.search(query, top_k=5)
        for i, match in enumerate(results, start=1):
            print(f"\n[{i}] source={match['source']} distance={match['distance']:.4f}")
            print(f"    {match['text'][:200]}...")
        print()


if __name__ == "__main__":
    main()
