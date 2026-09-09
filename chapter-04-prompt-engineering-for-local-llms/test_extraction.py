# test_extraction.py
# Combines a structured extraction prompt with Ollama's format parameter
# for maximum reliability.

import ollama
from prompt_templates import extraction_prompt

TEXT = (
    "Hi, this is Sarah Chen. I'd like to book a table for 4 people "
    "this Friday at 7:30 PM. My phone number is 555-0142."
)

FIELDS = {
    "name": "the customer's full name",
    "party_size": "number of people, as an integer",
    "date": "the requested date, described as given",
    "time": "the requested time",
    "phone": "the phone number if provided",
}


def main():
    messages = extraction_prompt(TEXT, FIELDS)

    response = ollama.chat(
        model="llama3.2:3b",
        messages=messages,
        format="json",
        options={"temperature": 0.1},
    )

    print(response["message"]["content"])


if __name__ == "__main__":
    main()
