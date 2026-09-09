# prompt_templates.py
# Reusable, parameterized prompt builders for common task types.
# Each function returns a well-formed messages list ready for ollama_client.

def classification_prompt(text: str, categories: list[str], examples: list[tuple[str, str]] | None = None) -> list[dict]:
    """Build a message list for classifying text into one of a fixed set of categories."""
    category_list = ", ".join(categories)
    system = (
        f"Classify the user's text into exactly one of these categories: {category_list}. "
        "Respond with only the category name, nothing else."
    )
    messages = [{"role": "system", "content": system}]

    if examples:
        for example_text, example_label in examples:
            messages.append({"role": "user", "content": example_text})
            messages.append({"role": "assistant", "content": example_label})

    messages.append({"role": "user", "content": text})
    return messages


def extraction_prompt(text: str, fields: dict[str, str]) -> list[dict]:
    """
    Build a message list for extracting specific fields from text.
    `fields` maps field name -> description, e.g. {"date": "the event date in YYYY-MM-DD"}.
    """
    field_lines = "\n".join(f"- {name}: {desc}" for name, desc in fields.items())
    system = (
        "Extract the following fields from the user's text. "
        "If a field is not present, use null.\n\n"
        f"Fields to extract:\n{field_lines}\n\n"
        "Respond with valid JSON only, no explanation."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": text},
    ]


def summarization_prompt(text: str, max_sentences: int = 3, tone: str = "neutral") -> list[dict]:
    """Build a message list for summarizing text with explicit length and tone constraints."""
    system = (
        f"Summarize the user's text in at most {max_sentences} sentences, "
        f"using a {tone} tone. Do not add an introduction or conclusion. "
        "Only output the summary itself."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": text},
    ]


def coding_prompt(task: str, language: str = "Python", constraints: list[str] | None = None) -> list[dict]:
    """Build a message list for a focused, specific coding request."""
    constraint_lines = ""
    if constraints:
        constraint_lines = "\n\nConstraints:\n" + "\n".join(f"- {c}" for c in constraints)

    system = (
        f"You are an expert {language} developer. Write complete, correct, "
        "runnable code with no placeholder logic. Include brief comments "
        "only where they clarify non-obvious decisions."
    )
    user = f"{task}{constraint_lines}"

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
