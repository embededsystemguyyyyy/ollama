# repo_context.py
# Builds a compact summary of a repository's structure and key files,
# for use as context in repository-wide analysis.

from pathlib import Path

IGNORE_DIRS = {".git", "__pycache__", "venv", "node_modules", ".venv"}
CODE_EXTENSIONS = {".py", ".js", ".ts", ".java", ".go"}


def build_file_tree(root: str) -> str:
    lines = []
    root_path = Path(root)

    for path in sorted(root_path.rglob("*")):
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue
        relative = path.relative_to(root_path)
        depth = len(relative.parts) - 1
        indent = "  " * depth
        lines.append(f"{indent}{relative.name}")

    return "\n".join(lines)


def gather_code_summary(root: str, max_files: int = 15, max_chars_per_file: int = 1000) -> str:
    root_path = Path(root)
    summaries = []
    count = 0

    for path in sorted(root_path.rglob("*")):
        if count >= max_files:
            break
        if path.suffix not in CODE_EXTENSIONS:
            continue
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue

        content = path.read_text(encoding="utf-8", errors="ignore")[:max_chars_per_file]
        summaries.append(f"### {path.relative_to(root_path)}\n{content}\n")
        count += 1

    return "\n".join(summaries)


if __name__ == "__main__":
    print(build_file_tree("."))
    print("\n--- Code summary ---\n")
    print(gather_code_summary(".", max_files=5))
