# agent_notes.py
# A simple scratchpad the agent can write to and read from during its run.

class Notepad:
    def __init__(self):
        self.notes: list[str] = []

    def add_note(self, note: str) -> str:
        """Save a piece of information the agent has learned, for later use in the report."""
        self.notes.append(note)
        return f"Note saved. Total notes: {len(self.notes)}"

    def get_all_notes(self) -> str:
        if not self.notes:
            return "No notes recorded yet."
        return "\n".join(f"{i+1}. {n}" for i, n in enumerate(self.notes))
