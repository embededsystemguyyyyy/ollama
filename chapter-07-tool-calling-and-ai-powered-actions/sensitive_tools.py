# sensitive_tools.py
# Demonstrates a human-in-the-loop confirmation gate for a tool with
# real side effects, rather than letting the model execute it freely.

from pathlib import Path

NOTES_FILE = Path("notes.txt")


def save_note(content: str) -> str:
    """Save a short note to a local notes file, appending to any existing notes."""
    print(f"\n[CONFIRMATION REQUIRED] The assistant wants to save this note:")
    print(f'  "{content}"')
    approval = input("Allow? (y/n): ").strip().lower()

    if approval != "y":
        return "The user declined to save this note."

    with NOTES_FILE.open("a", encoding="utf-8") as f:
        f.write(content + "\n")

    return "Note saved successfully."
