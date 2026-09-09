# multimodal_assistant.py
# Routes a request to text-only or vision processing depending on
# whether an image was provided.

from ollama_client import chat_once
from vision_tools import describe_image


def ask(question: str, image_path: str | None = None) -> str:
    if image_path:
        return describe_image(image_path, prompt=question)
    return chat_once("llama3.2:3b", [{"role": "user", "content": question}])


def main():
    print("Multimodal assistant. Type 'exit' to quit.")
    print("To include an image, format your input as: <question> | <image_path>\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        if "|" in user_input:
            question, image_path = [p.strip() for p in user_input.split("|", 1)]
        else:
            question, image_path = user_input, None

        answer = ask(question, image_path)
        print(f"Assistant: {answer}\n")


if __name__ == "__main__":
    main()
