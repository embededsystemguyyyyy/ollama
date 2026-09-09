# hello_ollama.py
# A minimal first contact with a local model via the Ollama Python library.

import ollama

def main():
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "user", "content": "In one paragraph, explain what makes local AI different from cloud AI."}
        ],
    )
    print(response["message"]["content"])

if __name__ == "__main__":
    main()
