# model_warmer.py
# Periodically pings a model with a trivial request to keep it resident
# in memory, avoiding cold-start latency on real user requests.

import threading
import time
import ollama

def keep_warm(model: str, interval_seconds: int = 240):
    def _ping_loop():
        while True:
            try:
                ollama.chat(model=model, messages=[{"role": "user", "content": "ping"}],
                            options={"num_predict": 1})
            except Exception:
                pass  # a failed warm-up ping shouldn't crash the warmer thread
            time.sleep(interval_seconds)

    thread = threading.Thread(target=_ping_loop, daemon=True)
    thread.start()
