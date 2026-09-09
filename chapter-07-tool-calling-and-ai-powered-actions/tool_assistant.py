# tool_assistant.py
# A multi-tool assistant: the model decides which tool to call, our
# code executes it, and the result feeds back into the conversation.

import ollama
from tools import AVAILABLE_TOOLS, calculate, search_documents, get_weather

MODEL = "llama3.2:3b"  # use a model tagged as supporting tools on ollama.com/library

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools: a calculator, a local "
    "document search, and a weather lookup. Use a tool whenever it would give "
    "a more accurate answer than guessing. Only answer directly, without a "
    "tool, for things you're confident about without needing external data."
)

TOOLS = [calculate, search_documents, get_weather]


def run_tool_call(tool_call) -> str:
    """Execute a single tool call requested by the model, safely."""
    name = tool_call.function.name
    arguments = tool_call.function.arguments

    function_to_run = AVAILABLE_TOOLS.get(name)
    if function_to_run is None:
        return f"Error: unknown tool '{name}' requested."

    try:
        return function_to_run(**arguments)
    except TypeError as exc:
        return f"Error: invalid arguments for '{name}': {exc}"
    except Exception as exc:
        return f"Error: tool '{name}' failed: {exc}"


def chat_with_tools(messages: list[dict]) -> str:
    response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
    assistant_message = response["message"]

    tool_calls = assistant_message.get("tool_calls")

    if not tool_calls:
        return assistant_message["content"]

    # Record the assistant's tool-call request in history before executing.
    messages.append(assistant_message)

    for tool_call in tool_calls:
        result = run_tool_call(tool_call)
        print(f"  [tool call] {tool_call.function.name}({tool_call.function.arguments}) -> {result[:80]}")
        messages.append({"role": "tool", "content": result})

    # Ask the model to produce a final answer now that it has tool results.
    final_response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
    final_message = final_response["message"]
    messages.append(final_message)

    return final_message["content"]


def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Multi-tool assistant. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        answer = chat_with_tools(messages)
        print(f"Assistant: {answer}\n")


if __name__ == "__main__":
    main()
