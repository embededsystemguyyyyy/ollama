# vision_tools.py
# Core functions for working with vision-capable Ollama models.

import ollama

VISION_MODEL = "llava"


def describe_image(image_path: str, prompt: str = "Describe this image in detail.") -> str:
    """Send an image to the vision model with a prompt and return the response."""
    response = ollama.chat(
        model=VISION_MODEL,
        messages=[{
            "role": "user",
            "content": prompt,
            "images": [image_path],
        }],
    )
    return response["message"]["content"]


def ask_about_image(image_path: str, question: str) -> str:
    """Ask a specific, targeted question about an image."""
    return describe_image(image_path, prompt=question)


def compare_images(image_paths: list[str], prompt: str = "Compare these images.") -> str:
    """Send multiple images at once for a comparative analysis."""
    response = ollama.chat(
        model=VISION_MODEL,
        messages=[{
            "role": "user",
            "content": prompt,
            "images": image_paths,
        }],
    )
    return response["message"]["content"]
