# memory_check.py
# Reports the approximate memory footprint of a currently loaded model
# by parsing `ollama ps` output.

import subprocess


def get_loaded_model_info() -> str:
    result = subprocess.run(["ollama", "ps"], capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
    import ollama

    # Trigger a load, then immediately check what's resident in memory.
    ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": "hi"}])
    print(get_loaded_model_info())
