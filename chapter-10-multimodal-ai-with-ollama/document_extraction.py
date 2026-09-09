# document_extraction.py
# Extracts structured data from a document image using a vision model
# combined with Ollama's structured-output support.

import ollama
from pydantic import BaseModel

VISION_MODEL = "qwen2.5vl:7b"  # strong at document/table understanding


class ReceiptData(BaseModel):
    merchant_name: str
    total_amount: str
    date: str
    line_items: list[str]


def extract_receipt(image_path: str) -> ReceiptData:
    response = ollama.chat(
        model=VISION_MODEL,
        messages=[{
            "role": "user",
            "content": (
                "Extract the merchant name, total amount, date, and line "
                "items from this receipt image. If a field isn't visible, "
                "use an empty string or empty list."
            ),
            "images": [image_path],
        }],
        format=ReceiptData.model_json_schema(),
    )
    return ReceiptData.model_validate_json(response["message"]["content"])


if __name__ == "__main__":
    result = extract_receipt("receipt.jpg")
    print(f"Merchant: {result.merchant_name}")
    print(f"Total:    {result.total_amount}")
    print(f"Date:     {result.date}")
    print("Items:")
    for item in result.line_items:
        print(f"  - {item}")
