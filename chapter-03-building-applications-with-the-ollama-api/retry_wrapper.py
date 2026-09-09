# retry_wrapper.py
# A small retry decorator for Ollama calls, to smooth over transient failures.

import time
import functools
from ollama_client import OllamaClientError


def with_retries(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except OllamaClientError as exc:
                    last_error = exc
                    if attempt < max_attempts:
                        wait = base_delay * (2 ** (attempt - 1))  # exponential backoff
                        print(f"Attempt {attempt} failed ({exc}), retrying in {wait}s...")
                        time.sleep(wait)
            raise last_error
        return wrapper
    return decorator
