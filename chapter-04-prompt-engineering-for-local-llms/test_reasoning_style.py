# test_reasoning_style.py
# Compares a plain question against the same question with unnecessary
# manual chain-of-thought scaffolding bolted on, against a reasoning model.

from ollama_client import chat_once

REASONING_MODEL = "deepseek-r1:7b"  # substitute whatever reasoning model you have pulled

QUESTION = "A train leaves at 3pm going 60mph. Another leaves the same station at 4pm going 90mph in the same direction. What time does the second train catch the first?"

plain = [{"role": "user", "content": QUESTION}]

overinstructed = [{"role": "user", "content": (
    "Think step by step. First, identify the variables. Then, set up an "
    f"equation. Then solve it carefully, showing all work. Question: {QUESTION}"
)}]

print("--- Plain question ---")
print(chat_once(REASONING_MODEL, plain, temperature=0.2))

print("\n--- Over-instructed ---")
print(chat_once(REASONING_MODEL, overinstructed, temperature=0.2))
