# code_generation.py
# Focused code generation using the coding prompt template from Chapter 4,
# with a coding-specialized model.

from prompt_templates import coding_prompt
from ollama_client import chat_once

CODING_MODEL = "qwen2.5-coder:7b"


def generate_code(task: str, language: str = "Python", constraints: list[str] | None = None) -> str:
    messages = coding_prompt(task, language=language, constraints=constraints)
    return chat_once(CODING_MODEL, messages, temperature=0.2)


if __name__ == "__main__":
    code = generate_code(
        task=(
            "Write a function `parse_log_line(line: str) -> dict` that parses "
            "a log line in the format '[2026-01-15 10:30:00] ERROR: message here' "
            "into a dict with keys 'timestamp', 'level', and 'message'."
        ),
        constraints=["No external dependencies", "Handle lines that don't match the format by returning None"],
    )
    print(code)
