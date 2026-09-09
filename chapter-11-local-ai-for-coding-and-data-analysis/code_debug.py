# code_debug.py
# Debugging assistant that takes actual error output, not a vague complaint.

from ollama_client import chat_once

CODING_MODEL = "qwen2.5-coder:7b"


def debug_error(code: str, error_traceback: str) -> str:
    messages = [
        {"role": "system", "content": (
            "You are debugging a Python error. Given the code and the full "
            "traceback, identify the root cause and provide a corrected "
            "version of the relevant code. Be specific about which line "
            "caused the failure and why."
        )},
        {"role": "user", "content": f"Code:\n{code}\n\nTraceback:\n{error_traceback}"},
    ]
    return chat_once(CODING_MODEL, messages, temperature=0.2)


if __name__ == "__main__":
    broken_code = '''
def average(numbers):
    return sum(numbers) / len(numbers)

print(average([]))
'''

    traceback_text = '''
Traceback (most recent call last):
  File "test.py", line 4, in <module>
    print(average([]))
  File "test.py", line 2, in average
    return sum(numbers) / len(numbers)
ZeroDivisionError: division by zero
'''

    print(debug_error(broken_code, traceback_text))
