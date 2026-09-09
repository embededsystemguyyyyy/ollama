# workspace_router.py
# Classifies an incoming request into one of the platform's capabilities,
# using the exact classification prompting pattern from Chapter 4.

from prompt_templates import classification_prompt
from ollama_client import chat_once

ROUTER_MODEL = "llama3.2:3b"

CAPABILITIES = ["DOCUMENTS", "TOOLS", "RESEARCH", "IMAGE", "DATABASE", "CHAT"]

ROUTING_EXAMPLES = [
    ("What does our refund policy document say about late cancellations?", "DOCUMENTS"),
    ("What's 340 divided by 12?", "TOOLS"),
    ("What's the weather like in Berlin right now?", "TOOLS"),
    ("Research the pros and cons of solar panels for a home in a cold climate.", "RESEARCH"),
    ("What's in this photo I just uploaded?", "IMAGE"),
    ("How many customers do we have in Seattle?", "DATABASE"),
    ("Tell me a joke.", "CHAT"),
]


def route_request(user_input: str, has_image: bool = False) -> str:
    if has_image:
        return "IMAGE"  # an attached image is an unambiguous signal, skip the model call

    messages = classification_prompt(user_input, CAPABILITIES, examples=ROUTING_EXAMPLES)
    result = chat_once(ROUTER_MODEL, messages, temperature=0.1)
    label = result.strip().upper()

    return label if label in CAPABILITIES else "CHAT"  # safe fallback
