# ollama_client.py
# A reusable wrapper around the Ollama Python library, handling
# conversation state, streaming, structured output, and errors.

import ollama
from typing import Optional
from pydantic import BaseModel


class OllamaClientError(Exception):
    """Raised when a call to Ollama fails in a way the app should handle gracefully."""
    pass


def chat_once(model: str, messages: list[dict], **options) -> str:
    """Send a full message list and return the complete text response."""
    try:
        response = ollama.chat(model=model, messages=messages, options=options or None)
        return response["message"]["content"]
    except Exception as exc:
        raise OllamaClientError(f"Chat request failed: {exc}") from exc


def chat_stream(model: str, messages: list[dict], **options):
    """Send a full message list and yield text chunks as they arrive."""
    try:
        stream = ollama.chat(model=model, messages=messages, stream=True, options=options or None)
        for chunk in stream:
            piece = chunk["message"]["content"]
            if piece:
                yield piece
    except Exception as exc:
        raise OllamaClientError(f"Streaming chat request failed: {exc}") from exc


def chat_structured(model: str, messages: list[dict], schema: type[BaseModel]) -> BaseModel:
    """
    Send a message list and force the response into the shape of a Pydantic
    model. Returns a validated instance of that model, not a raw string.
    """
    try:
        response = ollama.chat(
            model=model,
            messages=messages,
            format=schema.model_json_schema(),
        )
        raw_json = response["message"]["content"]
        return schema.model_validate_json(raw_json)
    except Exception as exc:
        raise OllamaClientError(f"Structured chat request failed: {exc}") from exc


class Conversation:
    """
    Keeps track of message history across turns so the model has
    context from earlier in the conversation.
    """

    def __init__(self, model: str, system_prompt: Optional[str] = None):
        self.model = model
        self.messages: list[dict] = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def ask(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})
        reply = chat_once(self.model, self.messages)
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def ask_stream(self, user_message: str):
        self.messages.append({"role": "user", "content": user_message})
        full_reply = ""
        for piece in chat_stream(self.model, self.messages):
            full_reply += piece
            yield piece
        self.messages.append({"role": "assistant", "content": full_reply})

    def reset(self):
        system = [m for m in self.messages if m["role"] == "system"]
        self.messages = system
