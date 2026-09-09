# pdf_assistant.py
# A complete private PDF knowledge assistant: ingest, chunk, embed,
# retrieve, and answer   all running locally.

import sys
from ingest import extract_text_from_pdf, clean_text
from chunking import chunk_text
from vector_store import SimpleVectorStore
from ollama_client import chat_once

CHAT_MODEL = "llama3.2:3b"

SYSTEM_PROMPT = (
    "You are a document assistant. Answer the user's question using ONLY "
    "the provided context. If the answer is not present in the context, "
    "say clearly: 'The document does not contain that information.' "
    "Do not use outside knowledge."
)


def build_index(pdf_path: str) -> SimpleVectorStore:
    print(f"Reading {pdf_path}...")
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned = clean_text(raw_text)

    print("Chunking...")
    chunks = chunk_text(cleaned, chunk_size=400, overlap=80)
    print(f"Created {len(chunks)} chunks")

    print("Embedding (this may take a moment)...")
    store = SimpleVectorStore()
    store.add_many(chunks)
    print("Index ready.\n")

    return store


def answer_question(store: SimpleVectorStore, question: str) -> str:
    results = store.search(question, top_k=3)
    context = "\n\n---\n\n".join(chunk for chunk, score in results)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]

    return chat_once(CHAT_MODEL, messages)


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "sample.pdf"
    store = build_index(pdf_path)

    print("Ask questions about the document. Type 'exit' to quit.\n")
    while True:
        question = input("Q: ").strip()
        if question.lower() == "exit":
            break
        if not question:
            continue

        answer = answer_question(store, question)
        print(f"A: {answer}\n")


if __name__ == "__main__":
    main()
