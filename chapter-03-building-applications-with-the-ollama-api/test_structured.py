# test_structured.py
# Demonstrates forcing model output into a defined schema.

from pydantic import BaseModel
from ollama_client import chat_structured


class MovieReview(BaseModel):
    title: str
    sentiment: str   # "positive", "negative", or "mixed"
    summary: str
    rating_out_of_ten: int


def main():
    messages = [
        {"role": "user", "content": (
            "Analyze this review and extract structured data from it: "
            "'Inception was visually stunning and the concept was brilliant, "
            "but the pacing dragged in the middle third. Still, one of the "
            "better sci-fi films of its decade. I'd give it an 8.'"
        )}
    ]

    review = chat_structured("llama3.2:3b", messages, MovieReview)

    print(f"Title:     {review.title}")
    print(f"Sentiment: {review.sentiment}")
    print(f"Rating:    {review.rating_out_of_ten}/10")
    print(f"Summary:   {review.summary}")


if __name__ == "__main__":
    main()
