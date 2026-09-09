# test_classification.py
# Compares zero-shot vs. few-shot classification accuracy.

from ollama_client import chat_once
from prompt_templates import classification_prompt

CATEGORIES = ["BILLING", "TECHNICAL", "GENERAL"]

TEST_CASES = [
    "I was charged twice for my subscription this month.",
    "The app crashes every time I try to upload a photo.",
    "What are your business hours?",
]

FEW_SHOT_EXAMPLES = [
    ("My credit card was billed incorrectly.", "BILLING"),
    ("The login page throws a 500 error.", "TECHNICAL"),
    ("Do you offer student discounts?", "GENERAL"),
]


def main():
    print("--- Zero-shot ---")
    for text in TEST_CASES:
        messages = classification_prompt(text, CATEGORIES)
        result = chat_once("llama3.2:3b", messages)
        print(f"{text[:40]:40} -> {result.strip()}")

    print("\n--- Few-shot ---")
    for text in TEST_CASES:
        messages = classification_prompt(text, CATEGORIES, examples=FEW_SHOT_EXAMPLES)
        result = chat_once("llama3.2:3b", messages)
        print(f"{text[:40]:40} -> {result.strip()}")


if __name__ == "__main__":
    main()
