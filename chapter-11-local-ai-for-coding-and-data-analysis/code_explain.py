# code_explain.py
# Explains or refactors a function using its full surrounding file as context.

from pathlib import Path
from ollama_client import chat_once

CODING_MODEL = "qwen2.5-coder:7b"


def explain_code(file_path: str, target_function: str | None = None) -> str:
    code = Path(file_path).read_text()

    focus = f" Focus specifically on the function `{target_function}`." if target_function else ""
    messages = [
        {"role": "system", "content": (
            "You are a senior developer reviewing code. Explain what this "
            f"code does, clearly and concisely.{focus}"
        )},
        {"role": "user", "content": code},
    ]
    return chat_once(CODING_MODEL, messages, temperature=0.3)


def suggest_refactor(file_path: str, target_function: str) -> str:
    code = Path(file_path).read_text()

    messages = [
        {"role": "system", "content": (
            "You are a senior developer. Suggest a cleaner implementation of "
            f"the function `{target_function}` from this file. Explain briefly "
            "why the change improves the code, then show the improved function."
        )},
        {"role": "user", "content": code},
    ]
    return chat_once(CODING_MODEL, messages, temperature=0.3)


if __name__ == "__main__":
    print(explain_code("ollama_client.py", target_function="Conversation"))
