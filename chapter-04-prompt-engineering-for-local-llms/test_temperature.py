# test_temperature.py
# Shows the same creative prompt at three different temperature settings.

from ollama_client import chat_once

PROMPT = [{"role": "user", "content": "Write a one-sentence tagline for a coffee shop."}]

for temp in [0.1, 0.7, 1.3]:
    print(f"\n--- temperature = {temp} ---")
    for _ in range(2):
        result = chat_once("llama3.2:3b", PROMPT, temperature=temp)
        print(f"  {result.strip()}")
