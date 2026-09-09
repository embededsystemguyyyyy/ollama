# hello_ollama_stream.py
# Same idea as before, but we print tokens as they arrive instead of
# waiting for the full response.

import ollama

def main():
    stream = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "user", "content": "List three practical uses for a local LLM."}
        ],
        stream=True,
    )

    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)

    print()  # final newline so your terminal prompt doesn't end up glued to the output

if __name__ == "__main__":
    main()
