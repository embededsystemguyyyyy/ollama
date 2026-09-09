# coding_assistant.py
# A CLI-based local coding assistant that can generate, explain, debug,
# test, and analyze a real small repository.

import sys
from code_generation import generate_code
from code_explain import explain_code, suggest_refactor
from code_debug import debug_error
from test_generation import generate_tests
from repo_context import build_file_tree, gather_code_summary
from ollama_client import chat_once

CODING_MODEL = "qwen2.5-coder:7b"


def analyze_repo(root: str, question: str) -> str:
    tree = build_file_tree(root)
    summary = gather_code_summary(root)

    messages = [
        {"role": "system", "content": (
            "You are a senior developer reviewing a codebase. Use the file "
            "tree and code samples provided to answer the question accurately. "
            "If you're not confident about something not shown in the samples, "
            "say so rather than guessing."
        )},
        {"role": "user", "content": (
            f"File tree:\n{tree}\n\nCode samples:\n{summary}\n\nQuestion: {question}"
        )},
    ]
    return chat_once(CODING_MODEL, messages, temperature=0.3)


def main():
    print("Local Coding Assistant")
    print("Commands: generate | explain <file> | refactor <file> <function> | "
          "tests <file> | analyze <folder>\n")

    while True:
        command = input("> ").strip()
        if command.lower() in ("exit", "quit"):
            break
        if not command:
            continue

        parts = command.split(" ", 2)
        action = parts[0]

        try:
            if action == "generate":
                task = input("Describe the task: ")
                print(generate_code(task))

            elif action == "explain" and len(parts) > 1:
                print(explain_code(parts[1]))

            elif action == "refactor" and len(parts) > 2:
                print(suggest_refactor(parts[1], parts[2]))

            elif action == "tests" and len(parts) > 1:
                from pathlib import Path
                code = Path(parts[1]).read_text()
                print(generate_tests(code))

            elif action == "analyze" and len(parts) > 1:
                question = input("What do you want to know about this codebase? ")
                print(analyze_repo(parts[1], question))

            else:
                print("Unrecognized command or missing argument.")

        except Exception as exc:
            print(f"Error: {exc}")

        print()


if __name__ == "__main__":
    main()
