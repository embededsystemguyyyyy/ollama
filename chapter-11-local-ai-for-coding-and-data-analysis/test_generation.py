# test_generation.py
# Generates unit tests for a given function, using its actual source code
# as context so the tests reflect the real signature and behavior.

from pathlib import Path
from ollama_client import chat_once

CODING_MODEL = "qwen2.5-coder:7b"


def generate_tests(function_code: str, framework: str = "pytest") -> str:
    messages = [
        {"role": "system", "content": (
            f"Write {framework} unit tests for the given function. Cover the "
            "happy path, at least one edge case, and at least one invalid-input "
            "case if applicable. Output complete, runnable test code only."
        )},
        {"role": "user", "content": function_code},
    ]
    return chat_once(CODING_MODEL, messages, temperature=0.3)


if __name__ == "__main__":
    function_code = '''
def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping intervals, assuming input is unsorted."""
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged
'''

    tests = generate_tests(function_code)
    print(tests)
