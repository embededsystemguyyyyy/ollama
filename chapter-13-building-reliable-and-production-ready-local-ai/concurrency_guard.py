# concurrency_guard.py
# Limits how many requests can be actively running inference at once,
# preventing a burst of traffic from exhausting local RAM/VRAM.

import threading

class ConcurrencyGuard:
    def __init__(self, max_concurrent: int = 2):
        self.semaphore = threading.Semaphore(max_concurrent)

    def __enter__(self):
        acquired = self.semaphore.acquire(timeout=30)
        if not acquired:
            raise TimeoutError("Server is at capacity, request timed out waiting for a slot.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.semaphore.release()
        return False
