# workspace_capabilities.py
# Thin adapters connecting the router to each capability built in
# earlier chapters. Each function has the same shape: (user_input) -> str.

from ollama_client import chat_once
from chroma_store import DocumentStore
from tools import calculate, get_weather
from sql_assistant import ask_database

_doc_store = None


def handle_chat(user_input: str) -> str:
    return chat_once("llama3.2:3b", [{"role": "user", "content": user_input}])


def handle_documents(user_input: str) -> str:
    global _doc_store
    if _doc_store is None:
        _doc_store = DocumentStore(path="./chroma_db")

    if _doc_store.count() == 0:
        return "No documents have been indexed yet. Add some to ./documents and re-run build_knowledge_base.py."

    results = _doc_store.search(user_input, top_k=3)
    context = "\n\n".join(r["text"] for r in results)

    messages = [
        {"role": "system", "content": (
            "Answer using ONLY the provided context. If the answer isn't "
            "present, say so clearly."
        )},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_input}"},
    ]
    return chat_once("llama3.2:3b", messages)


def handle_tools(user_input: str) -> str:
    import ollama
    from tools import AVAILABLE_TOOLS

    messages = [{"role": "user", "content": user_input}]
    response = ollama.chat(model="llama3.2:3b", messages=messages, tools=[calculate, get_weather])
    message = response["message"]

    tool_calls = message.get("tool_calls")
    if not tool_calls:
        return message["content"]

    messages.append(message)
    for call in tool_calls:
        func = AVAILABLE_TOOLS.get(call.function.name)
        result = func(**call.function.arguments) if func else "Unknown tool."
        messages.append({"role": "tool", "content": str(result)})

    final = ollama.chat(model="llama3.2:3b", messages=messages, tools=[calculate, get_weather])
    return final["message"]["content"]


def handle_research(user_input: str) -> str:
    from research_agent import run_agent
    return run_agent(user_input)


def handle_database(user_input: str) -> str:
    return ask_database(user_input, db_path="sample.db")


def handle_image(user_input: str, image_path: str) -> str:
    from vision_tools import describe_image
    return describe_image(image_path, prompt=user_input)


HANDLERS = {
    "CHAT": handle_chat,
    "DOCUMENTS": handle_documents,
    "TOOLS": handle_tools,
    "RESEARCH": handle_research,
    "DATABASE": handle_database,
    # IMAGE is handled specially in the workspace, since it needs an image path
}
