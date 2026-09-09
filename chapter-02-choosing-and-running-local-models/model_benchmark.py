# model_benchmark.py
# Runs a fixed set of prompts against a fixed set of models and reports
# latency, throughput, and the raw output so you can compare quality by eye.

import time
import ollama

MODELS = [
    "llama3.2:3b",
    "qwen2.5:3b",
    "gemma2:2b",
]

PROMPTS = [
    "Summarize the plot of Romeo and Juliet in two sentences.",
    "Write a Python function that returns the nth Fibonacci number.",
    "What are three risks of deploying an AI agent without human oversight?",
]


def run_single(model: str, prompt: str) -> dict:
    """Send one prompt to one model and measure latency and throughput."""
    start = time.perf_counter()

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    elapsed = time.perf_counter() - start
    content = response["message"]["content"]

    # eval_count is the number of tokens generated, reported by Ollama
    tokens_generated = response.get("eval_count", 0)
    tokens_per_second = tokens_generated / elapsed if elapsed > 0 else 0

    return {
        "model": model,
        "prompt": prompt,
        "elapsed_seconds": round(elapsed, 2),
        "tokens_generated": tokens_generated,
        "tokens_per_second": round(tokens_per_second, 1),
        "output": content,
    }


def main():
    results = []

    for model in MODELS:
        print(f"\n=== Benchmarking {model} ===")
        for prompt in PROMPTS:
            print(f"  Prompt: {prompt[:50]}...")
            result = run_single(model, prompt)
            results.append(result)
            print(f"    → {result['elapsed_seconds']}s, "
                  f"{result['tokens_per_second']} tok/s")

    print_report(results)


def print_report(results: list[dict]):
    print("\n" + "=" * 70)
    print("SUMMARY REPORT")
    print("=" * 70)

    for result in results:
        print(f"\nModel:   {result['model']}")
        print(f"Prompt:  {result['prompt']}")
        print(f"Time:    {result['elapsed_seconds']}s "
              f"({result['tokens_per_second']} tok/s)")
        print(f"Output:  {result['output'][:200]}...")


if __name__ == "__main__":
    main()
