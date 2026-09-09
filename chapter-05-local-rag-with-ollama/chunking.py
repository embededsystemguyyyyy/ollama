# chunking.py
# Splits cleaned text into overlapping word-based chunks.

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> list[str]:
    """
    Splits text into chunks of roughly `chunk_size` words, with `overlap`
    words shared between consecutive chunks so ideas at chunk boundaries
    aren't lost entirely.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += chunk_size - overlap  # move forward, but re-include the overlap

    return chunks


if __name__ == "__main__":
    sample = "word " * 1000  # a fake 1000-word document for a quick sanity check
    result = chunk_text(sample, chunk_size=400, overlap=80)
    print(f"Produced {len(result)} chunks")
    print(f"Chunk 1 length: {len(result[0].split())} words")
    print(f"Chunk 2 length: {len(result[1].split())} words")
