# build_knowledge_base.py
# Indexes every .txt and .pdf file in a folder into a persistent Chroma store.

from pathlib import Path
from ingest import extract_text_from_pdf, clean_text
from chunking import chunk_text
from chroma_store import DocumentStore


def load_and_clean(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        raw = extract_text_from_pdf(str(path))
    else:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    return clean_text(raw)


def build_knowledge_base(folder: str, store: DocumentStore):
    folder_path = Path(folder)
    supported = list(folder_path.glob("*.pdf")) + list(folder_path.glob("*.txt"))

    if not supported:
        print(f"No .pdf or .txt files found in {folder}")
        return

    for file_path in supported:
        print(f"Indexing {file_path.name}...")
        text = load_and_clean(file_path)
        chunks = chunk_text(text, chunk_size=400, overlap=80)
        store.add_chunks(chunks, source=file_path.name)
        print(f"  -> {len(chunks)} chunks added")

    print(f"\nKnowledge base ready: {store.count()} total chunks indexed")


if __name__ == "__main__":
    import sys

    folder = sys.argv[1] if len(sys.argv) > 1 else "./documents"
    store = DocumentStore(path="./chroma_db")
    build_knowledge_base(folder, store)
