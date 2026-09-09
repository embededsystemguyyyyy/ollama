# local_assistant.py
# An interactive CLI assistant with real conversation memory,
# built on top of ollama_client.py.

from ollama_client import Conversation, OllamaClientError

SYSTEM_PROMPT = (
    "You are a helpful, concise local AI assistant running entirely on the "
    "user's own hardware. Keep answers focused and avoid unnecessary padding."
)


def main():
    conversation = Conversation(model="llama3.2:3b", system_prompt=SYSTEM_PROMPT)

    print("Local AI Assistant   type 'exit' to quit, 'reset' to clear memory.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if user_input.lower() == "reset":
            conversation.reset()
            print("(conversation memory cleared)\n")
            continue

        print("Assistant: ", end="", flush=True)
        try:
            for piece in conversation.ask_stream(user_input):
                print(piece, end="", flush=True)
            print("\n")
        except OllamaClientError as exc:
            print(f"\n[Error: {exc}]")
            print("Is 'ollama serve' running, and is the model pulled?\n")


if __name__ == "__main__":
    main()
