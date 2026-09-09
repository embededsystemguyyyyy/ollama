# ingest.py
# Extracts and lightly cleans text from a PDF file.

import re
from pypdf import PdfReader


def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages_text = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)

    return "\n".join(pages_text)


def clean_text(raw_text: str) -> str:
    # Collapse repeated whitespace and blank lines into single spaces/breaks.
    text = re.sub(r"[ \t]+", " ", raw_text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.pdf"
    raw = extract_text_from_pdf(path)
    cleaned = clean_text(raw)
    print(f"Extracted {len(cleaned)} characters from {path}")
    print(cleaned[:500])
