# raw_http_example.py
# The same chat call as above, but using requests directly against
# the Ollama REST API instead of the ollama library.

import requests
import json

def chat_raw(model: str, messages: list[dict]) -> str:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": model, "messages": messages, "stream": False},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]


if __name__ == "__main__":
    reply = chat_raw("llama3.2:3b", [{"role": "user", "content": "Say hello in French."}])
    print(reply)
